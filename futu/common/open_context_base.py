# -*- coding: utf-8 -*-
import threading
import time
from abc import ABCMeta, abstractmethod
from collections import namedtuple
from time import sleep
# from typing import Optional
from threading import Timer
from datetime import datetime
from threading import RLock, Thread
from .utils import *
from .handler_context import HandlerContext
from ..quote.quote_query import InitConnect, TestCmd
from ..quote.quote_query import GlobalStateQuery
from ..quote.quote_query import KeepAlive, parse_head
from .conn_mng import FutuConnMng
from .network_manager import NetManager, PacketErr, ConnectErr, CloseReason, ConnectInfo
from .err import Err
from .constant import ContextStatus
from .callback_executor import CallbackExecutor, CallbackItem
from .ft_logger import *


class ReqInfo:
    def __init__(self, proto_id, serial_no, req_time, is_sync):
        self.req_time = req_time
        self.proto_id = proto_id
        self.serial_no = serial_no
        self.unpack_func = None
        self.err = PacketErr.Ok
        self.msg = ''
        self.rsp = None
        self.event = None
        if is_sync:
            self.event = threading.Event()

    @property
    def is_sync(self):
        return self.event is not None

    def set_result(self, err, msg, rsp):
        self.err = err
        self.msg = msg
        self.rsp = rsp

    def notify_finish(self):
        if self.is_sync:
            self.event.set()

    def wait(self):
        if self.is_sync:
            ret = self.event.wait(timeout=20)
            if not ret:
                self.err = PacketErr.Timeout
                self.msg = 'Abnormal event timeout'

