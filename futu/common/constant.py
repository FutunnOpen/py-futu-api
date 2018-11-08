# -*- coding: utf-8 -*-
"""
    Constant collection
"""
from copy import copy


RET_OK = 0
RET_ERROR = -1
ERROR_STR_PREFIX = 'ERROR. '
EMPTY_STRING = ''

MESSAGE_HEAD_FMT = "<1s1sI2B2I20s8s"
"""
    #pragma pack(push, APIProtoHeader, 1)
    struct APIProtoHeader
    {
        u8_t szHeaderFlag[2]; //包头起始标志，固定为“FT”
        u32_t nProtoID;	 //协议ID
        u8_t nProtoFmtType; //协议格式类型，0为Protobuf格式，1为Json格式
        u8_t nProtoVer; //协议版本，用于迭代兼容
        u32_t nSerialNo; //包序列号
        u32_t nBodyLen; //包体长度
        u8_t arrBodySHA1[20]; //包体原数据(解密后)的SHA1哈希值
        u8_t arrReserved[8]; //保留8字节扩展
    };
    #pragma pack(pop, APIProtoHeader)
"""

# 默认的ClientID, 用于区分不同的api
DEFULAT_CLIENT_ID = "PyNormal"
CLIENT_VERSION = 300

# 默认的init_connect连接用的rsa private key文件路径
DEFAULT_INIT_PRI_KEY_FILE = "conn_key.txt"

# 协议格式
class ProtoFMT(object):
    """
    协议格式类型
    ..  py:class:: ProtoFMT
     ..  py:attribute:: Protobuf
      google的protobuf格式
     ..  py:attribute:: Json
      json格式
    """
    Protobuf = 0
    Json = 1

# 默认的协议格式 : set_proto_fmt 更改
DEFULAT_PROTO_FMT = ProtoFMT.Protobuf

# api的协议版本号
API_PROTO_VER = int(0)

# 市场标识字符串
class Market(object):
    """
    标识不同的行情市场，股票名称的前缀复用该字符串,如 **'HK.00700'**, **'HK_FUTURE.999010'**
    ..  py:class:: Market
     ..  py:attribute:: HK
      港股
     ..  py:attribute:: US
      美股
     ..  py:attribute:: SH
      沪市
     ..  py:attribute:: SH
      深市
     ..  py:attribute:: HK_FUTURE
      港股期货
     ..  py:attribute:: NONE
      未知
    """
    HK = "HK"
    US = "US"
    SH = "SH"
    SZ = "SZ"
    HK_FUTURE = "HK_FUTURE"
    NONE = "N/A"

MKT_MAP = {
    Market.NONE: 0,
    Market.HK: 1,
    Market.HK_FUTURE: 2,
    Market.US: 11,
    Market.SH: 21,
    Market.SZ: 22
}

from .pb import Trd_Common_pb2
from .pb import Qot_Common_pb2

QOT_MARKET_TO_TRD_SEC_MARKET_MAP = {
    Qot_Common_pb2.QotMarket_Unknown: Trd_Common_pb2.TrdSecMarket_Unknown,
    Qot_Common_pb2.QotMarket_CNSH_Security: Trd_Common_pb2.TrdSecMarket_CN_SH,
    Qot_Common_pb2.QotMarket_CNSZ_Security: Trd_Common_pb2.TrdSecMarket_CN_SZ,
    Qot_Common_pb2.QotMarket_HK_Security: Trd_Common_pb2.TrdSecMarket_HK,
    Qot_Common_pb2.QotMarket_HK_Future: Trd_Common_pb2.TrdSecMarket_HK,
    Qot_Common_pb2.QotMarket_US_Security: Trd_Common_pb2.TrdSecMarket_US,
}

# 市场状态
class MarketState:
    """
    行情市场状态定义
    ..  py:class:: MarketState
     ..  py:attribute:: NONE
      无交易,美股未开盘
     ..  py:attribute:: AUCTION
      竞价
     ..  py:attribute:: WAITING_OPEN
      早盘前等待开盘
     ..  py:attribute:: MORNING
      早盘前等待开盘
     ..  py:attribute:: REST
      午间休市
     ..  py:attribute:: AFTERNOON
      午盘
     ..  py:attribute:: CLOSED
      收盘
     ..  py:attribute:: PRE_MARKET_BEGIN
      盘前开始
     ..  py:attribute:: PRE_MARKET_END
      盘前结束
     ..  py:attribute:: AFTER_HOURS_BEGIN
      盘后开始
     ..  py:attribute:: AFTER_HOURS_END
      盘后结束
     ..  py:attribute:: AFTER_HOURS_END
      盘后结束
     ..  py:attribute:: NIGHT_OPEN
      夜市开盘
     ..  py:attribute:: NIGHT_END
      夜市收盘
     ..  py:attribute:: FUTURE_DAY_OPEN
      期指日市开盘
     ..  py:attribute:: FUTURE_DAY_BREAK
      期指日市休市
     ..  py:attribute:: FUTURE_DAY_CLOSE
      期指日市收盘
     ..  py:attribute:: FUTURE_DAY_WAIT_OPEN
      期指日市等待开盘
     ..  py:attribute:: HK_CAS
      港股盘后竞价
    """
    NONE = "NONE"                                   # 无交易,美股未开盘
    AUCTION = "AUCTION"                             # 竞价
    WAITING_OPEN = "WAITING_OPEN"                   # 早盘前等待开盘
    MORNING = "MORNING"                             # 早盘
    REST = "REST"                                   # 午间休市
    AFTERNOON = "AFTERNOON"                         # 午盘
    CLOSED = "CLOSED"                               # 收盘
    PRE_MARKET_BEGIN = "PRE_MARKET_BEGIN"           # 盘前
    PRE_MARKET_END = "PRE_MARKET_END"               # 盘前结束
    AFTER_HOURS_BEGIN = "AFTER_HOURS_BEGIN"         # 盘后
    AFTER_HOURS_END = "AFTER_HOURS_END"             # 盘后结束
    NIGHT_OPEN = "NIGHT_OPEN"                       # 夜市开盘
    NIGHT_END = "NIGHT_END"                         # 夜市收盘
    FUTURE_DAY_OPEN = "FUTURE_DAY_OPEN"             # 期指日市开盘
    FUTURE_DAY_BREAK = "FUTURE_DAY_BREAK"           # 期指日市休市
    FUTURE_DAY_CLOSE = "FUTURE_DAY_CLOSE"           # 期指日市收盘
    FUTURE_DAY_WAIT_OPEN = "FUTURE_DAY_WAIT_OPEN"   # 期指日市等待开盘
    HK_CAS = "HK_CAS"                               # 盘后竞价, 港股市场增加CAS机制对应的市场状态


