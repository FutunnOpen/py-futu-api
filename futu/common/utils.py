# -*- coding: utf-8 -*-

import hashlib, json, os, sys, socket, traceback, time, struct, collections
from datetime import datetime, timedelta
from struct import calcsize
from google.protobuf.json_format import MessageToJson
from threading import RLock
from futu.common.conn_mng import *
from futu.common.sys_config import *
from futu.common.pbjson import json2pb


ProtoInfo = collections.namedtuple('ProtoInfo', ['proto_id', 'serial_no'])


def get_message_head_len():
    return calcsize(MESSAGE_HEAD_FMT)


def check_date_str_format(s, default_time="00:00:00"):
    """Check the format of date string"""
    try:
        str_fmt = s
        if ":" not in s:
            str_fmt = '{} {}'.format(s, default_time)

        dt_obj = datetime.strptime(str_fmt, "%Y-%m-%d %H:%M:%S")

        return RET_OK, dt_obj

    except ValueError:
        error_str = ERROR_STR_PREFIX + "wrong time or time format"
        return RET_ERROR, error_str


def normalize_date_format(date_str, default_time="00:00:00"):
    """normalize the format of data"""
    ret_code, ret_data = check_date_str_format(date_str, default_time)
    if ret_code != RET_OK:
        return ret_code, ret_data

    return RET_OK, ret_data.strftime("%Y-%m-%d %H:%M:%S")


def normalize_start_end_date(start, end, delta_days=0, default_time_start="00:00:00", default_time_end="23:59:59", prefer_end_now=True):
    """

    :param start:
    :param end:
    :param delta_days:
    :param default_time_start:
    :param default_time_end:
    :param prefer_end_now: 为True时，当start和end都为None时，end设为当前时间，为False则start设为当前时间
    :return:
    """
    if start is not None and is_str(start) is False:
        error_str = ERROR_STR_PREFIX + "the type of start param is wrong"
        return RET_ERROR, error_str, None, None

    if end is not None and is_str(end) is False:
        error_str = ERROR_STR_PREFIX + "the type of end param is wrong"
        return RET_ERROR, error_str, None, None

    dt_start = None
    dt_end = None
    delta = timedelta(days=delta_days)
    hour_end, min_end, sec_end = [int(x) for x in default_time_end.split(':')]
    hour_start, min_start, sec_start = [int(x) for x in default_time_start.split(':')]

    if start:
        ret_code, ret_data = check_date_str_format(start, default_time_start)
        if ret_code != RET_OK:
            return ret_code, ret_data, start, end
        dt_start = ret_data

    if end:
        ret_code, ret_data = check_date_str_format(end, default_time_end)
        if ret_code != RET_OK:
            return ret_code, ret_data, start, end
        dt_end = ret_data

    if end and not start:
        dt_tmp = dt_end - delta
        dt_start = datetime(year=dt_tmp.year, month=dt_tmp.month, day=dt_tmp.day, hour=hour_start, minute=min_start, second=sec_start)

    if start and not end:
        dt_tmp = dt_start + delta
        dt_end = datetime(year=dt_tmp.year, month=dt_tmp.month, day=dt_tmp.day, hour=hour_end, minute=min_end, second=sec_end)

    if not start and not end:
        if prefer_end_now:
            dt_now = datetime.now()
            dt_end = datetime(year=dt_now.year, month=dt_now.month, day=dt_now.day, hour=hour_end, minute=min_end, second=sec_end)
            dt_tmp = dt_end - delta
            dt_start = datetime(year=dt_tmp.year, month=dt_tmp.month, day=dt_tmp.day, hour=hour_start, minute=min_start, second=sec_start)
        else:
            dt_now = datetime.now()
            dt_start = datetime(year=dt_now.year, month=dt_now.month, day=dt_now.day, hour=hour_start, minute=min_start,
                              second=sec_start)
            dt_tmp = dt_start + delta
            dt_end = datetime(year=dt_tmp.year, month=dt_tmp.month, day=dt_tmp.day, hour=hour_end, minute=min_end,
                                second=sec_end)

    start = dt_start.strftime("%Y-%m-%d %H:%M:%S")
    end = dt_end.strftime("%Y-%m-%d %H:%M:%S")

    return RET_OK, '', start, end


