import errno
import datetime
import threading
import time
from time import sleep
from .utils import *
from ..quote.quote_query import parse_head
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
    CallClose = 3


class CloseReason(enum.Enum):
    Close = 0
    RemoteClose = 1
    ReadFail = 2
    SendFail = 3
    ConnectFail = 4
    KeepAliveFail = 5
    CloseNoNotify = 6


class PacketErr(enum.Enum):
    Ok = 0
    Timeout = 1
    Invalid = 2
    Disconnect = 3
    SendFail = 4


class ConnectInfo:
    def __init__(self, is_sync):
        self.start_time = None
        self.conn_id = 0
        self.err = ConnectErr.Ok
        self.msg = ''
        self.event = None
        if is_sync:
            self.event = threading.Event()

    @property
    def is_sync(self):
        return self.event is not None

    def set_result(self, err, msg):
        self.err = err
        self.msg = msg

    def notify_finish(self):
        if self.is_sync:
            self.event.set()

    def wait(self):
        if self.is_sync:
            ret = self.event.wait()
            if not ret:
                self.err = ConnectErr.Timeout
                self.msg = 'Abnormal event timeout'


class Connection:
    def __init__(self, conn_id, sock, addr, handler, is_encrypt, is_sync):
        self._conn_id = conn_id
        self.opend_conn_id = 0
        self.sock: socket.socket = sock
        self.is_encrypt = is_encrypt
        self.handler = handler
        self._peer_addr = addr
        self.status = ConnStatus.Start
        self.keep_alive_interval = 10
        self.last_keep_alive_time = time.time()
        self.timeout = 10
        self.writebuf = bytearray()
        self.connect_info = ConnectInfo(is_sync)
        self.connect_info.conn_id = conn_id

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
        self._conn_map = {}  # conn_id: Connection
        self._sync_req_timeout = 12
        now = time.time()
        self._last_check_time = now
        self._last_tick_time = now
        self._r_sock, self._w_sock = make_ctrl_socks()
        self._selector = selectors.DefaultSelector()
        self._selector.register(self._r_sock, selectors.EVENT_READ)
        self._req_queue = queue.Queue()
        self._thread = threading.Thread(target=self._loop)
        self._thread.setDaemon(True)
        self._thread.start()

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

        def do_connect():
            self._conn_map[conn_id] = conn
            conn.connect_info.start_time = time.time()
            try:
                self._selector.register(sock, selectors.EVENT_WRITE, conn)
                sock.connect(addr)
                conn.status = ConnStatus.Connected
                self._watch_read(conn, is_watch=True)
                self._watch_write(conn, is_watch=False)
                conn.connect_info.set_result(ConnectErr.Ok, msg='')
                try:
                    conn.handler.on_connect(conn.connect_info)
                except Exception as ex:
                    logger.warning(f'Callback on_connect error: conn={conn_id}', exc_info=True)
            except Exception as e:
                if not is_socket_exception_wouldblock(e):
                    logger.warning(f'Connect exception: conn={conn_id}', exc_info=True)
                    self._do_close(conn.conn_id, CloseReason.ConnectFail, str(e), False)
                    conn.connect_info.set_result(ConnectErr.Fail, str(e))
                    try:
                        conn.handler.on_connect(conn.connect_info)
                    except Exception as ex:
                        logger.warning(f'Callback on_connect error: conn={conn_id}', exc_info=True)

        self._req_queue.put(do_connect)
        self._w_sock.send(b'1')

        return RET_OK, conn.connect_info

    def poll(self):
        events = self._selector.select(0.1)
        now = time.time()
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
            conn: Connection = key.data
            if evt_mask & selectors.EVENT_WRITE != 0:
                self._on_write(conn)
            if evt_mask & selectors.EVENT_READ != 0:
                self._on_read(conn)

        if now - self._last_check_time >= 0.1:
            self._check_connect_timeout(now)
            self._last_check_time = now
        if now - self._last_tick_time >= 1:
            self._tick(now)
            self._last_tick_time = now

    def _check_connect_timeout(self, now):
        errs = []
        conn: Connection
        for conn_id, conn in self._conn_map.items():
            if conn.status == ConnStatus.Connecting:
                if now - conn.connect_info.start_time >= conn.timeout:
                    conn.connect_info.set_result(ConnectErr.Timeout, 'Timeout')
                    errs.append(conn)

        for conn in errs:
            self._selector.unregister(conn.sock)
            conn.sock.close()
            conn.sock = None
            conn.status = ConnStatus.Closed
            self._conn_map.pop(conn.conn_id, None)
            try:
                conn.handler.on_connect(conn.conn_id, conn_info=conn.connect_info)
            except Exception as ex:
                logger.warning(f'Callback on_connect error: conn={conn.conn_id}', exc_info=True)

    def _tick(self, now):
        for conn_id, conn in self._conn_map.items():
            if conn.status == ConnStatus.Connected:
                try:
                    conn.handler.on_tick(conn_id, now)
                except Exception:
                    logger.warning(f'Callback on_tick error: conn={conn_id}', exc_info=True)

    def _loop(self):
        while True:
            self.poll()

    def do_send(self, conn_id, data):
        ret_code = RET_OK
        msg = ''
        conn = self._get_conn(conn_id)  # type: Connection
        if not conn:
            ret_code, msg = RET_ERROR, Err.ConnectionLost.text
        elif conn.status != ConnStatus.Connected:
            ret_code, msg = RET_ERROR, Err.NotConnected.text

        if ret_code != RET_OK:
            logger.warning(f'Send fail: conn={conn_id} msg=msg')
            return

        size = 0
        try:
            if len(conn.writebuf) == 0:
                size = conn.sock.send(data)
        except Exception as e:
            if not is_socket_exception_wouldblock(e):
                ret_code, msg = RET_ERROR, str(e)

        if size < len(data):
            conn.writebuf.extend(data[size:])
            self._watch_write(conn, True)

        if ret_code != RET_OK:
            logger.warning(f'Send fail: conn={conn_id} msg=msg')
            self._do_close(conn.conn_id, CloseReason.SendFail, msg, True)

        return ret_code, msg

    def send(self, conn_id, data):
        def work():
            self.do_send(conn_id, data)

        self._req_queue.put(work)
        self._w_sock.send(b'1')
        return RET_OK, ''

    def close(self, conn_id, reason=CloseReason.Close):
        if reason == CloseReason.CloseNoNotify:
            is_notify = False
        else:
            is_notify = True

        def work():
            self._do_close(conn_id, reason, '', notify=is_notify)

        self._req_queue.put(work)
        self._w_sock.send(b'1')

    def _do_close(self, conn_id, reason, msg, notify):
        conn = self._get_conn(conn_id)  # type: Connection
        if not conn:
            return

        logger.info(f"Close: conn={conn_id} reason={reason} msg={msg}")
        if conn.sock:
            self._selector.unregister(conn.sock)
            conn.sock.close()
            conn.sock = None
        conn.status = ConnStatus.Closed
        self._conn_map.pop(conn_id, None)
        if notify:
            try:
                conn.handler.on_disconnect(conn_id, reason, msg)
            except Exception:
                logger.warning(f'Callback on_disconnect error: conn={conn_id}', exc_info=True)

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


    def _get_conn(self, conn_id):
        return self._conn_map.get(conn_id, None)

    def _on_read(self, conn):
        if conn.status != ConnStatus.Connected:
            return

        data = b''
        msg = ''
        has_err = False
        try:
            data = conn.sock.recv(128 * 1024)
            if data == b'':
                has_err = True
        except Exception as e:
            if not is_socket_exception_wouldblock(e):
                has_err = True
                msg = str(e)

        if len(data) > 0:
            try:
                conn.handler.on_recv(conn.conn_id, data)
            except Exception:
                logger.warning(f'Callback on_recv error: conn={conn.conn_id}', exc_info=True)

        if has_err:
            if msg == '':
                self._do_close(conn.conn_id, CloseReason.RemoteClose, msg, True)
            else:
                self._do_close(conn.conn_id, CloseReason.ReadFail, msg, True)

    def _on_write(self, conn: Connection):
        if conn.status == ConnStatus.Closed:
            return
        elif conn.status == ConnStatus.Connecting:
            err_code = conn.sock.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)

            if err_code != 0:
                msg = errno.errorcode[err_code]
                self._do_close(conn.conn_id, CloseReason.ConnectFail, msg, False)
                conn.connect_info.set_result(ConnectErr.Fail, msg)
            else:
                self._watch_read(conn, True)
                self._watch_write(conn, False)
                conn.status = ConnStatus.Connected
                conn.connect_info.set_result(ConnectErr.Ok, '')

            try:
                conn.handler.on_connect(conn.conn_id, conn.connect_info)
            except Exception:
                logger.warning(f'Callback on_connect error: conn={conn.conn_id}', exc_info=True)

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

    @staticmethod
    def extract_rsp_pb(opend_conn_id, head_dict, rsp_body):
        ret, msg, rsp = decrypt_rsp_body(rsp_body, head_dict, opend_conn_id)
        if ret == RET_OK:
            rsp_pb = binary2pb(rsp_body, head_dict['proto_id'], head_dict['proto_fmt_type'])
        else:
            rsp_pb = None
        return ret, msg, rsp_pb