MARKET_STATE_MAP = {
    MarketState.NONE: 0,
    MarketState.AUCTION: 1,
    MarketState.WAITING_OPEN: 2,
    MarketState.MORNING: 3,
    MarketState.REST: 4,
    MarketState.AFTERNOON: 5,
    MarketState.CLOSED: 6,
    MarketState.PRE_MARKET_BEGIN: 8,
    MarketState.PRE_MARKET_END: 9,
    MarketState.AFTER_HOURS_BEGIN: 10,
    MarketState.AFTER_HOURS_END: 11,
    MarketState.NIGHT_OPEN: 13,
    MarketState.NIGHT_END: 14,
    MarketState.FUTURE_DAY_OPEN: 15,
    MarketState.FUTURE_DAY_BREAK: 16,
    MarketState.FUTURE_DAY_CLOSE: 17,
    MarketState.FUTURE_DAY_WAIT_OPEN: 18,
    MarketState.HK_CAS: 19,
}


# 股票类型
class SecurityType(object):
    """
    证券类型定义
    ..  py:class:: SecurityType
     ..  py:attribute:: STOCK
      股票
     ..  py:attribute:: IDX
      指数
     ..  py:attribute:: ETF
      交易所交易基金(Exchange Traded Funds)
     ..  py:attribute:: WARRANT
      港股涡轮牛熊证
     ..  py:attribute:: BOND
      债券
    ..  py:attribute:: DRVT
      期权
     ..  py:attribute:: NONE
      未知
    """
    STOCK = "STOCK"
    IDX = "IDX"
    ETF = "ETF"
    WARRANT = "WARRANT"
    BOND = "BOND"
    DRVT = "DRVT"
    NONE = "N/A"

SEC_TYPE_MAP = {
    SecurityType.STOCK: 3,
    SecurityType.IDX: 6,
    SecurityType.ETF: 4,
    SecurityType.WARRANT: 5,
    SecurityType.BOND: 1,
    SecurityType.DRVT:8,
    SecurityType.NONE: 0
}


# 窝轮类型
class WrtType(object):
    """
    港股窝轮类型
    ..  py:class:: WrtType
     ..  py:attribute:: CALL
      认购
     ..  py:attribute:: PUT
      认沽
     ..  py:attribute:: BULL
      牛证
     ..  py:attribute:: BEAR
      熊证
     ..  py:attribute:: NONE
      未知
    """
    CALL = "CALL"
    PUT = "PUT"
    BULL = "BULL"
    BEAR = "BEAR"
    NONE = "N/A"

WRT_TYPE_MAP = {WrtType.CALL: 1, WrtType.PUT: 2, WrtType.BULL: 3, WrtType.BEAR: 4, WrtType.NONE: 0}


# 实时数据定阅类型
class SubType(object):
    """
    实时数据定阅类型定义
    ..  py:class:: SubType
     ..  py:attribute:: TICKER
      逐笔
     ..  py:attribute:: QUOTE
      报价
     ..  py:attribute:: ORDER_BOOK
      买卖摆盘
     ..  py:attribute:: K_1M
      1分钟K线
     ..  py:attribute:: K_5M
      5分钟K线
     ..  py:attribute:: K_15M
      15分钟K线
     ..  py:attribute:: K_30M
      30分钟K线
     ..  py:attribute:: K_60M
      60分钟K线
     ..  py:attribute:: K_DAY
      日K线
     ..  py:attribute:: K_WEEK
      周K线
     ..  py:attribute:: K_MON
      月K线
     ..  py:attribute:: RT_DATA
      分时
     ..  py:attribute:: BROKER
      买卖经纪
     ..  py:attribute:: ORDER_DETAIL
      委托明细
    """
    TICKER = "TICKER"
    QUOTE = "QUOTE"
    ORDER_BOOK = "ORDER_BOOK"
    ORDER_DETAIL = "ORDER_DETAIL"
    K_1M = "K_1M"
    K_5M = "K_5M"
    K_15M = "K_15M"
    K_30M = "K_30M"
    K_60M = "K_60M"
    K_DAY = "K_DAY"
    K_WEEK = "K_WEEK"
    K_MON = "K_MON"
    RT_DATA = "RT_DATA"
    BROKER = "BROKER"


KLINE_SUBTYPE_LIST = [SubType.K_DAY, SubType.K_MON, SubType.K_WEEK,
                      SubType.K_1M, SubType.K_5M, SubType.K_15M,
                      SubType.K_30M, SubType.K_60M
                      ]


SUBTYPE_MAP = {
    SubType.QUOTE: 1,
    SubType.ORDER_BOOK: 2,
    SubType.TICKER: 4,
    SubType.RT_DATA: 5,
    SubType.K_DAY: 6,
    SubType.K_5M: 7,
    SubType.K_15M: 8,
    SubType.K_30M: 9,
    SubType.K_60M: 10,
    SubType.K_1M: 11,
    SubType.K_WEEK: 12,
    SubType.K_MON: 13,
    SubType.BROKER: 14,
    SubType.ORDER_DETAIL: 18
}


# k线类型
class KLType(object):
    """
    k线类型定义
    ..  py:class:: KLType
     ..  py:attribute:: K_1M
      1分钟K线
     ..  py:attribute:: K_5M
      5分钟K线
     ..  py:attribute:: K_15M
      15分钟K线
     ..  py:attribute:: K_30M
      30分钟K线
     ..  py:attribute:: K_60M
      60分钟K线
     ..  py:attribute:: K_DAY
      日K线
     ..  py:attribute:: K_WEEK
      周K线
     ..  py:attribute:: K_MON
      月K线
    """
    K_1M = "K_1M"
    K_5M = "K_5M"
    K_15M = "K_15M"
    K_30M = "K_30M"
    K_60M = "K_60M"
    K_DAY = "K_DAY"
    K_WEEK = "K_WEEK"
    K_MON = "K_MON"