def is_str(s):
    if IS_PY2:
        return isinstance(s, str) or isinstance(s, unicode)
    else:
        return isinstance(s, str)


def extract_pls_rsp(rsp_str):
    """Extract the response of PLS"""
    try:
        rsp = json.loads(rsp_str)
    except ValueError:
        traceback.print_exc()
        err = sys.exc_info()[1]
        err_str = ERROR_STR_PREFIX + str(err)
        return RET_ERROR, err_str, None

    error_code = int(rsp['retType'])

    if error_code != 1:
        error_str = ERROR_STR_PREFIX + rsp['retMsg']
        return RET_ERROR, error_str, None

    return RET_OK, "", rsp


def split_stock_str(stock_str_param):
    """split the stock string"""
    stock_str = str(stock_str_param)

    split_loc = stock_str.find(".")
    '''do not use the built-in split function in python.
    The built-in function cannot handle some stock strings correctly.
    for instance, US..DJI, where the dot . itself is a part of original code'''
    if 0 <= split_loc < len(stock_str) - 1 and Market.if_has_key(stock_str[0:split_loc]):
        market_str = stock_str[0:split_loc]
        _, market_code = Market.to_number(market_str)
        partial_stock_str = stock_str[split_loc + 1:]
        return RET_OK, (market_code, partial_stock_str)

    else:
        error_str = ERROR_STR_PREFIX + "format of code %s is wrong. (US.AAPL, HK.00700, SZ.000001)" % stock_str
        return RET_ERROR, error_str


def merge_qot_mkt_stock_str(qot_mkt, partial_stock_str):
    """
    Merge the string of stocks
    :param market: market code
    :param partial_stock_str: original stock code string. i.e. "AAPL","00700", "000001"
    :return: unified representation of a stock code. i.e. "US.AAPL", "HK.00700", "SZ.000001"

    """
    market_str = Market.to_string2(qot_mkt)
    stock_str = '.'.join([market_str, partial_stock_str])
    return stock_str


def merge_trd_mkt_stock_str(trd_sec_mkt, partial_stock_str):
    """
    Merge the string of stocks
    :param market: market code
    :param partial_stock_str: original stock code string. i.e. "AAPL","00700", "000001"
    :return: unified representation of a stock code. i.e. "US.AAPL", "HK.00700", "SZ.000001"

    """
    mkt_qot = Market.NONE
    if trd_sec_mkt == Trd_Common_pb2.TrdSecMarket_HK:
        mkt_qot = Market.HK
    elif trd_sec_mkt == Trd_Common_pb2.TrdSecMarket_CN_SH:
        mkt_qot = Market.SH
    elif trd_sec_mkt == Trd_Common_pb2.TrdSecMarket_CN_SZ:
        mkt_qot = Market.SZ
    elif trd_sec_mkt == Trd_Common_pb2.TrdSecMarket_US:
        mkt_qot = Market.US
    _, mkt = Market.to_number(mkt_qot)
    return merge_qot_mkt_stock_str(mkt, partial_stock_str)


def str2binary(s):
    """
    Transfer string to binary
    :param s: string content to be transformed to binary
    :return: binary
    """
    return s.encode('utf-8')


def is_str(obj):
    if sys.version_info.major == 3:
        return isinstance(obj, str) or isinstance(obj, bytes)
    else:
        return isinstance(obj, basestring)


def price_to_str_int1000(price):
    return str(int(round(float(price) * 1000,
                         0))) if str(price) is not '' else ''


# 1000*int price to float val
def int1000_price_to_float(price):
    return round(float(price) / 1000.0,
                 3) if str(price) is not '' else float(0)


# 10^9 int price to float val
def int10_9_price_to_float(price):
    return round(float(price) / float(10**9),
                 3) if str(price) is not '' else float(0)


# list 参数除重及规整
def unique_and_normalize_list(lst):
    ret = []
    if not lst:
        return ret
    tmp = lst if isinstance(lst, list) else [lst]
    [ret.append(x) for x in tmp if x not in ret]
    return ret


def md5_transform(raw_str):
    h1 = hashlib.md5()
    h1.update(raw_str.encode(encoding='utf-8'))
    return h1.hexdigest()


