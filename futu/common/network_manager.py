import errno
import datetime
import threading
from time import sleep
from futu.common.utils import *
from futu.quote.quote_query import parse_head
from .err import Err
from .sys_config import SysConfig
from .ft_logger import *
import enum


if IS_PY2:
    import selectors2 as selectors
    import Queue as queue
else:
    import queue
    import selectors


class ConnStatus:
    Start = 0
    Connecting = 1
    Connected = 2
    Closed = 3


class ConnectErr(enum.Enum):
    Ok = 0
    Fail = 1
    Timeout = 2


class CloseReason(enum.Enum):
    Close = 0
    RemoteClose = 1
    ReadFail = 2
    SendFail = 3
    ConnectFail = 4


class PacketErr(enum.Enum):
    Ok = 0
    Timeout = 1
    Invalid = 2
    Disconnect = 3
    SendFail = 4


class SyncReqRspInfo:
    def __init__(self):
        self.event = threading.Event()
        self.ret = RET_OK
        self.msg = ''
        self.data = None


class ConnectInfo:
    def __init__(self, is_sync):
        self.start_time = None
        self.event = None
        self.conn_id = 0
        self.err = ConnectErr.Ok
        self.msg = ''
        if is_sync:
            self.event = threading.Event()

    @property
    def is_sync(self):
        return self.event is not None

    def set_result(self, err, msg):
        self.err = err
        self.msg = msg
        if self.event is not None:
            self.event.set()

    def wait(self):
        if self.event is not None:
            self.event.wait()


class SendInfo:
    def __init__(self, is_sync):
        self.send_time = None
        self.proto_id = 0
        self.serial_no = 0
        self.header_dict = None
        self.err = PacketErr.Ok
        self.msg = ''
        self.event = None
        self.rsp = None
        if is_sync:
            self.event = threading.Event()

    @property
    def is_sync(self):
        return self.event is not None

    def set_result(self, err, msg, rsp):
        self.err = err
        self.msg = msg
        self.rsp = rsp
        if self.event is not None:
            self.event.set()

    def wait(self):
        if self.event is not None:
            self.event.wait()


class Connection:
    def __init__(self, conn_id, sock, addr, handler, is_encrypt, is_sync):
        self._conn_id = conn_id
        self.opend_conn_id = 0
        self.sock = sock
        self.is_encrypt = is_encrypt
        self.handler = handler
        self._peer_addr = addr
        self.status = ConnStatus.Start
        self.keep_alive_interval = 10
        self.last_keep_alive_time = datetime.now()
        self.timeout = None
        self.readbuf = bytearray()
        self.writebuf = bytearray()
        self.req_dict = {}  # ProtoInfo -> req time
        self.sync_req_dict = {}  # ProtoInfo -> SyncReqRspInfo
        self.connect_info = ConnectInfo(is_sync)
        self.connect_info.conn_id = conn_id
        self.send_info_dict = {} # ProtoInfo -> SendInfo

    @property
    def conn_id(self):
        return self._conn_id

    @property
    def peer_addr(self):
        return self._peer_addr

    def fileno(self):
        return self.sock.fileno


def is_socket_exception_wouldblock(e):
    has_errno = False
    if IS_PY2:
        if isinstance(e, IOError):
            has_errno = True
    else:
        if isinstance(e, OSError):
            has_errno = True

    if has_errno:
        if e.errno == errno.EWOULDBLOCK or e.errno == errno.EAGAIN or e.errno == errno.EINPROGRESS:
            return True
    return False


def make_ctrl_socks():
    LOCAL_HOST = '127.0.0.1'
    if IS_PY2:
        svr_sock = []
        lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        def svr_sock_func():
            try:
                sock, _ = lsock.accept()
                svr_sock.append(sock)
            except Exception as e:
                logger.warning('Ctrl sock fail: {}'.format(str(e)))
        try:
            lsock.bind((LOCAL_HOST, 0))
            _, port = lsock.getsockname()[:2]
            lsock.listen(1)
            thread = threading.Thread(target=svr_sock_func)
            thread.start()
            client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_sock.settimeout(0.1)
            client_sock.connect((LOCAL_HOST, port))
            thread.join()
            return svr_sock[0], client_sock
        except Exception as e:
            logger.warning('Ctrl sock fail: {}'.format(str(e)))
            return None, None
        finally:
            lsock.close()
    else:
        return socket.socketpair()