KTYPE_MAP = {
    KLType.K_1M: 1,
    KLType.K_5M: 6,
    KLType.K_15M: 7,
    KLType.K_30M: 8,
    KLType.K_60M: 9,
    KLType.K_DAY: 2,
    KLType.K_WEEK: 3,
    KLType.K_MON: 4
}


class KLDataStatus(object):
    """
    指定时间点取历史k线， 获得数据的实际状态
    ..  py:class:: KLDataStatus
     ..  py:attribute:: NONE
      无效数据
     ..  py:attribute:: CURRENT
      当前时间周期数据
     ..  py:attribute:: PREVIOUS
      前一时间周期数据
     ..  py:attribute:: BACK
      后一时间周期数据
    """
    NONE = 'N/A'
    CURRENT = 'CURRENT'
    PREVIOUS = 'PREVIOUS'
    BACK = 'BACK'


KLDATA_STATUS_MAP = {
    KLDataStatus.NONE: 0,
    KLDataStatus.CURRENT: 1,
    KLDataStatus.PREVIOUS: 2,
    KLDataStatus.BACK: 3,
}


# k线复权
class AuType(object):
    """
    k线复权类型定义
    ..  py:class:: AuType
     ..  py:attribute:: QFQ
      前复权
     ..  py:attribute:: HFQ
      后复权
     ..  py:attribute:: NONE
      不复权
    """
    QFQ = "qfq"
    HFQ = "hfq"
    NONE = "None"

AUTYPE_MAP = {AuType.NONE: 0, AuType.QFQ: 1, AuType.HFQ: 2}


# 指定时间为非交易日时，对应的k线数据取值模式， get_multi_points_history_kline 参数用到
class KLNoDataMode(object):
    """
    指定时间为非交易日时，对应的K线数据取值模式
    ..  py:class:: KLNoDataMode
     ..  py:attribute:: NONE
      返回无数据
     ..  py:attribute:: FORWARD
      往前取数据
     ..  py:attribute:: BACKWARD
      往后取数据
    """
    NONE = 0     # 返回无数据
    FORWARD = 1  # 往前取数据
    BACKWARD = 2  # 往后取数据


# k线数据字段
class KL_FIELD(object):
    """
    获取K线数据, 可指定需返回的字段
    ..  py:class:: KL_FIELD
     ..  py:attribute:: ALL
      所有字段
     ..  py:attribute:: DATE_TIME
      日期时间
     ..  py:attribute:: OPEN
      开盘价
     ..  py:attribute:: CLOSE
      收盘价
     ..  py:attribute:: HIGH
      最高价
     ..  py:attribute:: LOW
      最低价
     ..  py:attribute:: PE_RATIO
      市盈率
     ..  py:attribute:: TURNOVER_RATE
      换手率
     ..  py:attribute:: TRADE_VOL
      成交量
     ..  py:attribute:: TRADE_VAL
      成交额
     ..  py:attribute:: CHANGE_RATE
      涨跌比率
     ..  py:attribute:: LAST_CLOSE
      昨收价
    """
    ALL = ''
    DATE_TIME = '1'
    OPEN = '2'
    CLOSE = '3'
    HIGH = '4'
    LOW = '5'
    PE_RATIO = '6'
    TURNOVER_RATE = '7'
    TRADE_VOL = '8'
    TRADE_VAL = '9'
    CHANGE_RATE = '10'
    LAST_CLOSE = '11'

    ALL_REAL = [
        DATE_TIME, OPEN, CLOSE, HIGH, LOW, PE_RATIO, TURNOVER_RATE, TRADE_VOL,
        TRADE_VAL, CHANGE_RATE, LAST_CLOSE
    ]

    FIELD_FLAG_VAL_MAP = {
        DATE_TIME: 0,
        HIGH: 1,
        OPEN: 2,
        LOW: 4,
        CLOSE: 8,
        LAST_CLOSE: 16,
        TRADE_VOL: 32,
        TRADE_VAL: 64,
        TURNOVER_RATE: 128,
        PE_RATIO: 256,
        CHANGE_RATE: 512,
    }

    DICT_KL_FIELD_STR = {
        DATE_TIME: 'time_key',
        OPEN: 'open',
        CLOSE: 'close',
        HIGH: 'high',
        LOW: 'low',
        PE_RATIO: 'pe_ratio',
        TURNOVER_RATE: 'turnover_rate',
        TRADE_VOL: 'volume',
        TRADE_VAL: 'turnover',
        CHANGE_RATE: 'change_rate',
        LAST_CLOSE: 'last_close'
    }

    @classmethod
    def get_field_list(cls, str_filed):
        ret_list = []
        data = str(str_filed).split(',')
        if KL_FIELD.ALL in data:
            ret_list = copy(KL_FIELD.ALL_REAL)
        else:
            for x in data:
                if x in KL_FIELD.ALL_REAL:
                    ret_list.append(x)
        return ret_list

    @classmethod
    def normalize_field_list(cls, fields):
        list_ret = []
        if KL_FIELD.ALL in fields:
            list_ret = copy(KL_FIELD.ALL_REAL)
        else:
            for x in fields:
                if x in KL_FIELD.ALL_REAL and x not in list_ret:
                    list_ret.append(x)
        return list_ret

    @classmethod
    def kl_fields_to_flag_val(cls, fields):
        fields_normal = KL_FIELD.normalize_field_list(fields)
        ret_flags = 0
        for x in fields_normal:
            ret_flags += KL_FIELD.FIELD_FLAG_VAL_MAP[x]
        return ret_flags


# 成交逐笔的方向
class TickerDirect(object):
    """
    逐笔方向定义
    ..  py:class:: TickerDirect
     ..  py:attribute:: BUY
      买
     ..  py:attribute:: SELL
      卖
     ..  py:attribute:: NEUTRAL
      中性
    """
    BUY = "BUY"
    SELL = "SELL"
    NEUTRAL = "NEUTRAL"