g_unique_id = int(time.time() % 10000)
g_unique_lock = RLock()
def get_unique_id32():
    global g_unique_id
    with g_unique_lock:
        g_unique_id += 1
        if g_unique_id >= 4294967295:
            g_unique_id = int(time.time() % 10000)
        ret_id = g_unique_id
    return ret_id


class ProtobufMap(dict):
    created_protobuf_map = {}

    def __init__(self):

        """ InitConnect = 1001  # 初始化连接 """
        from futu.common.pb.InitConnect_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.InitConnect] = Response()

        """ GetGlobalState = 1002  # 获取全局状态 """
        from futu.common.pb.GetGlobalState_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.GetGlobalState] = Response()

        """ Notify = 1003  # 通知推送 """
        from futu.common.pb.Notify_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Notify] = Response()

        """ KeepAlive = 1004  # 通知推送 """
        from futu.common.pb.KeepAlive_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.KeepAlive] = Response()

        """ GetUserInfo = 1005  # 获取全局状态 """
        from futu.common.pb.GetUserInfo_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.GetUserInfo] = Response()

        """ GetUserInfo = 1006  # 获取用户信息 """
        from futu.common.pb.Verification_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Verification] = Response()

        """ GetUserInfo = 1007  # 获取延迟统计 """
        from futu.common.pb.GetDelayStatistics_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.GetDelayStatistics] = Response()

        """ TestCmd = 1008  # 测试命令 """
        from futu.common.pb.TestCmd_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.TestCmd] = Response()

        """ Trd_GetAccList = 2001  # 获取业务账户列表 """
        from futu.common.pb.Trd_GetAccList_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Trd_GetAccList] = Response()

        """ Trd_UnlockTrade = 2005  # 解锁或锁定交易 """
        from futu.common.pb.Trd_UnlockTrade_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Trd_UnlockTrade] = Response()

        """ Trd_SubAccPush = 2008  # 订阅业务账户的交易推送数据 """
        from futu.common.pb.Trd_SubAccPush_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Trd_SubAccPush] = Response()

        """  Trd_GetFunds = 2101  # 获取账户资金 """
        from futu.common.pb.Trd_GetFunds_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Trd_GetFunds] = Response()

        """ Trd_GetPositionList = 2102  # 获取账户持仓 """
        from futu.common.pb.Trd_GetPositionList_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Trd_GetPositionList] = Response()

        """ Trd_GetOrderList = 2201  # 获取订单列表 """
        from futu.common.pb.Trd_GetOrderList_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Trd_GetOrderList] = Response()

        """ Trd_PlaceOrder = 2202  # 下单 """
        from futu.common.pb.Trd_PlaceOrder_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Trd_PlaceOrder] = Response()

        """ Trd_ModifyOrder = 2205  # 修改订单 """
        from futu.common.pb.Trd_ModifyOrder_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Trd_ModifyOrder] = Response()

        """ Trd_UpdateOrder = 2208  # 订单状态变动通知(推送) """
        from futu.common.pb.Trd_UpdateOrder_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Trd_UpdateOrder] = Response()

        """ Trd_GetOrderFillList = 2211  # 获取成交列表 """
        from futu.common.pb.Trd_GetOrderFillList_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Trd_GetOrderFillList] = Response()

        """ Trd_UpdateOrderFill = 2218  # 成交通知(推送) """
        from  futu.common.pb.Trd_UpdateOrderFill_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Trd_UpdateOrderFill] = Response()

        """ Trd_GetHistoryOrderList = 2221  # 获取历史订单列表 """
        from futu.common.pb.Trd_GetHistoryOrderList_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Trd_GetHistoryOrderList] = Response()

        """ Trd_GetHistoryOrderFillList = 2222  # 获取历史成交列表 """
        from futu.common.pb.Trd_GetHistoryOrderFillList_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Trd_GetHistoryOrderFillList] = Response()

        """ Qot_Sub = 3001  # 订阅或者反订阅 """
        from futu.common.pb.Qot_Sub_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Qot_Sub] = Response()

        """ Qot_RegQotPush = 3002  # 注册推送 """
        from futu.common.pb.Qot_RegQotPush_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Qot_RegQotPush] = Response()

        """ Qot_GetSubInfo = 3003  # 获取订阅信息 """
        from futu.common.pb.Qot_GetSubInfo_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Qot_GetSubInfo] = Response()

        """ Qot_GetBasicQot = 3004  # 获取股票基本行情 """
        from futu.common.pb.Qot_GetBasicQot_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Qot_GetBasicQot] = Response()

        """ Qot_UpdateBasicQot = 3005  # 推送股票基本行情 """
        from futu.common.pb.Qot_UpdateBasicQot_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Qot_UpdateBasicQot] = Response()

        """ Qot_GetKL = 3006  # 获取K线 """
        from futu.common.pb.Qot_GetKL_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Qot_GetKL] = Response()

        """ Qot_UpdateKL = 3007  # 推送K线 """
        from futu.common.pb.Qot_UpdateKL_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Qot_UpdateKL] = Response()

        """ Qot_GetRT = 3008  # 获取分时 """
        from futu.common.pb.Qot_GetRT_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Qot_GetRT] = Response()

        """ Qot_UpdateRT = 3009  # 推送分时 """
        from futu.common.pb.Qot_UpdateRT_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Qot_UpdateRT] = Response()

        """ Qot_GetTicker = 3010  # 获取逐笔 """
        from futu.common.pb.Qot_GetTicker_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Qot_GetTicker] = Response()

        """ Qot_UpdateTicker = 3011  # 推送逐笔 """
        from futu.common.pb.Qot_UpdateTicker_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Qot_UpdateTicker] = Response()

        """ Qot_GetOrderBook = 3012  # 获取买卖盘 """
        from futu.common.pb.Qot_GetOrderBook_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Qot_GetOrderBook] = Response()

        """ Qot_UpdateOrderBook = 3013  # 推送买卖盘 """
        from futu.common.pb.Qot_UpdateOrderBook_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Qot_UpdateOrderBook] = Response()

        """ Qot_GetBroker = 3014  # 获取经纪队列 """
        from futu.common.pb.Qot_GetBroker_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Qot_GetBroker] = Response()

        """ Qot_UpdateBroker = 3015  # 推送经纪队列 """
        from futu.common.pb.Qot_UpdateBroker_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Qot_UpdateBroker] = Response()

        """ Qot_UpdatePriceReminder = 3019  # 推送到价提醒 """
        from futu.common.pb.Qot_UpdatePriceReminder_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Qot_UpdatePriceReminder] = Response()


        """ Qot_GetTradeDate = 3200  # 获取市场交易日 """
        from futu.common.pb.Qot_GetTradeDate_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Qot_GetTradeDate] = Response()

        """ Qot_GetSuspend = 3201  # 获取股票停牌信息 """
        from futu.common.pb.Qot_GetSuspend_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Qot_GetSuspend] = Response()

        """ Qot_GetStaticInfo = 3202  # 获取股票列表 """
        from futu.common.pb.Qot_GetStaticInfo_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Qot_GetStaticInfo] = Response()

        """ Qot_GetSecuritySnapshot = 3203  # 获取股票快照 """
        from futu.common.pb.Qot_GetSecuritySnapshot_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Qot_GetSecuritySnapshot] = Response()

        """ Qot_GetPlateSet = 3204  # 获取板块集合下的板块 """
        from futu.common.pb.Qot_GetPlateSet_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Qot_GetPlateSet] = Response()

        """ Qot_GetPlateSecurity = 3205  # 获取板块下的股票 """
        from futu.common.pb.Qot_GetPlateSecurity_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Qot_GetPlateSecurity] = Response()

        """ Trd_GetMaxTrdQtys = 2111 查询最大买卖数量 """
        from futu.common.pb.Trd_GetMaxTrdQtys_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Trd_GetMaxTrdQtys] = Response()

        """ Qot_GetReference = 3206  获取正股相关股票，暂时只有窝轮"""
        from futu.common.pb.Qot_GetReference_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Qot_GetReference] = Response()

        """ Qot_GetOwnerPlate = 3207 获取股票所属板块"""
        from futu.common.pb.Qot_GetOwnerPlate_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Qot_GetOwnerPlate] = Response()

        """ Qot_GetOwnerPlate = 3208 获取高管持股变动"""
        from futu.common.pb.Qot_GetHoldingChangeList_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Qot_GetHoldingChangeList] = Response()

        from futu.common.pb.Qot_RequestHistoryKL_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Qot_RequestHistoryKL] = Response()

        from futu.common.pb.Qot_GetOptionChain_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Qot_GetOptionChain] = Response()

        """ Qot_GetOrderDetail = 3016 获取委托明细 """
        from futu.common.pb.Qot_GetOrderDetail_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Qot_GetOrderDetail] = Response()

        """ Qot_UpdateOrderDetail = 3017 推送委托明细 """
        from futu.common.pb.Qot_UpdateOrderDetail_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Qot_UpdateOrderDetail] = Response()

        """ Qot_GetWarrantData = 3210 获取窝轮 """
        from futu.common.pb.Qot_GetWarrant_pb2 import Response as GetWarrantPBResponse
        ProtobufMap.created_protobuf_map[ProtoId.Qot_GetWarrant] = GetWarrantPBResponse()

        """ Qot_GetOrderDetail = 3104 已使用过的额度 """
        from futu.common.pb.Qot_RequestHistoryKLQuota_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Qot_RequestHistoryKLQuota] = Response()

        """获取除权信息"""
        from futu.common.pb.Qot_RequestRehab_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Qot_RequestRehab] = Response()

        from futu.common.pb.Qot_GetCapitalDistribution_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Qot_GetCapitalDistribution] = Response()

        from futu.common.pb.Qot_GetCapitalFlow_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Qot_GetCapitalFlow] = Response()

        from futu.common.pb.Qot_GetUserSecurity_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Qot_GetUserSecurity] = Response()

        from futu.common.pb.Qot_ModifyUserSecurity_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Qot_ModifyUserSecurity] = Response()

        from futu.common.pb.Qot_StockFilter_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Qot_StockFilter] = Response()

        from futu.common.pb.Qot_GetCodeChange_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Qot_GetCodeChange] = Response()

        from futu.common.pb.Qot_GetIpoList_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Qot_GetIpoList] = Response()
        
        from futu.common.pb.Qot_GetFutureInfo_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Qot_GetFutureInfo] = Response()

        from futu.common.pb.Qot_RequestTradeDate_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Qot_RequestTradeDate] = Response()

        from futu.common.pb.Qot_SetPriceReminder_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Qot_SetPriceReminder] = Response()

        from futu.common.pb.Qot_GetPriceReminder_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Qot_GetPriceReminder] = Response()

        from futu.common.pb.Qot_GetUserSecurityGroup_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Qot_GetUserSecurityGroup] = Response()

        from futu.common.pb.Qot_GetMarketState_pb2 import Response
        ProtobufMap.created_protobuf_map[ProtoId.Qot_GetMarketState] = Response()

    def __getitem__(self, key):
        return ProtobufMap.created_protobuf_map[key] if key in ProtobufMap.created_protobuf_map else None


