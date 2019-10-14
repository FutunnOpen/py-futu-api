import errno
import datetime
import threading
from time import sleep
from futu.common.utils import *
from futu.quote.quote_query import parse_head
from .err import Err
from .sys_config import SysConfig
from .ft_logger import *

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


class SyncReqRspInfo:
    def __init__(self):
        self.event = threading.Event()
        self.ret = RET_OK
        self.msg = ''
        self.data = None


class Connection:
    def __init__(self, conn_id, sock, addr, handler, is_encrypt):
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
        self.start_time = None
        self.readbuf = bytearray()
        self.writebuf = bytearray()
        self.req_dict = {}  # ProtoInfo -> req time
        self.sync_req_dict = {}  # ProtoInfo -> SyncReqRspInfo

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

    def connect(self, addr, handler, timeout, is_encrypt):
        with self._lock:
            conn_id = self._next_conn_id
            self._next_conn_id += 1

        def work():
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024 * 1024)
            conn = Connection(conn_id, sock, addr, handler, is_encrypt)
            conn.status = ConnStatus.Connecting
            conn.start_time = datetime.now()
            conn.timeout = timeout
            sock.setblocking(False)
            self._selector.register(sock, selectors.EVENT_READ | selectors.EVENT_WRITE, conn)

            try:
                sock.connect(addr)
            except Exception as e:
                if not is_socket_exception_wouldblock(e):
                    conn.handler.on_error(conn.conn_id, str(e))
                    self.close(conn.conn_id)
                    return RET_ERROR, str(e), 0

            return RET_OK, '', conn_id

        self._req_queue.put(work)
        self._w_sock.send(b'1')
        return RET_OK, '', conn_id

    def poll(self):
        now = datetime.now()
        events = self._selector.select(0.02)
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
                        conn.handler.on_activate(conn.conn_id, now)
                    if is_check_req:
                        self._check_req(conn, now)

        if is_activate:
            self._last_activate_time = now
        if is_check_req:
            self._last_check_req_time = now

    def _check_connect_timeout(self, conn, now):
        time_delta = now - conn.start_time
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
        req_dict = dict(conn.req_dict.items())
        for proto_info, req_time in req_dict.items():  # type: ProtoInfo, datetime
            elapsed_time = now - req_time
            if elapsed_time.total_seconds() >= self._sync_req_timeout:
                self._on_packet(conn, proto_info._asdict(), Err.Timeout.code, Err.Timeout.text, None)

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

    def do_send(self, conn_id, proto_info, data):
        logger.debug2(FTLog.ONLY_FILE, 'Send: conn_id={}; proto_id={}; serial_no={}; total_len={};'.format(conn_id, proto_info.proto_id,
                                                                                         proto_info.serial_no,
                                                                                         len(data)))
        now = datetime.now()
        ret_code = RET_OK
        msg = ''
        conn = self._get_conn(conn_id)  # type: Connection
        sync_req_rsp = None
        if not conn:
            logger.debug(
                FTLog.make_log_msg('Send fail', conn_id=conn_id, proto_id=proto_info.proto_id, serial_no=proto_info.serial_no,
                             msg=Err.ConnectionLost.text))
            ret_code, msg = RET_ERROR, Err.ConnectionLost.text
        else:
            sync_req_rsp = conn.sync_req_dict.get(proto_info, None)

        if ret_code != RET_OK:
            return ret_code, msg

        if conn.status != ConnStatus.Connected:
            ret_code, msg = RET_ERROR, Err.NotConnected.text

        if ret_code != RET_OK:
            logger.warning(FTLog.make_log_msg('Send fail', proto_id=proto_info.proto_id, serial_no=proto_info.serial_no,
                                        conn_id=conn_id, msg=msg))
            if sync_req_rsp:
                sync_req_rsp.ret, sync_req_rsp.msg = RET_ERROR, msg
                sync_req_rsp.event.set()

            return ret_code, msg

        conn.req_dict[proto_info] = now
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

        if size > 0 and size < len(data):
            conn.writebuf.extend(data[size:])
            self._watch_write(conn, True)

        if ret_code != RET_OK:
            logger.warning(FTLog.make_log_msg('Send error', conn_id=conn_id, msg=msg))
            if sync_req_rsp:
                sync_req_rsp.ret, sync_req_rsp.msg = RET_ERROR, msg
                sync_req_rsp.event.set()
            return ret_code, msg

        return RET_OK, ''

    def send(self, conn_id, data):
        """

        :param conn_id:
        :param data:
        :return:
        """
        proto_info = self._parse_req_head_proto_info(data)

        def work():
            self.do_send(conn_id, proto_info, data)

        self._req_queue.put(work)
        self._w_sock.send(b'1')
        return RET_OK, None

    def close(self, conn_id):
        def work():
            conn = self._get_conn(conn_id)  # type: Connection
            if not conn:
                return
            if conn.sock is None:
                return
            self._watch_read(conn, False)
            self._watch_write(conn, False)
            conn.sock.close()
            conn.sock = None
            conn.status = ConnStatus.Closed
            for proto_info, sync_req_rsp in conn.sync_req_dict.items():  # type: ProtoInfo, SyncReqRspInfo
                sync_req_rsp.ret = RET_ERROR
                sync_req_rsp.msg = Err.ConnectionClosed.text
                sync_req_rsp.event.set()
            logger.info("Close: conn_id={}".format(conn_id))

        self._req_queue.put(work)
        self._w_sock.send(b'1')

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

    def _parse_req_head_proto_info(selfs, req_str):
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
        start_time = time.time()
        recv_len = 0
        buf_len = 0
        packet_count = 0

        if conn.status == ConnStatus.Closed:
            return

        err = None
        is_closed = False
        try:
            data = conn.sock.recv(128 * 1024)
            if data == b'':
                is_closed = True
            else:
                conn.readbuf.extend(data)
                recv_len = len(data)
                buf_len = len(conn.readbuf)

        except Exception as e:
            if not is_socket_exception_wouldblock(e):
                err = str(e)

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
            self._on_packet(conn, head_dict, Err.Ok.code, '', rsp_body)

        if is_closed:
            self.close(conn.conn_id)
            conn.handler.on_error(conn.conn_id, Err.ConnectionClosed.text)
        elif err:
            self.close(conn.conn_id)
            conn.handler.on_error(conn.conn_id, err)
        # end_time = time.time()
        # logger.debug2(FTLog.ONLY_FILE, 'conn_id={}; elapsed={}; recv_len={}; buf_len={}; packet={};'.format(conn.conn_id, end_time-start_time, recv_len, buf_len, packet_count))

    def _on_write(self, conn):
        if conn.status == ConnStatus.Closed:
            return
        elif conn.status == ConnStatus.Connecting:
            err = conn.sock.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
            self._watch_write(conn, False)
            if err != 0:
                conn.handler.on_error(conn.conn_id, errno.errorcode[err])
            else:
                conn.status = ConnStatus.Connected
                conn.handler.on_connected(conn.conn_id)
            return

        err = None

        size = 0
        try:
            if len(conn.writebuf) > 0:
                size = conn.sock.send(conn.writebuf)
        except Exception as e:
            if not is_socket_exception_wouldblock(e):
                err = str(e)

        if size > 0:
            del conn.writebuf[:size]

        if len(conn.writebuf) == 0:
            self._watch_write(conn, False)

        if err:
            self.close(conn.conn_id)
            conn.handler.on_error(conn.conn_id, err)

    def _on_connect_timeout(self, conn):
        conn.handler.on_connect_timeout(conn.conn_id)

    def _on_packet(self, conn, head_dict, err_code, msg, rsp_body_data):
        """

        :param conn:
        :type conn: Connection
        :param head_dict:
        :param err_code:
        :param msg:
        :param rsp_body_data:
        :return:
        """
        proto_info = ProtoInfo(head_dict['proto_id'], head_dict['serial_no'])
        rsp_pb = None
        if err_code == Err.Ok.code:
            ret_decrypt, msg_decrypt, rsp_body = decrypt_rsp_body(rsp_body_data, head_dict, conn.opend_conn_id, conn.is_encrypt)
            if ret_decrypt == RET_OK:
                rsp_pb = binary2pb(rsp_body, head_dict['proto_id'], head_dict['proto_fmt_type'])
            else:
                err_code = Err.PacketDataErr.code
                msg = msg_decrypt
                rsp_pb = None

        log_msg = 'Recv: conn_id={}; proto_id={}; serial_no={}; data_len={}; msg={};'.format(conn.conn_id,
                                                                                             proto_info.proto_id,
                                                                                             proto_info.serial_no,
                                                                                             len(
                                                                                                 rsp_body_data) if rsp_body_data else 0,
                                                                                             msg)
        if err_code == Err.Ok.code:
            logger.debug2(FTLog.ONLY_FILE, log_msg)
        else:
            logger.warning(log_msg)

        ret_code = RET_OK if err_code == Err.Ok.code else RET_ERROR
        sync_rsp_info = conn.sync_req_dict.get(proto_info, None)  # type: SyncReqRspInfo
        conn.req_dict.pop(proto_info, None)
        if sync_rsp_info:
            sync_rsp_info.ret, sync_rsp_info.msg, sync_rsp_info.data = ret_code, msg, rsp_pb
            sync_rsp_info.event.set()
            conn.sync_req_dict.pop(proto_info)
        else:
            conn.handler.on_packet(conn.conn_id, proto_info, ret_code, msg, rsp_pb)

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