TICKER_DIRECTION = {
    TickerDirect.BUY: 1,
    TickerDirect.SELL: 2,
    TickerDirect.NEUTRAL: 3
}


class Plate(object):
    """
    板块集合分类定义
    ..  py:class:: Plate
     ..  py:attribute:: ALL
      所有板块
     ..  py:attribute:: INDUSTRY
      行业板块
     ..  py:attribute:: REGION
      地域板块
     ..  py:attribute:: CONCEPT
      概念板块
    """
    ALL = "ALL"
    INDUSTRY = "INDUSTRY"
    REGION = "REGION"
    CONCEPT = "CONCEPT"
    OTHER = "OTHER"


PLATE_CLASS_MAP = {
    Plate.ALL: 0,
    Plate.INDUSTRY: 1,
    Plate.REGION: 2,
    Plate.CONCEPT: 3,
    Plate.OTHER: 4
}

PLATE_TYPE_ID_TO_NAME= [
    "ALL",
    "INDUSTRY",
    "REGION",
    "CONCEPT",
    "OTHER"
]

# 股票持有者类别
class StockHolder(object):
    """
    持有者类别
    ..  py:class:: StockHolderType
     ..  py:attribute:: INSTITUTE
      机构
     ..  py:attribute:: FUND
      基金
     ..  py:attribute:: EXECUTIVE
      高管
    """
    INSTITUTE = "INSTITUTE"
    FUND = "FUND"
    EXECUTIVE = "EXECUTIVE"


STOCK_HOLDER_CLASS_MAP = {
    StockHolder.INSTITUTE: 1,
    StockHolder.FUND: 2,
    StockHolder.EXECUTIVE: 3
}


# 期权类型
class OptionType(object):
    """
    期权类型
    ..  py:class:: OptionType
     ..  py:attribute:: ALL
      全部
     ..  py:attribute:: CALL
      涨
     ..  py:attribute:: PUT
      跌
    """
    ALL = "ALL"
    CALL = "CALL"
    PUT = "PUT"


OPTION_TYPE_CLASS_MAP = {
    OptionType.ALL: 0,
    OptionType.CALL: 1,
    OptionType.PUT: 2
}


# 价内价外
class OptionCondType(object):
    """
    价内价外
    ..  py:class:: OptionCondType
     ..  py:attribute:: ALL
      全部
     ..  py:attribute:: WITHIN
      价内
     ..  py:attribute:: OUTSIDE
      价外
    """
    ALL = "ALL"
    WITHIN = "WITHIN"
    OUTSIDE = "OUTSIDE"


OPTION_COND_TYPE_CLASS_MAP = {
    OptionCondType.ALL: 0,
    OptionCondType.WITHIN: 1,
    OptionCondType.OUTSIDE: 2
}

class ProtoId(object):
    InitConnect = 1001  # 初始化连接
    GetGlobalState = 1002  # 获取全局状态
    Notify = 1003  # 通知推送
    KeepAlive = 1004  # 通知推送

    Trd_GetAccList = 2001  # 获取业务账户列表
    Trd_UnlockTrade = 2005  # 解锁或锁定交易
    Trd_SubAccPush = 2008  # 订阅业务账户的交易推送数据

    Trd_GetFunds = 2101  # 获取账户资金
    Trd_GetPositionList = 2102  # 获取账户持仓

    Trd_GetOrderList = 2201  # 获取订单列表
    Trd_PlaceOrder = 2202  # 下单
    Trd_ModifyOrder = 2205  # 修改订单
    Trd_UpdateOrder = 2208  # 订单状态变动通知(推送)

    Trd_GetOrderFillList = 2211  # 获取成交列表
    Trd_UpdateOrderFill = 2218  # 成交通知(推送)

    Trd_GetHistoryOrderList = 2221  # 获取历史订单列表
    Trd_GetHistoryOrderFillList = 2222  # 获取历史成交列表
    Trd_GetAccTradingInfo = 2111    # 查询最大买卖数量

    # 订阅数据
    Qot_Sub = 3001  # 订阅或者反订阅
    Qot_RegQotPush = 3002  # 注册推送
    Qot_GetSubInfo = 3003  # 获取订阅信息
    Qot_GetBasicQot = 3004  # 获取股票基本行情
    Qot_UpdateBasicQot = 3005  # 推送股票基本行情
    Qot_GetKL = 3006  # 获取K线
    Qot_UpdateKL = 3007  # 推送K线
    Qot_GetRT = 3008  # 获取分时
    Qot_UpdateRT = 3009  # 推送分时
    Qot_GetTicker = 3010  # 获取逐笔
    Qot_UpdateTicker = 3011  # 推送逐笔
    Qot_GetOrderBook = 3012  # 获取买卖盘
    Qot_UpdateOrderBook = 3013  # 推送买卖盘
    Qot_GetBroker = 3014  # 获取经纪队列
    Qot_UpdateBroker = 3015  # 推送经纪队列

    # 历史数据
    Qot_GetHistoryKL = 3100  # 获取历史K线
    Qot_GetHistoryKLPoints = 3101  # 获取多只股票历史单点K线
    Qot_GetRehab = 3102  # 获取复权信息
    Qot_RequestHistoryKL = 3103 # 拉取历史K线

    # 其他行情数据
    Qot_GetTradeDate = 3200         # 获取市场交易日
    Qot_GetSuspend = 3201           # 获取股票停牌信息
    Qot_GetStaticInfo = 3202        # 获取股票列表
    Qot_GetSecuritySnapshot = 3203  # 获取股票快照
    Qot_GetPlateSet = 3204          # 获取板块集合下的板块
    Qot_GetPlateSecurity = 3205     # 获取板块下的股票
    Qot_GetReference = 3206         # 获取正股相关股票，暂时只有窝轮
    Qot_GetOwnerPlate = 3207        # 获取股票所属板块
    Qot_GetHoldingChangeList = 3208     # 获取高管持股变动
    Qot_GetOptionChain = 3209           # 获取期权链
    Qot_GetOrderDetail = 3016           # 获取委托明细
    Qot_UpdateOrderDetail = 3017        # 推送委托明细

    All_PushId = [Notify, KeepAlive, Trd_UpdateOrder, Trd_UpdateOrderFill, Qot_UpdateBroker,
                  Qot_UpdateOrderBook, Qot_UpdateKL, Qot_UpdateRT, Qot_UpdateBasicQot, Qot_UpdateTicker]

    @classmethod
    def is_proto_id_push(cls, id):
        return id in ProtoId.All_PushId