class OpenContextBase(object):
    """Base class for set context"""
    metaclass__ = ABCMeta

    def __init__(self, host, port, is_encrypt=None, is_async_connect=False):
        self.__host = host
        self.__port = port
        self._callback_executor = CallbackExecutor()
        self._net_mgr = NetManager.default()
        self._handler_ctx = HandlerContext(self._is_proc_run)
        self._lock = RLock()
        self._status = ContextStatus.START
        self._proc_run = True
        self._opend_conn_id = 0
        self._conn_id = 0
        self._keep_alive_interval = 10
        self._last_keep_alive_time = time.time()
        self._last_recv_time = time.time()
        self._conn_alive_timeout = 33
        self._auto_reconnect = True
        self._reconnect_timer = None
        self._reconnect_interval = 6  # 重试连接的间隔
        self._sync_query_connect_timeout = None
        self._query_timeout = 12
        self._is_encrypt = is_encrypt
        self._req_map = {}
        self._recv_buf = bytearray()
        self._push_handler_time_warn = 2
        if self.is_encrypt():
            assert SysConfig.INIT_RSA_FILE != '', Err.NotSetRSAFile.text

        if is_async_connect:
            self._wait_reconnect(0)
        else:
            while True:
                self._status = ContextStatus.START
                ret = self._init_connect_sync()
                if ret == RET_OK:
                    return
                else:
                    if not self._auto_reconnect:
                        return
                sleep(self._reconnect_interval)

    def get_login_user_id(self):
        """
        get login user id
        :return: user id(int64)
        """
        with self._lock:
            return FutuConnMng.get_conn_user_id(self._opend_conn_id)

    def __del__(self):
        pass
        
    def __enter__(self):
        return self

    def __exit__(self, t, v, tb):
        self.close()

    @property
    def status(self):
        with self._lock:
            return self._status

    def conn_str(self):
        with self._lock:
            s = f'{self._opend_conn_id}({self._conn_id})'
        return s

    def set_sync_query_connect_timeout(self, timeout):
        with self._lock:
            self._sync_query_connect_timeout = timeout

    @property
    def reconnect_interval(self):
        with self._lock:
            return self._reconnect_interval

    @reconnect_interval.setter
    def reconnect_interval(self, value):
        with self._lock:
            self._reconnect_interval = value

    @abstractmethod
    def close(self, reason=CloseReason.Close):
        logger.info(f'call close: conn={self.conn_str()} reason={reason}')
        with self._lock:
            if reason is CloseReason.Close:
                self._auto_reconnect = False

            if self._status == ContextStatus.CLOSING or self._status == ContextStatus.CLOSED:
                return

            conn_id = self._conn_id
            self._clear()

            if self._status == ContextStatus.START or self._status == ContextStatus.WAIT_RECONNECT:
                self._close_callback_executor()
                self._status = ContextStatus.CLOSED
            elif self._status == ContextStatus.CONNECTED or self._status == ContextStatus.READY or self._status == ContextStatus.CONNECTING:
                self._status = ContextStatus.CLOSING
                self._net_mgr.close(conn_id, reason=reason)

    @abstractmethod
    def on_api_socket_reconnected(self):
        """
        callback after reconnect ok
        """
        # logger.debug("on_api_socket_reconnected obj ID={}".format(id(self)))
        return RET_OK, ''

    def on_connect(self, conn_id, conn_info: ConnectInfo):
        logger.debug(f'on_connect: self={id(self)} self.conn_id={self._conn_id} self.status={self._status} conn={conn_id} err={conn_info.err}')
        with self._lock:
            if self._status == ContextStatus.CONNECTING:
                if conn_info.err == ConnectErr.Ok:
                    self._status = ContextStatus.CONNECTED
                else:
                    self._status = ContextStatus.CLOSED
            elif self._status == ContextStatus.CLOSING:
                self._status = ContextStatus.CLOSED
                if conn_info.err == ConnectErr.Ok:
                    conn_info.err = ConnectErr.CallClose
            else:
                pass  #todo

        if conn_info.is_sync:
            conn_info.notify_finish()

    def _clear(self):
        FutuConnMng.remove_conn(self._opend_conn_id)
        self._opend_conn_id = 0
        if self._reconnect_timer is not None:
            self._reconnect_timer.cancel()
            self._reconnect_timer = None

    def _close_callback_executor(self):
        callback_executor = self._callback_executor
        if self._auto_reconnect:
            self._callback_executor = CallbackExecutor()
        if callback_executor:
            callback_executor.close()

    def start(self):
        """
        启动异步接收推送数据
        """
        with self._lock:
            self._proc_run = True

    def stop(self):
        """
        停止异步接收推送数据
        """
        with self._lock:
            self._proc_run = False

    def set_handler(self, handler):
        """
        设置异步回调处理对象

        :param handler: 回调处理对象，必须是以下类的子类实例

                    ===============================    =========================
                     类名                                 说明
                    ===============================    =========================
                    StockQuoteHandlerBase               报价处理基类
                    OrderBookHandlerBase                摆盘处理基类
                    CurKlineHandlerBase                 实时k线处理基类
                    TickerHandlerBase                   逐笔处理基类
                    RTDataHandlerBase                   分时数据处理基类
                    BrokerHandlerBase                   经济队列处理基类
                    PriceReminderHandlerBase            到价提醒处理基类
                    ===============================    =========================

        :return: RET_OK: 设置成功

                RET_ERROR: 设置失败
        """
        with self._lock:
            if self._handler_ctx is not None:
                return self._handler_ctx.set_handler(handler)
        return RET_ERROR

    def _is_proc_run(self):
        with self._lock:
            return self._proc_run  and self._status == ContextStatus.READY

    def _is_ready(self):
        with self._lock:
            return self._status == ContextStatus.READY

    def _get_sync_query_processor(self, pack_func, unpack_func):
        """
        synchronize the query processor
        :param pack_func: back
        :param unpack_func: unpack
        :return: sync_query_processor
        """

        def sync_query_processor(**kargs):
            """sync query processor"""
            start_time = datetime.now()
            try:
                ret_code, msg, req_str, proto_id, serial_no = pack_func(**kargs)
                if ret_code != RET_OK:
                    return ret_code, msg, None
            except Exception as ex:
                return RET_ERROR, str(ex), None

            while True:
                with self._lock:
                    if self.can_send_proto(proto_id):
                        net_mgr = self._net_mgr
                        conn_id = self._conn_id
                        proto_info = None
                        try:
                            proto_info = ProtoInfo(proto_id=proto_id, serial_no=serial_no)
                            req_info = ReqInfo(proto_id=proto_id, serial_no=serial_no, req_time=time.time(), is_sync=True)
                            req_info.unpack_func = unpack_func
                            self._req_map[proto_info] = req_info
                            ret_code, msg = net_mgr.send(conn_id, req_str)
                        except Exception as ex:
                            ret_code, msg = RET_ERROR, str(ex)

                        if ret_code != RET_OK:
                            if proto_info:
                                self._req_map.pop(proto_info, None)
                            return ret_code, msg, None
                        else:
                            logger.info(f'Send: conn={self.conn_str()} proto={proto_id} sn={serial_no}')
                        break
                    elif self._status == ContextStatus.CLOSED:
                        return RET_ERROR, Err.ConnectionClosed.text, None

                    if self._sync_query_connect_timeout is not None:
                        elapsed_time = datetime.now() - start_time
                        if elapsed_time.total_seconds() >= self._sync_query_connect_timeout:
                            return RET_ERROR, 'Connect timeout', None
                sleep(0.02)

            req_info.wait()
            if req_info.err is not PacketErr.Ok:
                msg = req_info.msg if req_info.msg != '' else str(req_info.err)
                return RET_ERROR, msg, None

            try:
                ret_code, msg, data = req_info.unpack_func(req_info.rsp)
            except Exception as ex:
                ret_code = RET_ERROR
                msg = str(ex)
                data = None

            return ret_code, msg, data

        return sync_query_processor

    def _query_sync(self, pack_func, unpack_func, **kargs):
        try:
            ret_code, msg, req_str, proto_id, serial_no = pack_func(**kargs)
            if ret_code != RET_OK:
                return ret_code, msg, None
        except Exception as ex:
            return RET_ERROR, str(ex), None

        with self._lock:
            if self.can_send_proto(proto_id):
                net_mgr = self._net_mgr
                conn_id = self._conn_id
                proto_info = None
                try:
                    proto_info = ProtoInfo(proto_id=proto_id, serial_no=serial_no)
                    req_info = ReqInfo(proto_id=proto_id, serial_no=serial_no, req_time=time.time(), is_sync=True)
                    req_info.unpack_func = unpack_func
                    self._req_map[proto_info] = req_info
                    ret_code, msg = net_mgr.send(conn_id, req_str)
                except Exception as ex:
                    ret_code, msg = RET_ERROR, str(ex)

                if ret_code != RET_OK:
                    if proto_info:
                        self._req_map.pop(proto_info)
                    return ret_code, msg, None
                else:
                    logger.info(f'Send: conn={self.conn_str()} proto={proto_id} sn={serial_no}')
            else:
                return RET_ERROR, 'Context status bad', None

        req_info.wait()
        if req_info.err is not PacketErr.Ok:
            msg = req_info.msg if req_info.msg != '' else str(req_info.err)
            return RET_ERROR, msg, None
        try:
            ret_code, msg, data = req_info.unpack_func(req_info.rsp)
        except Exception as ex:
            ret_code = RET_ERROR
            msg = str(ex)
            data = None

        return ret_code, msg, data

    def _query_async(self, pack_func, unpack_func, **kargs):
        try:
            ret_code, msg, req_str, proto_id, serial_no = pack_func(**kargs)
            if ret_code != RET_OK:
                return ret_code, msg
        except Exception as ex:
            return RET_ERROR, str(ex)

        with self._lock:
            if self.can_send_proto(proto_id):
                net_mgr = self._net_mgr
                conn_id = self._conn_id
                proto_info = None
                try:
                    proto_info = ProtoInfo(proto_id=proto_id, serial_no=serial_no)
                    req_info = ReqInfo(proto_id=proto_id, serial_no=serial_no, req_time=time.time(), is_sync=False)
                    req_info.unpack_func = unpack_func
                    self._req_map[proto_info] = req_info
                    ret_code, msg = net_mgr.send(conn_id, req_str)
                except Exception as ex:
                    ret_code, msg = RET_ERROR, str(ex)

                if ret_code != RET_OK:
                    if proto_info is not None:
                        self._req_map.pop(proto_info, None)
                    return ret_code, msg
                else:
                    logger.info(f'Send: conn={self.conn_str()} proto={proto_id} sn={serial_no}')
            else:
                return RET_ERROR, 'Context status bad'

        return RET_OK, ''

    def _init_connect_sync(self):
        with self._lock:
            if self._status == ContextStatus.READY:
                return RET_OK
            if self._status != ContextStatus.START:
                return RET_ERROR

        ret = self._connect_sync()
        if ret != RET_OK:
            return ret

        ret, msg = self._send_init_connect_sync()
        if ret != RET_OK:
            logger.warning2(FTLog.BOTH_FILE_CONSOLE, f'init connect fail: conn={self.conn_str()} msg={msg} context={self}')
            return ret

        logger.info2(FTLog.BOTH_FILE_CONSOLE, f'New connect ready: conn={self.conn_str()} context={self}')
        ret, msg = self.on_api_socket_reconnected()
        if ret != RET_OK:
            logger.warning(f'on_api_socket_reconnected fail: msg={msg}')
        return RET_OK

    def _connect_sync(self):
        with self._lock:
            if self._status == ContextStatus.START:
                self._status = ContextStatus.CONNECTING
            elif self._status == ContextStatus.CONNECTED or self._status == ContextStatus.READY:
                return RET_OK
            else:
                logger.warning(f'Not connect: status={self._status}')
                return RET_ERROR
            ret, result = self._net_mgr.connect((self.__host, self.__port), self, 20, self.is_encrypt(), is_sync=True)
            if ret == RET_OK:
                self._conn_id = result.conn_id
        logger.info(f'Start connect: self={id(self)} ret={ret} conn={result.conn_id}')
        result.wait()
        if result.err is ConnectErr.Ok:
            logger.info('Connected : conn={0}; '.format(self._conn_id))
            return RET_OK
        else:
            msg = result.msg if result.msg != '' else str(result.err)
            logger.warning2(FTLog.BOTH_FILE_CONSOLE, 'Connect fail: conn={}; msg={}; context={}'.format(self.conn_str(), msg, self))
        return RET_ERROR

    def _send_init_connect_sync(self):
        kargs = {
            'client_ver': int(SysConfig.get_client_ver()),
            'client_id': str(SysConfig.get_client_id()),
            'recv_notify': True,
            'is_encrypt': self.is_encrypt(),
            'push_proto_fmt': SysConfig.get_proto_fmt()
        }

        ret, msg, rsp = self._query_sync(InitConnect.pack_req, InitConnect.unpack_rsp, **kargs)
        if ret == RET_OK:
            self._handle_init_connect_rsp(rsp)
        return ret, msg

    def get_sync_conn_id(self):
        with self._lock:
            return self._opend_conn_id

    def get_async_conn_id(self):
        return self.get_sync_conn_id()

    def get_global_state(self):
        """
        获取全局状态

        :return: (ret, data)

                ret == RET_OK data为包含全局状态的字典，含义如下

                ret != RET_OK data为错误描述字符串

                =====================   ===========   ==============================================================
                key                      value类型                        说明
                =====================   ===========   ==============================================================
                market_sz               str            深圳市场状态，参见MarketState
                market_us               str            美国市场状态，参见MarketState
                market_sh               str            上海市场状态，参见MarketState
                market_hk               str            香港市场状态，参见MarketState
                market_hkfuture         str            香港期货市场状态，参见MarketState
                market_usfuture         str            美国期货市场状态，参见MarketState
                market_sgfuture         str            新加坡期货市场状态，参见MarketState
                market_jpfuture         str            日本期货市场状态，参见MarketState
                server_ver              str            FutuOpenD版本号
                trd_logined             str            '1'：已登录交易服务器，'0': 未登录交易服务器
                qot_logined             str            '1'：已登录行情服务器，'0': 未登录行情服务器
                timestamp               str            Futu后台服务器当前时间戳(秒)
                local_timestamp         double         FutuOpenD运行机器当前时间戳(
                =====================   ===========   ==============================================================
        :example:

        .. code:: python

        from futu import *
        quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
        print(quote_ctx.get_global_state())
        quote_ctx.close()
        """
        query_processor = self._get_sync_query_processor(
            GlobalStateQuery.pack_req, GlobalStateQuery.unpack_rsp)

        kargs = {
            'user_id': self.get_login_user_id(),
            'conn_id': self.get_sync_conn_id(),
        }
        ret_code, msg, state_dict = query_processor(**kargs)
        if ret_code != RET_OK:
            return ret_code, msg

        return RET_OK, state_dict

    def is_encrypt(self):
        with self._lock:
            if self._is_encrypt is None:
                return SysConfig.is_proto_encrypt()
            return self._is_encrypt

    def on_disconnect(self, conn_id, reason, msg):
        if reason is CloseReason.Close:
            logger.info(f'Disconnected: conn={self.conn_str()} reason=CallClose')
            logger.info2(FTLog.ONLY_CONSOLE, f'Disconnected: conn={self.conn_str()} reason=CallClose')
        else:
            logger.warning(f'Disconnected: conn={self.conn_str()} reason={reason} msg={msg}')
            logger.info2(FTLog.ONLY_CONSOLE, f'Disconnected: conn={self.conn_str()} reason={reason.name} msg={msg}')

        with self._lock:
            self._status = ContextStatus.CLOSED
            self._close_callback_executor()
            self._pop_all_req_info(PacketErr.Disconnect)
            self._clear()
            if self._auto_reconnect:
                self._wait_reconnect()

    def handle_push(self, conn_id, proto_id, serial_no, rsp_pb, err, msg):
        if err is PacketErr.Ok:
            item = CallbackItem(self, proto_id=proto_id, serial_no=serial_no, rsp_pb=rsp_pb)
            self._callback_executor.queue.put(item)

    def handle_packet(self, conn_id, proto_id, serial_no, rsp_pb, err, msg):
        if proto_id == ProtoId.KeepAlive:
            pass
        elif err is PacketErr.Ok:
            pass  #todo
            # item = CallbackItem(self, proto_id=proto_id, rsp_pb=rsp_pb)
            # self._callback_executor.queue.put(item)

    def _handle_recv(self):
        while True:
            result = parse_rsp(self._recv_buf, self._opend_conn_id, self.is_encrypt())
            if result.err == ParseRspErr.NOT_ENOUGH_DATA:
                return

            del self._recv_buf[:result.total_len]

            self._last_recv_time = time.time()
            err = PacketErr.Ok
            if result.err != ParseRspErr.OK:
                err = PacketErr.Invalid
            proto_id = result.head_dict['proto_id']
            serial_no = result.head_dict['serial_no']
            is_push = ProtoId.is_proto_id_push(proto_id)

            if is_push:
                logger.debug(
                    f'Push: conn={self.conn_str()} proto={proto_id} sn={serial_no} err={err.name}')
                self.handle_push(conn_id=self._conn_id, proto_id=proto_id, serial_no=serial_no, rsp_pb=result.rsp_pb, err=err, msg=result.msg)
            else:
                logger.info(
                    f'Recv: conn={self.conn_str()} proto={proto_id} sn={serial_no} err={err.name}')
                proto_info = ProtoInfo(proto_id=proto_id, serial_no=serial_no)
                req_info: ReqInfo
                req_info = self._req_map.pop(proto_info, None)
                if req_info:
                    if req_info.is_sync:
                        req_info.err = err
                        req_info.msg = result.msg
                        req_info.rsp = result.rsp_pb
                        req_info.notify_finish()
                    else:
                        self.handle_packet(conn_id=self._conn_id, proto_id=proto_id, serial_no=serial_no, rsp_pb=result.rsp_pb, err=err, msg=result.msg)
                else:
                    logger.warning(f'Reqinfo not found for recv package: conn={self.conn_str()} proto={proto_id} sn={serial_no}')
                    pass  #todo

    def on_recv(self, conn_id, data):
        with self._lock:
            if self._status != ContextStatus.CONNECTED and self._status != ContextStatus.READY:
                return
            if conn_id != self._conn_id:
                return
            self._recv_buf.extend(data)
            self._handle_recv()

    def on_tick(self, conn_id, now: float):
        with self._lock:
            if self._status != ContextStatus.READY:
                return

            if now - self._last_recv_time >= self._conn_alive_timeout:
                logger.warning(f'Long time not recv: conn={self.conn_str()} last_recv_time={self._last_recv_time}')
                self.close(reason=CloseReason.KeepAliveFail)
                return

            time_elapsed = now - self._last_keep_alive_time
            if time_elapsed >= self._keep_alive_interval:
                ret, msg = self.keep_alive()
                if ret != RET_OK:
                    logger.warning("KeepAlive fail: {0}".format(msg))
                else:
                    self._last_keep_alive_time = now

            self._check_req_timeout()

    def keep_alive(self):
        kargs = {'conn_id': self._opend_conn_id}
        ret, msg = self._query_async(KeepAlive.pack_req, KeepAlive.unpack_rsp, **kargs)
        return  ret, msg

    def _check_req_timeout(self):
        timeout_list = []
        now = time.time()
        proto_info: ProtoInfo
        req_info: ReqInfo
        for proto_info, req_info in self._req_map.items():
            elapsed = now - req_info.req_time
            if elapsed >= self._query_timeout:
                timeout_list.append(proto_info)
                req_info.err = PacketErr.Timeout
                req_info.msg = str(PacketErr.Timeout)
                logger.warning(f'Recv: conn={self.conn_str()} proto={req_info.proto_id} sn={req_info.serial_no} err=timeout')
                if req_info.is_sync:
                    req_info.notify_finish()

        for conn_info in timeout_list:
            self._req_map.pop(conn_info)

    def packet_callback(self, proto_id, serial_no, rsp_pb):
        with self._lock:
            if self._status != ContextStatus.READY:
                return

            handler_ctx = self._handler_ctx
        if handler_ctx:
            begin_time = time.time()
            end_time = begin_time
            try:
                logger.debug(f'Push callback: conn={self.conn_str()} proto={proto_id} sn={serial_no}')
                handler_ctx.recv_func(rsp_pb, proto_id)
                end_time = time.time()
            except Exception:
                logger.warning(f'Exception in push callback: conn={self.conn_str()} proto={proto_id} sn={serial_no}', exc_info=True)

            if end_time - begin_time >= self._push_handler_time_warn:
                logger.warning(f'Push callback use too much time: conn={self.conn_str()} proto={proto_id} sn={serial_no} time={end_time-begin_time}')

    def can_send_proto(self, proto_id):
        with self._lock:
            if proto_id == ProtoId.InitConnect:
                if self._status == ContextStatus.CONNECTED:
                    return True
            else:
                if self._status == ContextStatus.READY:
                    return True
            return False

    def _pop_all_req_info(self, err: PacketErr):
        with self._lock:
            for conn_id, req_info in self._req_map.items():
                req_info.err = err
                req_info.msg = err.name
                if req_info.is_sync:
                    req_info.notify_finish()
            self._req_map.clear()

    def _handle_init_connect_rsp(self, data):
        with self._lock:
            conn_info = copy(data)
            conn_info['is_encrypt'] = self.is_encrypt()
            self._opend_conn_id = conn_info['conn_id']
            self._keep_alive_interval = conn_info['keep_alive_interval'] * 4 / 5
            now = time.time()
            self._last_keep_alive_time = now
            self._last_recv_time = now
            self._status = ContextStatus.READY
            FutuConnMng.add_conn(conn_info)
        return conn_info

    def _wait_reconnect(self, wait_reconnect_interval=6):
        with (self._lock):
            if not self._auto_reconnect:
                logger.warning(f'Not reconnect: auto reconnect off')
                return
            if self._status == ContextStatus.CONNECTED or self._status == ContextStatus.CONNECTING or \
                self._status == ContextStatus.CLOSING or self._reconnect_timer is not None:
                logger.warning(f'Not reconnect: status={self._status}')
                return

            logger.info('Wait reconnect in {} seconds: host={}; port={};'.format(wait_reconnect_interval,
                                                                                 self.__host,
                                                                                 self.__port))
            self._status = ContextStatus.WAIT_RECONNECT
            self._opend_conn_id = 0
            self._conn_id = 0
            self._reconnect_timer = Timer(wait_reconnect_interval, self._reconnect)
            self._reconnect_timer.start()

    def _reconnect(self):
        with self._lock:
            self._reconnect_timer.cancel()
            self._reconnect_timer = None

            if not self._auto_reconnect:
                logger.info(f'cancel reconnect, auto_reconnect is false: self={id(self)}')
                return
            else:
                logger.info(f'start reconnect: self={id(self)}')
            self._status = ContextStatus.START

        ret = RET_ERROR
        try:
            ret = self._init_connect_sync()
        except Exception as ex:
            pass

        if ret != RET_OK:
            with self._lock:
                self._net_mgr.close(self._conn_id, reason=CloseReason.CloseNoNotify)
                self._close_callback_executor()
                self._pop_all_req_info(PacketErr.Disconnect)
                self._clear()
                if self._auto_reconnect:
                    self._wait_reconnect(self._reconnect_interval)

    def test_cmd(self, cmd, params):
        query_processor = self._get_sync_query_processor(
            TestCmd.pack_req, TestCmd.unpack_rsp)

        kargs = {
            'cmd': cmd,
            'params': params,
        }
        ret_code, msg, state_dict = query_processor(**kargs)
        if ret_code != RET_OK:
            return ret_code, msg

        return RET_OK, state_dict
