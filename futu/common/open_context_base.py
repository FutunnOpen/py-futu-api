# -*- coding: utf-8 -*-

import time
from abc import ABCMeta, abstractmethod
from collections import namedtuple
from time import sleep
# from typing import Optional
from threading import Timer
from datetime import datetime
from threading import RLock, Thread
from futu.common.utils import *
from futu.common.handler_context import HandlerContext
from futu.quote.quote_query import InitConnect, TestCmd
from futu.quote.quote_query import GlobalStateQuery
from futu.quote.quote_query import KeepAlive, parse_head
from futu.common.conn_mng import FutuConnMng
from futu.common.network_manager import NetManager, PacketErr, ConnectErr, CloseReason
from .err import Err
from .constant import ContextStatus
from .callback_executor import CallbackExecutor, CallbackItem
from .ft_logger import *


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
        self._connect_err = None  # rsa加密失败时为Err.RsaErr, 否则为str
        self._proc_run = True
        self._sync_conn_id = 0
        self._conn_id = 0
        self._keep_alive_interval = 10
        self._last_keep_alive_time = datetime.now()
        self._reconnect_timer = None
        self._reconnect_interval = 8  # 重试连接的间隔
        self._sync_query_connect_timeout = None
        self._keep_alive_fail_count = 0
        self._last_recv_time = datetime.now()
        self._is_encrypt = is_encrypt
        if self.is_encrypt():
            assert SysConfig.INIT_RSA_FILE != '', Err.NotSetRSAFile.text
        self._net_mgr.start()

        if is_async_connect:
            self._wait_reconnect(0)
        else:
            while True:
                ret = self._init_connect_sync()
                if ret == RET_OK:
                    return
                else:
                    if self.status == ContextStatus.CLOSED:
                        return
                sleep(self._reconnect_interval)

    def get_login_user_id(self):
        """
        get login user id
        :return: user id(int64)
        """
        with self._lock:
            return FutuConnMng.get_conn_user_id(self._sync_conn_id)

    def __del__(self):
        self.close()
        
    def __enter__(self):
        return self

    def __exit__(self, t, v, tb):
        self.close()

    @property
    def status(self):
        with self._lock:
            return self._status

    @property
    def connect_err_msg(self):
        with self._lock:
            if self._connect_err is Err.RsaErr:
                return Err.RsaErr.text
            return self._connect_err

    @property
    def connect_err(self):
        return self._connect_err

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
    def close(self):
        """
        to call close old obj before loop create new, otherwise socket will encounter error 10053 or more!
        """
        self._close(False)

    @abstractmethod
    def on_api_socket_reconnected(self):
        """
        callback after reconnect ok
        """
        # logger.debug("on_api_socket_reconnected obj ID={}".format(id(self)))
        return RET_OK, ''

    def _close(self, is_passive):
        with self._lock:
            if self._status == ContextStatus.CLOSED:
                return
            self._status = ContextStatus.CLOSED
            net_mgr = self._net_mgr
            conn_id = self._conn_id
            self._conn_id = 0
            self._net_mgr = None
            self.stop()
            self._callback_executor.close()
            self._handler_ctx = None
            if self._reconnect_timer is not None:
                self._reconnect_timer.cancel()
                self._reconnect_timer = None
        if conn_id > 0 and not is_passive:
            net_mgr.close(conn_id)
        net_mgr.stop()

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
            return self._proc_run

    def _get_sync_query_processor(self, pack_func, unpack_func, is_create_socket=True):
        """
        synchronize the query processor
        :param pack_func: back
        :param unpack_func: unpack
        :return: sync_query_processor
        """

        def sync_query_processor(**kargs):
            """sync query processor"""
            start_time = datetime.now()
            while True:
                with self._lock:
                    if self._status == ContextStatus.READY:
                        net_mgr = self._net_mgr
                        conn_id = self._conn_id
                        break
                    elif self._status == ContextStatus.CLOSED:
                        return RET_ERROR, Err.ConnectionClosed.text, None

                    if self._sync_query_connect_timeout is not None:
                        elapsed_time = datetime.now() - start_time
                        if elapsed_time.total_seconds() >= self._sync_query_connect_timeout:
                            return RET_ERROR, 'Connect timeout', None
                sleep(0.02)

            try:
                ret_code, msg, req_str = pack_func(**kargs)
                if ret_code != RET_OK:
                    return ret_code, msg, None

                ret_code, send_result = net_mgr.send(conn_id, req_str, True)
                if ret_code != RET_OK:
                    msg = send_result.msg if send_result.msg != '' else str(send_result.err)
                    return ret_code, msg, None

                send_result.wait()
                if send_result.err is not PacketErr.Ok:
                    msg = send_result.msg if send_result.msg != '' else str(send_result.err)
                    return RET_ERROR, msg, None

                with self._lock:
                    self._last_recv_time = datetime.now()
                ret_code, msg, content = unpack_func(send_result.rsp)
                if ret_code != RET_OK:
                    return ret_code, msg, None
            except Exception as e:
                logger.error(traceback.format_exc())
                return RET_ERROR, str(e), None

            return RET_OK, msg, content

        return sync_query_processor

    def _send_async_req(self, req_str):
        conn_id = 0
        net_mgr = None
        with self._lock:
            if self._status != ContextStatus.READY:
                return RET_ERROR, 'Context closed or not ready'
            conn_id = self._conn_id
            net_mgr = self._net_mgr
        return net_mgr.send(conn_id, req_str)

    def _init_connect_sync(self):
        with self._lock:
            if self._status == ContextStatus.START:
                self._status = ContextStatus.CONNECTING
            elif self._status == ContextStatus.READY:
                return RET_OK
            elif self._status != ContextStatus.CONNECTING:
                return RET_ERROR

        ret = self._connect_sync()
        if ret != RET_OK:
            return ret

        ret = self._send_init_connect_sync()
        if ret != RET_OK:
            return ret
        self.on_api_socket_reconnected()
        return RET_OK

    def _connect_sync(self):
        with self._lock:
            # logger.info("Start connecting: host={}; port={};".format(self.__host, self.__port))
            self._status = ContextStatus.CONNECTING
            ret, result = self._net_mgr.connect((self.__host, self.__port), self, 5, self.is_encrypt(), is_sync=True)
            if ret == RET_OK:
                self._conn_id = result.conn_id

        result.wait()
        if result.err is ConnectErr.Ok:
            # logger.info('Connected : conn_id={0}; '.format(self._conn_id))
            return RET_OK
        else:
            msg = result.msg if result.msg != '' else str(result.err)
            logger.warning('Connect fail: conn_id={}; msg={}'.format(result.conn_id, msg))
        return RET_ERROR

    def _send_init_connect_sync(self):
        kargs = {
            'client_ver': int(SysConfig.get_client_ver()),
            'client_id': str(SysConfig.get_client_id()),
            'recv_notify': True,
            'is_encrypt': self.is_encrypt(),
            'push_proto_fmt': SysConfig.get_proto_fmt()
        }

        ret, msg, req_str = InitConnect.pack_req(**kargs)
        if ret == RET_OK:
            _, send_result = self._net_mgr.send(self._conn_id, req_str, True)
        else:
            logger.error('Fail to pack InitConnect')
            return ret

        send_result.wait()
        if send_result.err is PacketErr.Ok:
            ret, msg, conn_info = self._handle_init_connect_rsp(send_result.rsp)
            if ret == RET_OK:
                # logger.info('InitConnect ok: {}'.format(conn_info))
                logger.info('InitConnect ok: conn_id={}, host={}, port={}, user_id={}'.format(self._conn_id, self.__host, self.__port, conn_info['login_user_id']))
                return RET_OK

        if msg == '':
            msg = send_result.msg if send_result.msg != '' else str(send_result.err)
        logger.warning('InitConnect fail: {}'.format(msg))
        return RET_ERROR

    def get_sync_conn_id(self):
        with self._lock:
            return self._sync_conn_id

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
            logger.info('Disconnected: conn_id={0}'.format(conn_id))
            return
        else:
            logger.warning('Disconnected: conn_id={0} reason={1} msg={2}'.format(conn_id, str(reason), msg))

        with self._lock:
            if self._status == ContextStatus.CLOSED:
                return
            self._wait_reconnect()

    def on_packet(self, conn_id, proto_info, err, msg, rsp_pb):
        with self._lock:
            if self._status == ContextStatus.CLOSED or self._status == ContextStatus.START:
                return
            elif self._status == ContextStatus.CONNECTING and proto_info.proto_id != ProtoId.InitConnect:
                return

        if proto_info.proto_id == ProtoId.InitConnect:
            self._handle_init_connect(conn_id, proto_info.proto_id, err, msg, rsp_pb)
        elif proto_info.proto_id == ProtoId.KeepAlive:
            self._handle_keep_alive(conn_id, proto_info.proto_id, err, msg, rsp_pb)
        elif err is PacketErr.Ok:
            item = CallbackItem(self, proto_info.proto_id, rsp_pb)
            self._callback_executor.queue.put(item)
            with self._lock:
                self._last_recv_time = datetime.now()

    def on_tick(self, conn_id, now):
        with self._lock:
            if self._status != ContextStatus.READY:
                return
            time_elapsed = now - self._last_keep_alive_time
            if time_elapsed.total_seconds() < self._keep_alive_interval:
                return

            ret, msg, req = KeepAlive.pack_req(self.get_sync_conn_id())
            if ret != RET_OK:
                logger.warning("KeepAlive.pack_req fail: {0}".format(msg))
                return
            ret, result = self._net_mgr.send(conn_id, req, is_sync=False)
            if ret != RET_OK:
                return

            self._last_keep_alive_time = now

    def packet_callback(self, proto_id, rsp_pb):
        with self._lock:
            if self._status != ContextStatus.READY:
                return

            handler_ctx = self._handler_ctx
        if handler_ctx:
            handler_ctx.recv_func(rsp_pb, proto_id)

    def _handle_init_connect(self, conn_id, proto_info, ret, msg, rsp_pb):
        pass

    def _handle_init_connect_rsp(self, rsp):
        ret, msg, data = InitConnect.unpack_rsp(rsp)
        if ret != RET_OK:
            return ret, msg, None

        with self._lock:
            conn_info = copy(data)
            conn_info['is_encrypt'] = self.is_encrypt()
            self._sync_conn_id = conn_info['conn_id']
            self._keep_alive_interval = conn_info['keep_alive_interval'] * 4 / 5
            self._net_mgr.set_conn_info(self._conn_id, conn_info)
            now = datetime.now()
            self._last_keep_alive_time = now
            self._last_recv_time = now
            self._status = ContextStatus.READY
            FutuConnMng.add_conn(conn_info)
        return ret, '', conn_info

    def _handle_keep_alive(self, conn_id, proto_info, err, msg, rsp_pb):
        should_reconnect = False
        with self._lock:
            if err is PacketErr.Ok:
                self._keep_alive_fail_count = 0
            else:
                self._keep_alive_fail_count += 1

            now = datetime.now()

            if self._keep_alive_fail_count >= 3:
                if (now - self._last_recv_time).total_seconds() < self._keep_alive_interval:
                    self._keep_alive_fail_count = 0
                else:
                    logger.warning('Fail to recv KeepAlive for 3 times')
                    should_reconnect = True

        if should_reconnect:
            self._wait_reconnect()

    def _wait_reconnect(self, wait_reconnect_interval=8):
        with self._lock:
            if self._status == ContextStatus.CLOSED or self._reconnect_timer is not None:
                return
            logger.info('Wait reconnect in {} seconds: host={}; port={};'.format(wait_reconnect_interval,
                                                                                 self.__host,
                                                                                 self.__port))
            net_mgr = self._net_mgr
            conn_id = self._conn_id

            self._status = ContextStatus.CONNECTING
            self._sync_conn_id = 0
            self._conn_id = 0
            self._keep_alive_fail_count = 0
            self._reconnect_timer = Timer(wait_reconnect_interval, self._reconnect)
            self._reconnect_timer.start()

        net_mgr.close(conn_id)

    def _reconnect(self):
        with self._lock:
            self._reconnect_timer.cancel()
            self._reconnect_timer = None

        ret = self._init_connect_sync()
        if ret != RET_OK:
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