class DarkStatus:
    NONE = 'N/A'
    TRADING = 'TRADING'
    END = 'END'

DARK_STATUS_MAP = {
    DarkStatus.NONE: Qot_Common_pb2.DarkStatus_None,
    DarkStatus.TRADING: Qot_Common_pb2.DarkStatus_Trading,
    DarkStatus.END: Qot_Common_pb2.DarkStatus_End
}

class PushDataType:
    NONE = 'N/A'
    REALTIME = 'REALTIME'
    BYDISCONN = 'BYDISCONN'
    CACHE = 'CACHE'

PUSH_DATA_TYPE_MAP = {
    PushDataType.NONE: Qot_Common_pb2.PushDataType_Unknow,
    PushDataType.REALTIME: Qot_Common_pb2.PushDataType_Realtime,
    PushDataType.BYDISCONN: Qot_Common_pb2.PushDataType_ByDisConn,
    PushDataType.CACHE: Qot_Common_pb2.PushDataType_Cache
}

class TickerType:
    UNKNOWN = 'UNKNOWN'
    AUTO_MATCH = 'AUTO_MATCH'
    LATE = 'LATE'
    NON_AUTO_MATCH = 'NON_AUTO_MATCH'
    INTER_AUTO_MATCH = 'INTER_AUTO_MATCH'
    INTER_NON_AUTO_MATCH = 'INTER_NON_AUTO_MATCH'
    ODD_LOT = 'ODD_LOT'
    AUCTION = 'AUCTION'
    BULK = 'BULK'
    CRASH = 'CRASH'
    CROSS_MARKET = 'CROSS_MARKET'
    BULK_SOLD = 'BULK_SOLD'
    FREE_ON_BOARD = 'FREE_ON_BOARD'
    RULE127_OR_155 = 'RULE127_OR_155'
    DELAY = 'DELAY'
    MARKET_CENTER_CLOSE_PRICE = 'MARKET_CENTER_CLOSE_PRICE'
    NEXT_DAY = 'NEXT_DAY'
    MARKET_CENTER_OPENING = 'MARKET_CENTER_OPENING'
    PRIOR_REFERENCE_PRICE = 'PRIOR_REFERENCE_PRICE'
    MARKET_CENTER_OPEN_PRICE = 'MARKET_CENTER_OPEN_PRICE'
    SELLER = 'SELLER'
    T = 'T'
    EXTENDED_TRADING_HOURS = 'EXTENDED_TRADING_HOURS'
    CONTINGENT = 'CONTINGENT'
    AVERAGE_PRICE = 'AVERAGE_PRICE'
    OTC_SOLD = 'OTC_SOLD'
    ODD_LOT_CROSS_MARKET = 'ODD_LOT_CROSS_MARKET'
    DERIVATIVELY_PRICED = 'DERIVATIVELY_PRICED'
    REOPENINGP_RICED = 'REOPENINGP_RICED'
    CLOSING_PRICED = 'CLOSING_PRICED'
    COMPREHENSIVE_DELAY_PRICE = 'COMPREHENSIVE_DELAY_PRICE'


TICKER_TYPE_MAP = {
    TickerType.UNKNOWN: Qot_Common_pb2.TickerType_Unknown,
    TickerType.AUTO_MATCH: Qot_Common_pb2.TickerType_Automatch,
    TickerType.LATE: Qot_Common_pb2.TickerType_Late,
    TickerType.NON_AUTO_MATCH: Qot_Common_pb2.TickerType_NoneAutomatch,
    TickerType.INTER_AUTO_MATCH: Qot_Common_pb2.TickerType_InterAutomatch,
    TickerType.INTER_NON_AUTO_MATCH: Qot_Common_pb2.TickerType_InterNoneAutomatch,
    TickerType.ODD_LOT: Qot_Common_pb2.TickerType_OddLot,
    TickerType.AUCTION: Qot_Common_pb2.TickerType_Auction,
    TickerType.BULK: Qot_Common_pb2.TickerType_Bulk,
    TickerType.CRASH: Qot_Common_pb2.TickerType_Crash,
    TickerType.CROSS_MARKET: Qot_Common_pb2.TickerType_CrossMarket,
    TickerType.BULK_SOLD: Qot_Common_pb2.TickerType_BulkSold,
    TickerType.FREE_ON_BOARD: Qot_Common_pb2.TickerType_FreeOnBoard,
    TickerType.RULE127_OR_155: Qot_Common_pb2.TickerType_Rule127Or155,
    TickerType.DELAY: Qot_Common_pb2.TickerType_Delay,
    TickerType.MARKET_CENTER_CLOSE_PRICE: Qot_Common_pb2.TickerType_MarketCenterClosePrice,
    TickerType.NEXT_DAY: Qot_Common_pb2.TickerType_NextDay,
    TickerType.MARKET_CENTER_OPENING: Qot_Common_pb2.TickerType_MarketCenterOpening,
    TickerType.PRIOR_REFERENCE_PRICE: Qot_Common_pb2.TickerType_PriorReferencePrice,
    TickerType.MARKET_CENTER_OPEN_PRICE: Qot_Common_pb2.TickerType_MarketCenterOpenPrice,
    TickerType.SELLER: Qot_Common_pb2.TickerType_Seller,
    TickerType.T: Qot_Common_pb2.TickerType_T,
    TickerType.EXTENDED_TRADING_HOURS: Qot_Common_pb2.TickerType_ExtendedTradingHours,
    TickerType.CONTINGENT: Qot_Common_pb2.TickerType_Contingent,
    TickerType.AVERAGE_PRICE: Qot_Common_pb2.TickerType_AveragePrice,
    TickerType.OTC_SOLD: Qot_Common_pb2.TickerType_OTCSold,
    TickerType.ODD_LOT_CROSS_MARKET: Qot_Common_pb2.TickerType_OddLotCrossMarket,
    TickerType.DERIVATIVELY_PRICED: Qot_Common_pb2.TickerType_DerivativelyPriced,
    TickerType.REOPENINGP_RICED: Qot_Common_pb2.TickerType_ReOpeningPriced,
    TickerType.CLOSING_PRICED: Qot_Common_pb2.TickerType_ClosingPriced,
    TickerType.COMPREHENSIVE_DELAY_PRICE: Qot_Common_pb2.TickerType_ComprehensiveDelayPrice
}