pb_map = ProtobufMap()

def binary2str(b, proto_id, proto_fmt_type):
    """
    Transfer binary to string
    :param b: binary content to be transformed to string
    :return: string
    """
    if proto_fmt_type == ProtoFMT.Json:
        return b.decode('utf-8')
    elif proto_fmt_type == ProtoFMT.Protobuf:
        rsp = pb_map[proto_id]
        if IS_PY2:
            rsp.ParseFromString(str(b))
        else:
            rsp.ParseFromString(b)
        return MessageToJson(rsp)
    else:
        raise Exception("binary2str: unknown proto format.")


def binary2pb(b, proto_id, proto_fmt_type):
    """
    Transfer binary to pb message
    :param b: binary content to be transformed to pb message
    :return: pb message
    """
    rsp = pb_map[proto_id]
    if rsp is None:
        return None
    if proto_fmt_type == ProtoFMT.Json:
        return json2pb(type(rsp), b.decode('utf-8'))
    elif proto_fmt_type == ProtoFMT.Protobuf:
        try:
            rsp = type(rsp)()
            # logger.debug((proto_id))
            if IS_PY2:
                rsp.ParseFromString(str(b))
            else:
                rsp.ParseFromString(b)
        except Exception as e:
            print(e)
        return rsp
    else:
        raise Exception("binary2str: unknown proto format.")