class NetManager:
    _default_inst = None
    _default_inst_lock = threading.Lock()

    @classmethod
    def default(cls):
        with cls._default_inst_lock:
            if cls._default_inst is None:
                cls._default_inst = NetManager()
            return cls._default_inst

    def __init__(self):
        self._use_count = 0
        self._next_conn_id = 1
        self._lock = threading.RLock()
        self._mgr_lock = threading.Lock()  # Used to control start and stop
        self._pending_read_conns = set()
        self._create_all()

    def _close_all(self):
        for sel_key in list(self._selector.get_map().values()):
            self._selector.unregister(sel_key.fileobj)
            sel_key.fileobj.close()
        self._selector.close()
        self._selector = None
        if self._r_sock:
            self._r_sock.close()
            self._r_sock = None
        if self._w_sock:
            self._w_sock.close()
            self._w_sock = None

    def _create_all(self):
        self._selector = selectors.DefaultSelector()
        self._req_queue = queue.Queue()
        self._sync_req_timeout = 12
        self._thread = None
        now = datetime.now()
        self._last_activate_time = now
        self._last_check_req_time = now
        self._r_sock, self._w_sock = make_ctrl_socks()
        self._selector.register(self._r_sock, selectors.EVENT_READ)

    def connect(self, addr, handler, timeout, is_encrypt, is_sync):
        with self._lock:
            conn_id = self._next_conn_id
            self._next_conn_id += 1

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024 * 1024)
        sock.setblocking(False)
        conn = Connection(conn_id, sock, addr, handler, is_encrypt, is_sync)
        conn.status = ConnStatus.Connecting
        conn.timeout = timeout

        def work():
            conn.connect_info.start_time = datetime.now()
            self._selector.register(sock, selectors.EVENT_WRITE, conn)
            try:
                sock.connect(addr)
            except Exception as e:
                if not is_socket_exception_wouldblock(e):
                    self._do_close(conn.conn_id, CloseReason.ConnectFail, str(e), False)
                    conn.connect_info.set_result(ConnectErr.Fail, str(e))
                    if not conn.connect_info.is_sync:
                        conn.handler.on_connect(conn_id, ConnectErr.Fail, str(e))

        self._req_queue.put(work)
        self._w_sock.send(b'1')

        return RET_OK, conn.connect_info

    def poll(self):
        now = datetime.now()
        events = self._selector.select(0.05)
        for key, evt_mask in events:
            if key.fileobj == self._r_sock:
                self._r_sock.recv(1024)
                while True:
                    try:
                        work = self._req_queue.get(block=False)
                        work()
                    except queue.Empty:
                        break
                continue
            conn = key.data
            if evt_mask & selectors.EVENT_WRITE != 0:
                self._on_write(conn)

            if evt_mask & selectors.EVENT_READ != 0:
                self._pending_read_conns.discard(conn)
                self._on_read(conn)

        pending_read_conns = list(self._pending_read_conns)
        self._pending_read_conns.clear()
        for conn in pending_read_conns:
            self._on_read(conn)

        activate_elapsed_time = now - self._last_activate_time
        check_req_elapsed_time = now - self._last_check_req_time
        is_activate = activate_elapsed_time.total_seconds() >= 0.05
        is_check_req = check_req_elapsed_time.total_seconds() >= 0.1

        if is_activate or is_check_req:
            for key in list(self._selector.get_map().values()):
                if key.fileobj == self._r_sock:
                    continue
                conn = key.data
                if conn.status == ConnStatus.Connecting:
                    if is_activate:
                        self._check_connect_timeout(conn, now)
                elif conn.status == ConnStatus.Connected:
                    if is_activate:
                        conn.handler.on_tick(conn.conn_id, now)
                    if is_check_req:
                        self._check_req(conn, now)

        if is_activate:
            self._last_activate_time = now
        if is_check_req:
            self._last_check_req_time = now

    def _check_connect_timeout(self, conn, now):
        time_delta = now - conn.connect_info.start_time
        if conn.timeout is not None and conn.timeout > 0 and time_delta.total_seconds() >= conn.timeout:
            self._on_connect_timeout(conn)

    def _check_req(self, conn, now):
        """

        :param conn:
        :type conn: Connection
        :param now:
        :type now: datetime
        :return:
        """
        req_dict = dict(conn.send_info_dict.items())
        for proto_info, send_info in req_dict.items():  # type: ProtoInfo, SendInfo
            elapsed_time = now - send_info.send_time
            if elapsed_time.total_seconds() >= self._sync_req_timeout:
                self._on_packet(conn, send_info.header_dict, PacketErr.Timeout, '', None)

    def _thread_func(self):
        while True:
            with self._lock:
                if not self.is_alive():
                    self._thread = None
                    break
            self.poll()

    def start(self):
        """
        Should be called from main thread
        :return:
        """
        with self._mgr_lock:
            with self._lock:
                self._use_count += 1

            if self._thread is None:
                self._create_all()
                self._thread = threading.Thread(target=self._thread_func)
                self._thread.setDaemon(SysConfig.get_all_thread_daemon())
                self._thread.start()

    def stop(self):
        with self._mgr_lock:
            with self._lock:
                self._use_count = max(self._use_count - 1, 0)

    def is_alive(self):
        with self._lock:
            return self._use_count > 0

    def do_send(self, conn_id, send_info: SendInfo, data):
        logger.debug2(FTLog.ONLY_FILE, 'Send: conn_id={}; proto_id={}; serial_no={}; total_len={};'.format(conn_id,
                                                                                                           send_info.proto_id,
                                                                                                           send_info.serial_no,
                                                                                                           len(data)))
        now = datetime.now()
        ret_code = RET_OK
        msg = ''
        conn = self._get_conn(conn_id)  # type: Connection
        if not conn:
            logger.debug(
                FTLog.make_log_msg('Send fail', conn_id=conn_id, proto_id=send_info.proto_id, serial_no=send_info.serial_no,
                                   msg=Err.ConnectionLost.text))
            ret_code, msg = RET_ERROR, Err.ConnectionLost.text
        elif conn.status != ConnStatus.Connected:
            ret_code, msg = RET_ERROR, Err.NotConnected.text

        if ret_code != RET_OK:
            logger.warning(FTLog.make_log_msg('Send fail', proto_id=send_info.proto_id, serial_no=send_info.serial_no,
                                              conn_id=conn_id, msg=msg))
            send_info.set_result(PacketErr.SendFail, msg, None)
            return

        proto_info = ProtoInfo(send_info.proto_id, send_info.serial_no)
        conn.send_info_dict[proto_info] = send_info
        size = 0
        try:
            if len(conn.writebuf) > 0:
                conn.writebuf.extend(data)
            else:
                size = conn.sock.send(data)
        except Exception as e:
            if is_socket_exception_wouldblock(e):
                pass
            else:
                ret_code, msg = RET_ERROR, str(e)

        if 0 < size < len(data):
            conn.writebuf.extend(data[size:])
            self._watch_write(conn, True)

        if ret_code != RET_OK:
            logger.warning(FTLog.make_log_msg('Send error', conn_id=conn_id, msg=msg))
            send_info.set_result(PacketErr.SendFail, msg, None)
            self._do_close(conn.conn_id, CloseReason.SendFail, msg, True)

        return RET_OK, ''

    def send(self, conn_id, data, is_sync=False):
        """

        :param conn_id:
        :param data:
        :return:
        """
        header = self._parse_req_head(data)
        send_info = SendInfo(is_sync)
        send_info.proto_id = header['proto_id']
        send_info.serial_no = header['serial_no']
        send_info.header_dict = header

        def work():
            send_info.send_time = datetime.now()
            self.do_send(conn_id, send_info, data)

        self._req_queue.put(work)
        self._w_sock.send(b'1')
        return RET_OK, send_info

    def close(self, conn_id):
        def work():
            self._do_close(conn_id, CloseReason.Close, '', True)

        self._req_queue.put(work)
        self._w_sock.send(b'1')

    def _do_close(self, conn_id, reason, msg, notify):
        conn = self._get_conn(conn_id)  # type: Connection
        if not conn:
            return
        if conn.sock is None:
            return
        self._selector.unregister(conn.sock)
        conn.sock.close()
        conn.sock = None
        conn.status = ConnStatus.Closed
        send_info: SendInfo
        for send_info in conn.send_info_dict.values():
            send_info.set_result(PacketErr.Disconnect, '', None)
        logger.debug("Close: conn_id={}".format(conn_id))
        if notify:
            conn.handler.on_disconnect(conn_id, reason, msg)

    def _watch_read(self, conn, is_watch):
        try:
            sel_key = self._selector.get_key(conn.sock)
        except KeyError:
            return

        if is_watch:
            new_event = sel_key.events | selectors.EVENT_READ
        else:
            new_event = sel_key.events & (~selectors.EVENT_READ)

        if new_event != 0:
            self._selector.modify(conn.sock, new_event, conn)
        else:
            self._selector.unregister(conn.sock)

    def _watch_write(self, conn, is_watch):
        try:
            sel_key = self._selector.get_key(conn.sock)
        except KeyError:
            return

        if is_watch:
            new_event = sel_key.events | selectors.EVENT_WRITE
        else:
            new_event = sel_key.events & (~selectors.EVENT_WRITE)

        if new_event != 0:
            self._selector.modify(conn.sock, new_event, conn)
        else:
            self._selector.unregister(conn.sock)

    def sync_query(self, conn_id, req_str):
        head_dict = self._parse_req_head(req_str)
        proto_info = ProtoInfo(head_dict['proto_id'], head_dict['serial_no'])
        rsp_info = SyncReqRspInfo()

        def work():
            conn = self._get_conn(conn_id)  # type: Connection
            ret, msg = RET_OK, ''
            if not conn:
                ret = RET_ERROR
                msg = Err.ConnectionLost.text
            else:
                conn.sync_req_dict[proto_info] = rsp_info
                self.do_send(conn_id, proto_info, req_str)

            if ret != RET_OK:
                rsp_info.ret = ret
                rsp_info.msg = msg
                rsp_info.event.set()

        self._req_queue.put(work)
        self._w_sock.send(b'1')

        rsp_info.event.wait()
        return rsp_info.ret, rsp_info.msg, rsp_info.data

    def _parse_req_head(self, req_str):
        head_len = get_message_head_len()
        req_head_dict = parse_head(req_str[:head_len])
        return req_head_dict

    def _parse_req_head_proto_info(self, req_str):
        head_len = get_message_head_len()
        proto_info = parse_proto_info(req_str[:head_len])
        return proto_info

    def _get_conn(self, conn_id):
        with self._lock:
            for sock, sel_key in self._selector.get_map().items():
                if sel_key.fileobj == self._r_sock:
                    continue
                conn = sel_key.data
                if conn.conn_id == conn_id:
                    return conn
            return None

    def _on_read(self, conn):
        if conn.status == ConnStatus.Closed:
            return

        packet_count = 0
        msg = ''
        is_closed = False
        try:
            data = conn.sock.recv(128 * 1024)
            if data == b'':
                is_closed = True
            else:
                conn.readbuf.extend(data)
        except Exception as e:
            if not is_socket_exception_wouldblock(e):
                is_closed = True
                msg = str(e)

        while len(conn.readbuf) > 0:
            head_len = get_message_head_len()
            if len(conn.readbuf) < head_len:
                break
            head_dict = parse_head(conn.readbuf[:head_len])
            body_len = head_dict['body_len']
            if len(conn.readbuf) < head_len + body_len:
                break

            rsp_body = conn.readbuf[head_len:head_len+body_len]
            del conn.readbuf[:head_len+body_len]
            packet_count += 1
            self._on_packet(conn, head_dict, PacketErr.Ok, '', rsp_body)
            if packet_count >= 10:
                if len(conn.readbuf) > 0:
                    self._pending_read_conns.add(conn)
                    self._w_sock.send(b'1')
                break  # 收10个包强制跳出循环，避免长时间解包导致无法发送心跳

        if is_closed:
            if msg == '':
                self._do_close(conn.conn_id, CloseReason.RemoteClose, msg, True)
            else:
                self._do_close(conn.conn_id, CloseReason.ReadFail, msg, True)

        # logger.debug2(FTLog.ONLY_FILE, 'conn_id={}; elapsed={}; recv_len={}; buf_len={}; packet={};'.format(conn.conn_id, end_time-start_time, recv_len, buf_len, packet_count))

    def _on_write(self, conn: Connection):
        if conn.status == ConnStatus.Closed:
            return
        elif conn.status == ConnStatus.Connecting:
            err_code = conn.sock.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
            self._watch_read(conn, True)
            self._watch_write(conn, False)
            if err_code != 0:
                msg = errno.errorcode[err_code]
                self._do_close(conn.conn_id, CloseReason.ConnectFail, msg, False)
                conn.connect_info.set_result(ConnectErr.Fail, msg)
                if not conn.connect_info.is_sync:
                    conn.handler.on_connect(conn.conn_id, ConnectErr.Fail, msg)
            else:
                conn.status = ConnStatus.Connected
                conn.connect_info.set_result(ConnectErr.Ok, '')
                if not conn.connect_info.is_sync:
                    conn.handler.on_connect(conn.conn_id, ConnectErr.Ok, '')
            return

        msg = ''
        size = 0
        try:
            if len(conn.writebuf) > 0:
                size = conn.sock.send(conn.writebuf)
        except Exception as e:
            if not is_socket_exception_wouldblock(e):
                msg = str(e)

        if size > 0:
            del conn.writebuf[:size]

        if len(conn.writebuf) == 0:
            self._watch_write(conn, False)

        if msg:
            self._do_close(conn.conn_id, CloseReason.SendFail, msg, True)

    def _on_connect_timeout(self, conn: Connection):
        conn.connect_info.set_result(ConnectErr.Timeout, '')
        if not conn.connect_info.is_sync:
            conn.handler.on_connect(conn.conn_id, ConnectErr.Timeout, '')
        self._do_close(conn.conn_id, CloseReason.ConnectFail, '', False)

    def _on_packet(self, conn, head_dict, err: PacketErr, msg: str, rsp_body_data: bytes):
        proto_info = ProtoInfo(head_dict['proto_id'], head_dict['serial_no'])
        rsp_pb = None
        if err is PacketErr.Ok:
            ret_decrypt, msg_decrypt, rsp_body = decrypt_rsp_body(rsp_body_data, head_dict, conn.opend_conn_id, conn.is_encrypt)
            if ret_decrypt == RET_OK:
                rsp_pb = binary2pb(rsp_body, head_dict['proto_id'], head_dict['proto_fmt_type'])
            else:
                err = PacketErr.Invalid
                msg = msg_decrypt
                rsp_pb = None
        elif msg == '':
            msg = str(err)

        log_msg = 'Recv: conn_id={}; proto_id={}; serial_no={}; data_len={}; msg={};'.format(conn.conn_id,
                                                                                             proto_info.proto_id,
                                                                                             proto_info.serial_no,
                                                                                             len(
                                                                                                 rsp_body_data) if rsp_body_data else 0,
                                                                                             msg)
        if err is PacketErr.Ok:
            logger.debug2(FTLog.ONLY_FILE, log_msg)
        else:
            logger.warning(log_msg)

        send_info: SendInfo
        send_info = conn.send_info_dict.get(proto_info, None)
        conn.send_info_dict.pop(proto_info, None)
        if send_info:
            send_info.set_result(err, msg, rsp_pb)
            if not send_info.is_sync:
                conn.handler.on_packet(conn.conn_id, proto_info, err, msg, rsp_pb)
        elif ProtoId.is_proto_id_push(proto_info.proto_id):
            conn.handler.on_packet(conn.conn_id, proto_info, err, msg, rsp_pb)

    @staticmethod
    def extract_rsp_pb(opend_conn_id, head_dict, rsp_body):
        ret, msg, rsp = decrypt_rsp_body(rsp_body, head_dict, opend_conn_id)
        if ret == RET_OK:
            rsp_pb = binary2pb(rsp_body, head_dict['proto_id'], head_dict['proto_fmt_type'])
        else:
            rsp_pb = None
        return ret, msg, rsp_pb

    def set_conn_info(self, conn_id, info):
        with self._lock:
            conn = self._get_conn(conn_id)
            if conn is not None:
                conn.opend_conn_id = info.get('conn_id', conn.opend_conn_id)
                conn.keep_alive_interval = info.get('keep_alive_interval', conn.keep_alive_interval)
            else:
                return RET_ERROR, Err.ConnectionLost.text
        return RET_OK, ''