# noinspection PyPep8Naming
class QUOTE(object):
    REV_MKT_MAP = {MKT_MAP[x]: x for x in MKT_MAP}
    REV_WRT_TYPE_MAP = {WRT_TYPE_MAP[x]: x for x in WRT_TYPE_MAP}
    REV_PLATE_CLASS_MAP = {PLATE_CLASS_MAP[x]: x for x in PLATE_CLASS_MAP}
    REV_SEC_TYPE_MAP = {SEC_TYPE_MAP[x]: x for x in SEC_TYPE_MAP}
    REV_SUBTYPE_MAP = {SUBTYPE_MAP[x]: x for x in SUBTYPE_MAP}
    REV_KTYPE_MAP = {KTYPE_MAP[x]: x for x in KTYPE_MAP}
    REV_AUTYPE_MAP = {AUTYPE_MAP[x]: x for x in AUTYPE_MAP}
    REV_KLDATA_STATUS_MAP = {KLDATA_STATUS_MAP[x]: x for x in KLDATA_STATUS_MAP}
    REV_TICKER_DIRECTION = {TICKER_DIRECTION[x]: x for x in TICKER_DIRECTION}
    REV_MARKET_STATE_MAP = {MARKET_STATE_MAP[x]: x for x in MARKET_STATE_MAP}
    REV_DARK_STATUS_MAP = {DARK_STATUS_MAP[x]: x for x in DARK_STATUS_MAP}
    REV_PUSH_DATA_TYPE_MAP = {PUSH_DATA_TYPE_MAP[x]: x for x in PUSH_DATA_TYPE_MAP}
    REV_TICKER_TYPE_MAP = {TICKER_TYPE_MAP[x]: x for x in TICKER_TYPE_MAP}
    REV_OPTION_TYPE_CLASS_MAP = {OPTION_TYPE_CLASS_MAP[x]: x for x in OPTION_TYPE_CLASS_MAP}
    REV_OPTION_COND_TYPE_CLASS_MAP = {OPTION_COND_TYPE_CLASS_MAP[x]: x for x in OPTION_COND_TYPE_CLASS_MAP}

# sys notify info
class SysNotifyType(object):
    """
    系统异步通知类型定义
    ..  py:class:: SysNotifyType
     ..  py:attribute:: NONE
      未知
     ..  py:attribute:: GTW_EVENT
      网关事件
    """
    NONE = "N/A"
    GTW_EVENT = "GTW_EVENT"


SYS_EVENT_TYPE_MAP = {
    SysNotifyType.NONE: 0, SysNotifyType.GTW_EVENT: 1
}


class GtwEventType(object):
    """
    网关异步通知类型定义
    ..  py:class:: GtwEventType
     ..  py:attribute:: LocalCfgLoadFailed
      本地配置文件加载失败
     ..  py:attribute:: APISvrRunFailed
      网关监听服务运行失败
     ..  py:attribute:: ForceUpdate
      强制升级网关
     ..  py:attribute:: LoginFailed
      登录牛牛服务器失败
     ..  py:attribute:: UnAgreeDisclaimer
      未同意免责声明，无法加运行
     ..  py:attribute:: NetCfgMissing
      缺少网络连接配置
     ..  py:attribute:: KickedOut
      登录被踢下线
     ..  py:attribute:: LoginPwdChanged
      登陆密码变更
     ..  py:attribute:: BanLogin
      牛牛后台不允许该账号登陆
     ..  py:attribute:: NeedPicVerifyCode
      登录需要输入图形验证码
     ..  py:attribute:: NeedPhoneVerifyCode
      登录需要输入手机验证码
     ..  py:attribute:: AppDataNotExist
      程序打包数据丢失
     ..  py:attribute:: NessaryDataMissing
      必要的数据没同步成功
     ..  py:attribute:: TradePwdChanged
      交易密码变更通知
     ..  py:attribute:: EnableDeviceLock
      需启用设备锁
    """
    NONE = "N/A"
    LocalCfgLoadFailed = "LocalCfgLoadFailed"
    APISvrRunFailed = "APISvrRunFailed"
    ForceUpdate = "ForceUpdate"
    LoginFailed = "LoginFailed"
    UnAgreeDisclaimer = "UnAgreeDisclaimer"
    NetCfgMissing = "NetCfgMissing"
    KickedOut = "KickedOut"
    LoginPwdChanged = "LoginPwdChanged"
    BanLogin = "BanLogin"
    NeedPicVerifyCode = "NeedPicVerifyCode"
    NeedPhoneVerifyCode = "NeedPhoneVerifyCode"
    AppDataNotExist = "AppDataNotExist"
    NessaryDataMissing = "NessaryDataMissing"
    TradePwdChanged = "TradePwdChanged"
    EnableDeviceLock="EnableDeviceLock"


GTW_EVENT_MAP = {
    GtwEventType.NONE: 0,
    GtwEventType.LocalCfgLoadFailed: 1,
    GtwEventType.APISvrRunFailed: 2,
    GtwEventType.ForceUpdate: 3,
    GtwEventType.LoginFailed: 4,
    GtwEventType.UnAgreeDisclaimer: 5,
    GtwEventType.NetCfgMissing: 6,
    GtwEventType.KickedOut: 7,
    GtwEventType.LoginPwdChanged: 8,
    GtwEventType.BanLogin: 9,
    GtwEventType.NeedPicVerifyCode: 10,
    GtwEventType.NeedPhoneVerifyCode: 11,
    GtwEventType.AppDataNotExist: 12,
    GtwEventType.NessaryDataMissing: 13,
    GtwEventType.TradePwdChanged: 14,
    GtwEventType.EnableDeviceLock: 15,
}