def pack_pb_req(pb_req, proto_id, conn_id, serial_no=0):
    proto_fmt = SysConfig.get_proto_fmt()
    serial_no = serial_no if serial_no else get_unique_id32()
    is_encrypt = FutuConnMng.is_conn_encrypt(conn_id)

    if proto_fmt == ProtoFMT.Json:
        req_json = MessageToJson(pb_req)
        ret, msg, req = _joint_head(proto_id, proto_fmt, len(req_json),
                          req_json.encode(), conn_id, serial_no, is_encrypt)
        return ret, msg, req

    elif proto_fmt == ProtoFMT.Protobuf:
        ret, msg, req = _joint_head(proto_id, proto_fmt, pb_req.ByteSize(), pb_req, conn_id, serial_no, is_encrypt)
        return ret, msg, req
    else:
        error_str = ERROR_STR_PREFIX + 'unknown protocol format, %d' % proto_fmt
        return RET_ERROR, error_str, None


def _joint_head(proto_id, proto_fmt_type, body_len, str_body, conn_id, serial_no, is_encrypt):

    # sha20 = b'00000000000000000000'
    reserve8 = b'\x00\x00\x00\x00\x00\x00\x00\x00'

    if proto_fmt_type == ProtoFMT.Protobuf:
        str_body = str_body.SerializeToString()

    if type(str_body) is not bytes:
        str_body = bytes_utf8(str_body)
    sha20 = hashlib.sha1(str_body).digest()

    # init connect 需要用rsa加密
    try:
        if proto_id == ProtoId.InitConnect:
            if SysConfig.INIT_RSA_FILE != '':
                str_body = RsaCrypt.encrypt(str_body)
                body_len = len(str_body)
        else:
            if is_encrypt:
                ret, msg, str_body = FutuConnMng.encrypt_conn_data(conn_id, str_body)
                body_len = len(str_body)
                if ret != RET_OK:
                    return ret, msg, str_body
    except Exception as e:
        return RET_ERROR, str(e), None

    fmt = "%s%ds" % (MESSAGE_HEAD_FMT, body_len)

    bin_head = struct.pack(fmt, b'F', b'T', proto_id, proto_fmt_type,
                           API_PROTO_VER, serial_no, body_len, sha20, reserve8, str_body)

    return RET_OK, "", bin_head