class SysNoitfy(object):
    REV_SYS_EVENT_TYPE_MAP = {SYS_EVENT_TYPE_MAP[x]: x for x in SYS_EVENT_TYPE_MAP}
    REV_GTW_EVENT_MAP = {GTW_EVENT_MAP[x]: x for x in GTW_EVENT_MAP}


# 交易环境
class TrdEnv(object):
    """
    交易环境类型定义
    ..  py:class:: TrdEnv
     ..  py:attribute:: REAL
      真实环境
     ..  py:attribute:: SIMULATE
      模拟环境
    """
    REAL = "REAL"
    SIMULATE = "SIMULATE"

TRD_ENV_MAP = {TrdEnv.REAL: 1, TrdEnv.SIMULATE: 0}


# 交易大市场， 不是具体品种
class TrdMarket(object):
    """
    交易市场类型定义
    ..  py:class:: TrdMarket
     ..  py:attribute:: NONE
      未知
     ..  py:attribute:: HK
      港股交易
     ..  py:attribute:: US
      美股交易
     ..  py:attribute:: CN
      A股交易
     ..  py:attribute:: HKCC
      A股通交易
    """
    NONE = "N/A"   # 未知
    HK = "HK"      # 香港市场
    US = "US"      # 美国市场
    CN = "CN"      # 大陆市场
    HKCC = "HKCC"  # 香港A股通市场

TRD_MKT_MAP = {
    TrdMarket.NONE: 0,
    TrdMarket.HK: 1,
    TrdMarket.US: 2,
    TrdMarket.CN: 3,
    TrdMarket.HKCC: 4,
}


# 持仓方向
class PositionSide(object):
    """
    持仓方向类型定义
    ..  py:class:: PositionSide
     ..  py:attribute:: NONE
      未知
     ..  py:attribute:: LONG
      多仓
     ..  py:attribute:: SHORT
      空仓
    """
    NONE = "N/A"
    LONG = "LONG"    # 多仓
    SHORT = "SHORT"  # 空仓

POSITION_SIDE_MAP = {
    PositionSide.NONE: -1,
    PositionSide.LONG: 0,
    PositionSide.SHORT: 1,
}


# 订单类型
class OrderType(object):
    """
    订单类型定义
    ..  py:class:: OrderType
     ..  py:attribute:: NONE
      未知
     ..  py:attribute:: NORMAL
      普通订单(港股的增强限价单、A股限价委托、美股的限价单)
     ..  py:attribute:: MARKET
      市价，目前仅美股
     ..  py:attribute:: ABSOLUTE_LIMIT
      港股限价单(只有价格完全匹配才成交)
     ..  py:attribute:: AUCTION
      港股竞价单
     ..  py:attribute:: AUCTION_LIMIT
      港股竞价限价单
     ..  py:attribute:: SPECIAL_LIMIT
      港股特别限价(即市价IOC, 订单到达交易所后，或全部成交， 或部分成交再撤单， 或下单失败)
    """
    NONE = "N/A"
    NORMAL = "NORMAL"                         # 普通订单(港股的增强限价单、A股限价委托、美股的限价单)
    MARKET = "MARKET"                         # 市价，目前仅美股
    ABSOLUTE_LIMIT = "ABSOLUTE_LIMIT"         # 港股_限价(只有价格完全匹配才成交)
    AUCTION = "AUCTION"                       # 港股_竞价
    AUCTION_LIMIT = "AUCTION_LIMIT"           # 港股_竞价限价
    SPECIAL_LIMIT = "SPECIAL_LIMIT"           # 港股_特别限价(即市价IOC, 订单到达交易所后，或全部成交， 或部分成交再撤单， 或下单失败)

ORDER_TYPE_MAP = {
    OrderType.NONE: 0,
    OrderType.NORMAL: 1,
    OrderType.MARKET: 2,
    OrderType.ABSOLUTE_LIMIT: 5,
    OrderType.AUCTION: 6,
    OrderType.AUCTION_LIMIT: 7,
    OrderType.SPECIAL_LIMIT: 8,
}


# 订单状态
class OrderStatus(object):
    """
    订单状态定义
    ..  py:class:: OrderStatus
     ..  py:attribute:: NONE
      未知
     ..  py:attribute:: UNSUBMITTED
      未提交
     ..  py:attribute:: WAITING_SUBMIT
      等待提交
     ..  py:attribute:: SUBMITTING
      提交中
     ..  py:attribute:: SUBMIT_FAILED
      提交失败，下单失败
     ..  py:attribute:: SUBMITTED
      已提交，等待成交
     ..  py:attribute:: FILLED_PART
      部分成交
     ..  py:attribute:: FILLED_ALL
      全部已成
     ..  py:attribute:: CANCELLING_PART
      正在撤单部分(部分已成交，正在撤销剩余部分)
     ..  py:attribute:: CANCELLING_ALL
      正在撤单全部
     ..  py:attribute:: CANCELLED_PART
      部分成交，剩余部分已撤单
     ..  py:attribute:: CANCELLED_ALL
      全部已撤单，无成交
     ..  py:attribute:: FAILED
      下单失败，服务拒绝
     ..  py:attribute:: DISABLED
      已失效
     ..  py:attribute:: DELETED
      已删除(无成交的订单才能删除)
    """
    NONE = "N/A"                                # 未知状态
    UNSUBMITTED = "UNSUBMITTED"                 # 未提交
    WAITING_SUBMIT = "WAITING_SUBMIT"           # 等待提交
    SUBMITTING = "SUBMITTING"                   # 提交中
    SUBMIT_FAILED = "SUBMIT_FAILED"             # 提交失败，下单失败
    TIMEOUT = "TIMEOUT"                         # 处理超时，结果未知
    SUBMITTED = "SUBMITTED"                     # 已提交，等待成交
    FILLED_PART = "FILLED_PART"                 # 部分成交
    FILLED_ALL = "FILLED_ALL"                   # 全部已成
    CANCELLING_PART = "CANCELLING_PART"         # 正在撤单_部分(部分已成交，正在撤销剩余部分)
    CANCELLING_ALL = "CANCELLING_ALL"           # 正在撤单_全部
    CANCELLED_PART = "CANCELLED_PART"           # 部分成交，剩余部分已撤单
    CANCELLED_ALL = "CANCELLED_ALL"             # 全部已撤单，无成交
    FAILED = "FAILED"                           # 下单失败，服务拒绝
    DISABLED = "DISABLED"                       # 已失效
    DELETED = "DELETED"                         # 已删除，无成交的订单才能删除


ORDER_STATUS_MAP = {
    OrderStatus.NONE: -1,
    OrderStatus.UNSUBMITTED: 0,
    OrderStatus.WAITING_SUBMIT: 1,
    OrderStatus.SUBMITTING: 2,
    OrderStatus.SUBMIT_FAILED: 3,
    OrderStatus.TIMEOUT: 4,
    OrderStatus.SUBMITTED: 5,
    OrderStatus.FILLED_PART: 10,
    OrderStatus.FILLED_ALL: 11,
    OrderStatus.CANCELLING_PART: 12,
    OrderStatus.CANCELLING_ALL: 13,
    OrderStatus.CANCELLED_PART: 14,
    OrderStatus.CANCELLED_ALL: 15,
    OrderStatus.FAILED: 21,
    OrderStatus.DISABLED: 22,
    OrderStatus.DELETED: 23,
}

# 修改订单操作
class ModifyOrderOp(object):
    """
    修改订单操作类型定义
    ..  py:class:: ModifyOrderOp
     ..  py:attribute:: NONE
      未知
     ..  py:attribute:: NORMAL
      修改订单的数量、价格
     ..  py:attribute:: CANCEL
      取消订单
     ..  py:attribute:: DISABLE
      使订单失效
     ..  py:attribute:: ENABLE
      使订单生效
     ..  py:attribute:: DELETE
      删除订单
    """
    NONE = "N/A"
    NORMAL = "NORMAL"
    CANCEL = "CANCEL"
    DISABLE = "DISABLE"
    ENABLE = "ENABLE"
    DELETE = "DELETE"

MODIFY_ORDER_OP_MAP = {
    ModifyOrderOp.NONE: 0,
    ModifyOrderOp.NORMAL: 1,
    ModifyOrderOp.CANCEL: 2,
    ModifyOrderOp.DISABLE: 3,
    ModifyOrderOp.ENABLE: 4,
    ModifyOrderOp.DELETE: 5,
}

# 交易方向 (客户端下单只传Buy或Sell即可，SELL_SHORT / BUY_BACK 服务器可能会传回
class TrdSide(object):
    """
    交易方向类型定义(客户端下单只传Buy或Sell即可，SELL_SHORT / BUY_BACK 服务器可能会传回)
    ..  py:class:: TrdSide
     ..  py:attribute:: NONE
      未知
    ..  py:attribute:: BUY
      买
     ..  py:attribute:: SELL
      卖
     ..  py:attribute:: SELL_SHORT
      卖空
     ..  py:attribute:: BUY_BACK
      买回
    """
    NONE = "N/A"
    BUY = "BUY"
    SELL = "SELL"
    SELL_SHORT = "SELL_SHORT"
    BUY_BACK = "BUY_BACK"

TRD_SIDE_MAP = {
    TrdSide.NONE: 0,
    TrdSide.BUY: 1,
    TrdSide.SELL: 2,
    TrdSide.SELL_SHORT: 3,
    TrdSide.BUY_BACK: 4,
}

# 交易的支持能力，持续更新中
MKT_ENV_ENABLE_MAP = {
    (TrdMarket.HK, TrdEnv.REAL): True,
    (TrdMarket.HK, TrdEnv.SIMULATE): True,

    (TrdMarket.US, TrdEnv.REAL): True,
    (TrdMarket.US, TrdEnv.SIMULATE): True,

    (TrdMarket.HKCC, TrdEnv.REAL): True,
    (TrdMarket.HKCC, TrdEnv.SIMULATE): False,

    (TrdMarket.CN, TrdEnv.REAL): False,
    (TrdMarket.CN, TrdEnv.SIMULATE): True,
}


class TRADE(object):
    REV_TRD_MKT_MAP = {TRD_MKT_MAP[x]: x for x in TRD_MKT_MAP}
    REV_TRD_ENV_MAP = {TRD_ENV_MAP[x]: x for x in TRD_ENV_MAP}
    REV_POSITION_SIDE_MAP = {POSITION_SIDE_MAP[x]: x for x in POSITION_SIDE_MAP}
    REV_ORDER_TYPE_MAP = {ORDER_TYPE_MAP[x]: x for x in ORDER_TYPE_MAP}
    REV_TRD_SIDE_MAP = {TRD_SIDE_MAP[x]: x for x in TRD_SIDE_MAP}
    REV_ORDER_STATUS_MAP = {ORDER_STATUS_MAP[x]: x for x in ORDER_STATUS_MAP}
    REV_MODIFY_ORDER_OP_MAP = {MODIFY_ORDER_OP_MAP[x]: x for x in MODIFY_ORDER_OP_MAP}

    @staticmethod
    def check_mkt_envtype(trd_mkt, trd_env):
        if (trd_mkt, trd_env) in MKT_ENV_ENABLE_MAP:
            return MKT_ENV_ENABLE_MAP[trd_mkt, trd_env]
        return False


class SecurityReferenceType:
    """
    股票关联数据类型
    ..  py:class:: SecurityReferenceType
     ..  py:attribute:: NONE
      未知
     ..  py:attribute:: WARRANT
     相关窝轮
    """
    NONE = 'N/A'
    WARRANT = 'WARRANT'


from .pb import Qot_GetReference_pb2


STOCK_REFERENCE_TYPE_MAP = {
    SecurityReferenceType.NONE: Qot_GetReference_pb2.ReferenceType_Unknow,
    SecurityReferenceType.WARRANT: Qot_GetReference_pb2.ReferenceType_Warrant
}