def parse_head(head_bytes):
    head_dict = {}
    head_dict['head_1'], head_dict['head_2'], head_dict['proto_id'], \
    head_dict['proto_fmt_type'], head_dict['proto_ver'], \
    head_dict['serial_no'], head_dict['body_len'], head_dict['sha20'], \
    head_dict['reserve8'], = struct.unpack(MESSAGE_HEAD_FMT, head_bytes)
    return head_dict


def parse_proto_info(head_bytes):
    unpacked = struct.unpack(MESSAGE_HEAD_FMT, head_bytes)
    return ProtoInfo(unpacked[2], unpacked[5])


def decrypt_rsp_body(rsp_body, head_dict, conn_id, is_encrypt):
    ret_code = RET_OK
    msg = ''
    sha20 = head_dict['sha20']
    proto_id = head_dict['proto_id']

    if is_encrypt:
        try:
            if proto_id == ProtoId.InitConnect:
                rsp_body = RsaCrypt.decrypt(rsp_body)
            else:
                ret_code, msg, decrypt_data = FutuConnMng.decrypt_conn_data(conn_id, rsp_body)
                rsp_body = decrypt_data

        except Exception as e:
            msg = sys.exc_info()[1]
            ret_code = RET_ERROR

    # check sha20
    if ret_code == RET_OK:
        sha20_check = hashlib.sha1(rsp_body).digest()
        if sha20_check != sha20:
            ret_code = RET_ERROR
            msg = "proto id:{} conn_id:{} check sha error!".format(proto_id, conn_id)

    return ret_code, msg, rsp_body


def make_from_namedtuple(t, **kwargs):
    """
    t是namedtuple，复制一份t，但其中部分字段更新为kwargs的值
    :param t:
    :param kwargs:
    :return:
    """
    d = t._asdict()
    d.update(kwargs)
    cls = type(t)
    return cls(**d)