# -*- coding: utf-8 -*-
"""
    Constant collection
"""
from futu.common.pb import Qot_GetCodeChange_pb2
from futu.common.pb import Qot_StockFilter_pb2
from futu.common.pb import Qot_ModifyUserSecurity_pb2
from futu.common.pb import GetDelayStatistics_pb2
from futu.common.pb import GetUserInfo_pb2
from futu.common.pb import Common_pb2
from futu.common.pb import Notify_pb2
from futu.common.pb import Verification_pb2
from futu.common.pb import Qot_GetReference_pb2
from futu.common.pb import Qot_Common_pb2
from futu.common.pb import Trd_Common_pb2
from futu.common.pb import Qot_SetPriceReminder_pb2
from futu.common.pb import Qot_UpdatePriceReminder_pb2
from futu.common.pb import Qot_GetUserSecurityGroup_pb2
from futu.common.pb import Qot_GetOptionChain_pb2
from copy import copy
from abc import abstractmethod

class ProtoId(object):
    InitConnect = 1001  # 初始化连接
    GetGlobalState = 1002  # 获取全局状态
    Notify = 1003  # 通知推送
    KeepAlive = 1004  # 通知推送
    GetUserInfo = 1005  # 获取用户信息
    Verification = 1006  # 请求或输入验证码
    GetDelayStatistics = 1007  # 获取延迟统计
    TestCmd = 1008

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
    Trd_GetMaxTrdQtys = 2111    # 查询最大买卖数量

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
    Qot_UpdatePriceReminder = 3019 #到价提醒通知

    # 历史数据
    Qot_RequestHistoryKL = 3103  # 拉取历史K线
    Qot_RequestHistoryKLQuota = 3104  # 拉取历史K线已经用掉的额度
    Qot_RequestRehab = 3105  # 获取除权信息

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

    Qot_GetWarrant = 3210          # 拉取窝轮信息
    Qot_GetCapitalFlow = 3211          # 获取资金流向
    Qot_GetCapitalDistribution = 3212  # 获取资金分布

    Qot_GetUserSecurity = 3213  # 获取自选股分组下的股票
    Qot_ModifyUserSecurity = 3214  # 修改自选股分组下的股票
    Qot_StockFilter = 3215   # 条件选股
    Qot_GetCodeChange = 3216   # 代码变换
    Qot_GetIpoList = 3217  # 获取新股Ipo
    Qot_GetFutureInfo = 3218  # 获取期货资料
    Qot_RequestTradeDate = 3219  # 在线拉取交易日
    Qot_SetPriceReminder = 3220  # 设置到价提醒
    Qot_GetPriceReminder = 3221  # 获取到价提醒

    Qot_GetUserSecurityGroup = 3222  # 获取自选股分组
    Qot_GetMarketState = 3223  # 获取指定品种的市场状态
    All_PushId = [Notify, KeepAlive, Trd_UpdateOrder, Trd_UpdateOrderFill, Qot_UpdateBroker,
                  Qot_UpdateOrderBook, Qot_UpdateKL, Qot_UpdateRT, Qot_UpdateBasicQot, Qot_UpdateTicker, Qot_UpdatePriceReminder]

    @classmethod
    def is_proto_id_push(cls, id):
        return id in ProtoId.All_PushId


class FtEnum(object):

    def __init__(self):
        self.str_dic = self.load_dic()
        """逆转kv对"""
        self.number_dic = dict()
        for k, v in self.str_dic.items():
            self.number_dic[v] = k

    @abstractmethod
    def load_dic(self):
        return {
        }

    @classmethod
    def if_has_key(cls, str_value):
        obj = cls()
        if not isinstance(str_value, str):
            return False
        return str_value in obj.str_dic

    @classmethod
    def get_all_keys(cls):
        obj = cls()
        return ",".join([x for x in obj.str_dic.keys()])

    @classmethod
    def get_all_key_list(cls):
        obj = cls()
        key_list = list()
        for x in obj.str_dic.keys():
            key_list.append(x)
        return key_list

    @classmethod
    def to_number(cls, str_value):
        obj = cls()
        if not isinstance(str_value, str):
            return False, obj.__class__.__name__ + " input parameter must str!"

        if str_value in obj.str_dic:
            return True, obj.str_dic[str_value]
        else:
            return False, obj.__class__.__name__ + " input parameter is incorrect!"

    @classmethod
    def to_string(cls, number_value):
        obj = cls()
        if not isinstance(number_value, int):
            return False, obj.__class__.__name__ + " input parameter must int!"

        if number_value in obj.number_dic:
            return True, obj.number_dic[number_value]
        else:
            return False, str(number_value) + " cannot be converted to SortField Type!"

    @classmethod
    def to_string2(cls, number_value):
        obj = cls()
        if not isinstance(number_value, int):
            return "N/A"
        if number_value in obj.number_dic:
            return obj.number_dic[number_value]
        else:
            return "N/A"


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
        u32_t nProtoID;  //协议ID
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


class Market(FtEnum):
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
    NONE = "N/A"
    HK = "HK"
    US = "US"
    SH = "SH"
    SZ = "SZ"
    HK_FUTURE = "HK_FUTURE"

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.QotMarket_Unknown,
            self.HK: Qot_Common_pb2.QotMarket_HK_Security,
            self.US: Qot_Common_pb2.QotMarket_US_Security,
            self.SH: Qot_Common_pb2.QotMarket_CNSH_Security,
            self.SZ: Qot_Common_pb2.QotMarket_CNSZ_Security,
            self.HK_FUTURE: Qot_Common_pb2.QotMarket_HK_Future,
        }

QOT_MARKET_TO_TRD_SEC_MARKET_MAP = {
    Qot_Common_pb2.QotMarket_Unknown: Trd_Common_pb2.TrdSecMarket_Unknown,
    Qot_Common_pb2.QotMarket_CNSH_Security: Trd_Common_pb2.TrdSecMarket_CN_SH,
    Qot_Common_pb2.QotMarket_CNSZ_Security: Trd_Common_pb2.TrdSecMarket_CN_SZ,
    Qot_Common_pb2.QotMarket_HK_Security: Trd_Common_pb2.TrdSecMarket_HK,
    Qot_Common_pb2.QotMarket_HK_Future: Trd_Common_pb2.TrdSecMarket_HK,
    Qot_Common_pb2.QotMarket_US_Security: Trd_Common_pb2.TrdSecMarket_US,
}


# 市场状态
class MarketState(FtEnum):
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
    FUTURE_NIGHT_WAIT = "FUTURE_NIGHT_WAIT"         # 夜市等待开盘
    FUTURE_AFTERNOON = "FUTURE_AFTERNOON"           # 期货下午开盘
    FUTURE_SWITCH_DATE = "FUTURE_SWITCH_DATE"       # 期货切交易日
    FUTURE_OPEN = "FUTURE_OPEN"                     # 期货开盘
    FUTURE_BREAK = "FUTURE_BREAK"                   # 期货中盘休息
    FUTURE_BREAK_OVER = "FUTURE_BREAK_OVER"         # 期货休息后开盘
    FUTURE_CLOSE = "FUTURE_CLOSE"                   # 期货收盘
    STIB_AFTER_HOURS_WAIT = "STIB_AFTER_HOURS_WAIT"  #科创板的盘后撮合时段
    STIB_AFTER_HOURS_BEGIN = "STIB_AFTER_HOURS_BEGIN"  # 科创板的盘后交易开始
    STIB_AFTER_HOURS_END = "STIB_AFTER_HOURS_END"  # 科创板的盘后交易结束

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.QotMarketState_None,
            self.AUCTION: Qot_Common_pb2.QotMarketState_Auction,
            self.WAITING_OPEN: Qot_Common_pb2.QotMarketState_WaitingOpen,
            self.MORNING: Qot_Common_pb2.QotMarketState_Morning,
            self.REST: Qot_Common_pb2.QotMarketState_Rest,
            self.AFTERNOON: Qot_Common_pb2.QotMarketState_Afternoon,
            self.CLOSED: Qot_Common_pb2.QotMarketState_Closed,
            self.PRE_MARKET_BEGIN: Qot_Common_pb2.QotMarketState_PreMarketBegin,
            self.PRE_MARKET_END: Qot_Common_pb2.QotMarketState_PreMarketEnd,
            self.AFTER_HOURS_BEGIN: Qot_Common_pb2.QotMarketState_AfterHoursBegin,
            self.AFTER_HOURS_END: Qot_Common_pb2.QotMarketState_AfterHoursEnd,
            self.NIGHT_OPEN: Qot_Common_pb2.QotMarketState_NightOpen,
            self.NIGHT_END: Qot_Common_pb2.QotMarketState_NightEnd,
            self.FUTURE_DAY_OPEN: Qot_Common_pb2.QotMarketState_FutureDayOpen,
            self.FUTURE_DAY_BREAK: Qot_Common_pb2.QotMarketState_FutureDayBreak,
            self.FUTURE_DAY_CLOSE: Qot_Common_pb2.QotMarketState_FutureDayClose,
            self.FUTURE_DAY_WAIT_OPEN: Qot_Common_pb2.QotMarketState_FutureDayWaitForOpen,
            self.HK_CAS: Qot_Common_pb2.QotMarketState_HkCas,
            self.FUTURE_NIGHT_WAIT: Qot_Common_pb2.QotMarketState_FutureNightWait,
            self.FUTURE_AFTERNOON: Qot_Common_pb2.QotMarketState_FutureAfternoon,
            self.FUTURE_SWITCH_DATE: Qot_Common_pb2.QotMarketState_FutureSwitchDate,
            self.FUTURE_OPEN: Qot_Common_pb2.QotMarketState_FutureOpen,
            self.FUTURE_BREAK: Qot_Common_pb2.QotMarketState_FutureBreak,
            self.FUTURE_BREAK_OVER: Qot_Common_pb2.QotMarketState_FutureBreakOver,
            self.FUTURE_CLOSE: Qot_Common_pb2.QotMarketState_FutureClose,
            self.STIB_AFTER_HOURS_WAIT: Qot_Common_pb2.QotMarketState_StibAfterHoursWait,
            self.STIB_AFTER_HOURS_BEGIN: Qot_Common_pb2.QotMarketState_StibAfterHoursBegin,
            self.STIB_AFTER_HOURS_END: Qot_Common_pb2.QotMarketState_StibAfterHoursEnd,
        }

# 股票类型
class SecurityType(FtEnum):
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
      港股窝轮牛熊证
     ..  py:attribute:: BOND
      债券
    ..  py:attribute:: DRVT
      期权
    ..  py:attribute:: FUTURE
      期货
     ..  py:attribute:: NONE
      未知
    """
    NONE = "N/A"
    BOND = "BOND"
    BWRT = "BWRT"
    STOCK = "STOCK"
    WARRANT = "WARRANT"
    IDX = "IDX"
    ETF = "ETF"
    DRVT = "DRVT"
    FUTURE = "FUTURE"
    PLATE = "PLATE"
    PLATESET = "PLATESET"

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.SecurityType_Unknown,
            self.BOND: Qot_Common_pb2.SecurityType_Bond,
            self.BWRT: Qot_Common_pb2.SecurityType_Bwrt,
            self.STOCK: Qot_Common_pb2.SecurityType_Eqty,
            self.ETF: Qot_Common_pb2.SecurityType_Trust,
            self.WARRANT: Qot_Common_pb2.SecurityType_Warrant,
            self.IDX: Qot_Common_pb2.SecurityType_Index,
            self.PLATE: Qot_Common_pb2.SecurityType_Plate,
            self.DRVT: Qot_Common_pb2.SecurityType_Drvt,
            self.PLATESET: Qot_Common_pb2.SecurityType_PlateSet,
            self.FUTURE: Qot_Common_pb2.SecurityType_Future,
        }

# 实时数据定阅类型
class SubType(FtEnum):
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
    NONE = "N/A"
    TICKER = "TICKER"
    QUOTE = "QUOTE"
    ORDER_BOOK = "ORDER_BOOK"
    # ORDER_DETAIL = "ORDER_DETAIL"
    K_1M = "K_1M"
    K_3M = "K_3M"
    K_5M = "K_5M"
    K_15M = "K_15M"
    K_30M = "K_30M"
    K_60M = "K_60M"
    K_DAY = "K_DAY"
    K_WEEK = "K_WEEK"
    K_MON = "K_MON"
    K_QUARTER = "K_QUARTER"
    K_YEAR = "K_YEAR"
    RT_DATA = "RT_DATA"
    BROKER = "BROKER"

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.SubType_None,
            self.QUOTE: Qot_Common_pb2.SubType_Basic,
            self.ORDER_BOOK: Qot_Common_pb2.SubType_OrderBook,
            self.TICKER: Qot_Common_pb2.SubType_Ticker,
            self.BROKER: Qot_Common_pb2.SubType_Broker,
            self.RT_DATA: Qot_Common_pb2.SubType_RT,
            self.K_DAY: Qot_Common_pb2.SubType_KL_Day,
            self.K_1M: Qot_Common_pb2.SubType_KL_1Min,
            self.K_3M: Qot_Common_pb2.SubType_KL_3Min,
            self.K_5M: Qot_Common_pb2.SubType_KL_5Min,
            self.K_15M: Qot_Common_pb2.SubType_KL_15Min,
            self.K_30M: Qot_Common_pb2.SubType_KL_30Min,
            self.K_60M: Qot_Common_pb2.SubType_KL_60Min,
            self.K_WEEK: Qot_Common_pb2.SubType_KL_Week,
            self.K_MON: Qot_Common_pb2.SubType_KL_Month,
            self.K_QUARTER: Qot_Common_pb2.SubType_KL_Qurater,
            self.K_YEAR: Qot_Common_pb2.SubType_KL_Year,
        }


KLINE_SUBTYPE_LIST = [SubType.K_DAY, SubType.K_MON, SubType.K_WEEK,
                      SubType.K_1M, SubType.K_3M, SubType.K_5M, SubType.K_15M,
                      SubType.K_30M, SubType.K_60M, SubType.K_QUARTER, SubType.K_YEAR,
                      ]

# k线类型


class KLType(FtEnum):
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
    NONE = "N/A"
    K_1M = "K_1M"
    K_3M = "K_3M"
    K_5M = "K_5M"
    K_15M = "K_15M"
    K_30M = "K_30M"
    K_60M = "K_60M"
    K_DAY = "K_DAY"
    K_WEEK = "K_WEEK"
    K_MON = "K_MON"
    K_QUARTER = "K_QUARTER"
    K_YEAR = "K_YEAR"

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.KLType_Unknown,
            self.K_1M: Qot_Common_pb2.KLType_1Min,
            self.K_3M: Qot_Common_pb2.KLType_3Min,
            self.K_5M: Qot_Common_pb2.KLType_5Min,
            self.K_15M: Qot_Common_pb2.KLType_15Min,
            self.K_30M: Qot_Common_pb2.KLType_30Min,
            self.K_60M: Qot_Common_pb2.KLType_60Min,
            self.K_DAY: Qot_Common_pb2.KLType_Day,
            self.K_WEEK: Qot_Common_pb2.KLType_Week,
            self.K_MON: Qot_Common_pb2.KLType_Month,
            self.K_QUARTER: Qot_Common_pb2.KLType_Quarter,
            self.K_YEAR: Qot_Common_pb2.KLType_Year,
        }

# k线复权
class AuType(FtEnum):
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

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.RehabType_None,
            self.QFQ: Qot_Common_pb2.RehabType_Forward,
            self.HFQ: Qot_Common_pb2.RehabType_Backward,
        }

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
class TickerDirect(FtEnum):
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
    NONE = "N/A"
    BUY = "BUY"
    SELL = "SELL"
    NEUTRAL = "NEUTRAL"

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.TickerDirection_Unknown,
            self.BUY: Qot_Common_pb2.TickerDirection_Bid,
            self.SELL: Qot_Common_pb2.TickerDirection_Ask,
            self.NEUTRAL: Qot_Common_pb2.TickerDirection_Neutral,
        }

class Plate(FtEnum):
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

    def load_dic(self):
        return {
            self.ALL: Qot_Common_pb2.PlateSetType_All,
            self.INDUSTRY: Qot_Common_pb2.PlateSetType_Industry,
            self.REGION: Qot_Common_pb2.PlateSetType_Region,
            self.CONCEPT: Qot_Common_pb2.PlateSetType_Concept,
            self.OTHER: Qot_Common_pb2.PlateSetType_Other,
        }

# 股票持有者类别
class StockHolder(FtEnum):
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
    NONE = "N/A"
    INSTITUTE = "INSTITUTE"
    FUND = "FUND"
    EXECUTIVE = "EXECUTIVE"

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.HolderCategory_Unknow,
            self.INSTITUTE: Qot_Common_pb2.HolderCategory_Agency,
            self.FUND: Qot_Common_pb2.HolderCategory_Fund,
            self.EXECUTIVE: Qot_Common_pb2.HolderCategory_SeniorManager,
        }

# 期权类型
class OptionType(FtEnum):
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

    def load_dic(self):
        return {
            self.ALL: Qot_Common_pb2.OptionType_Unknown,
            self.CALL: Qot_Common_pb2.OptionType_Call,
            self.PUT: Qot_Common_pb2.OptionType_Put,
        }

# 价内价外
class OptionCondType(FtEnum):
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

    def load_dic(self):
        return {
            self.ALL: Qot_GetOptionChain_pb2.OptionCondType_Unknow,
            self.WITHIN: Qot_GetOptionChain_pb2.OptionCondType_WithIn,
            self.OUTSIDE: Qot_GetOptionChain_pb2.OptionCondType_Outside,
        }

class DarkStatus(FtEnum):
    NONE = 'N/A'
    TRADING = 'TRADING'
    END = 'END'

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.DarkStatus_None,
            self.TRADING: Qot_Common_pb2.DarkStatus_Trading,
            self.END: Qot_Common_pb2.DarkStatus_End,
        }

class PushDataType(FtEnum):
    NONE = 'N/A'
    REALTIME = 'REALTIME'
    BYDISCONN = 'BYDISCONN'
    CACHE = 'CACHE'

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.PushDataType_Unknow,
            self.REALTIME: Qot_Common_pb2.PushDataType_Realtime,
            self.BYDISCONN: Qot_Common_pb2.PushDataType_ByDisConn,
            self.CACHE: Qot_Common_pb2.PushDataType_Cache,
        }

class TickerType(FtEnum):
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
    OVERSEAS = 'OVERSEAS'

    def load_dic(self):
        return {
            self.UNKNOWN: Qot_Common_pb2.TickerType_Unknown,
            self.AUTO_MATCH: Qot_Common_pb2.TickerType_Automatch,
            self.LATE: Qot_Common_pb2.TickerType_Late,
            self.NON_AUTO_MATCH: Qot_Common_pb2.TickerType_NoneAutomatch,
            self.INTER_AUTO_MATCH: Qot_Common_pb2.TickerType_InterAutomatch,
            self.INTER_NON_AUTO_MATCH: Qot_Common_pb2.TickerType_InterNoneAutomatch,
            self.ODD_LOT: Qot_Common_pb2.TickerType_OddLot,
            self.AUCTION: Qot_Common_pb2.TickerType_Auction,
            self.BULK: Qot_Common_pb2.TickerType_Bulk,
            self.CRASH: Qot_Common_pb2.TickerType_Crash,
            self.CROSS_MARKET: Qot_Common_pb2.TickerType_CrossMarket,
            self.BULK_SOLD: Qot_Common_pb2.TickerType_BulkSold,
            self.FREE_ON_BOARD: Qot_Common_pb2.TickerType_FreeOnBoard,
            self.RULE127_OR_155: Qot_Common_pb2.TickerType_Rule127Or155,
            self.DELAY: Qot_Common_pb2.TickerType_Delay,
            self.MARKET_CENTER_CLOSE_PRICE: Qot_Common_pb2.TickerType_MarketCenterClosePrice,
            self.NEXT_DAY: Qot_Common_pb2.TickerType_NextDay,
            self.MARKET_CENTER_OPENING: Qot_Common_pb2.TickerType_MarketCenterOpening,
            self.PRIOR_REFERENCE_PRICE: Qot_Common_pb2.TickerType_PriorReferencePrice,
            self.MARKET_CENTER_OPEN_PRICE: Qot_Common_pb2.TickerType_MarketCenterOpenPrice,
            self.SELLER: Qot_Common_pb2.TickerType_Seller,
            self.T: Qot_Common_pb2.TickerType_T,
            self.EXTENDED_TRADING_HOURS: Qot_Common_pb2.TickerType_ExtendedTradingHours,
            self.CONTINGENT: Qot_Common_pb2.TickerType_Contingent,
            self.AVERAGE_PRICE: Qot_Common_pb2.TickerType_AvgPrice,
            self.OTC_SOLD: Qot_Common_pb2.TickerType_OTCSold,
            self.ODD_LOT_CROSS_MARKET: Qot_Common_pb2.TickerType_OddLotCrossMarket,
            self.DERIVATIVELY_PRICED: Qot_Common_pb2.TickerType_DerivativelyPriced,
            self.REOPENINGP_RICED: Qot_Common_pb2.TickerType_ReOpeningPriced,
            self.CLOSING_PRICED: Qot_Common_pb2.TickerType_ClosingPriced,
            self.COMPREHENSIVE_DELAY_PRICE: Qot_Common_pb2.TickerType_ComprehensiveDelayPrice,
            self.OVERSEAS: Qot_Common_pb2.TickerType_Overseas,
        }

class SysNotifyType(FtEnum):
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
    PROGRAM_STATUS = "PROGRAM_STATUS"
    CONN_STATUS = "CONN_STATUS"
    QOT_RIGHT = "QOT_RIGHT"
    API_LEVEL = "API_LEVEL"
    API_QUOTA = "API_QUOTA"

    def load_dic(self):
        return {
            self.NONE: Notify_pb2.NotifyType_None,
            self.GTW_EVENT: Notify_pb2.NotifyType_GtwEvent,
            self.PROGRAM_STATUS: Notify_pb2.NotifyType_ProgramStatus,
            self.CONN_STATUS: Notify_pb2.NotifyType_ConnStatus,
            self.QOT_RIGHT: Notify_pb2.NotifyType_QotRight,
            self.API_LEVEL: Notify_pb2.NotifyType_APILevel,
            self.API_QUOTA: Notify_pb2.NotifyType_APIQuota,
        }

class GtwEventType(FtEnum):
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
    EnableDeviceLock = "EnableDeviceLock"

    def load_dic(self):
        return {
            self.NONE: Notify_pb2.GtwEventType_None,
            self.LocalCfgLoadFailed: Notify_pb2.GtwEventType_LocalCfgLoadFailed,
            self.APISvrRunFailed: Notify_pb2.GtwEventType_APISvrRunFailed,
            self.ForceUpdate: Notify_pb2.GtwEventType_ForceUpdate,
            self.LoginFailed: Notify_pb2.GtwEventType_LoginFailed,
            self.UnAgreeDisclaimer: Notify_pb2.GtwEventType_UnAgreeDisclaimer,
            self.NetCfgMissing: Notify_pb2.GtwEventType_NetCfgMissing,
            self.KickedOut: Notify_pb2.GtwEventType_KickedOut,
            self.LoginPwdChanged: Notify_pb2.GtwEventType_LoginPwdChanged,
            self.BanLogin: Notify_pb2.GtwEventType_BanLogin,
            self.NeedPicVerifyCode: Notify_pb2.GtwEventType_NeedPicVerifyCode,
            self.NeedPhoneVerifyCode: Notify_pb2.GtwEventType_NeedPhoneVerifyCode,
            self.AppDataNotExist: Notify_pb2.GtwEventType_AppDataNotExist,
            self.NessaryDataMissing: Notify_pb2.GtwEventType_NessaryDataMissing,
            self.TradePwdChanged: Notify_pb2.GtwEventType_TradePwdChanged,
            self.EnableDeviceLock: Notify_pb2.GtwEventType_EnableDeviceLock,
        }

# 交易环境
class TrdEnv(FtEnum):
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

    def load_dic(self):
        return {
            self.REAL: Trd_Common_pb2.TrdEnv_Real,
            self.SIMULATE: Trd_Common_pb2.TrdEnv_Simulate,
        }

# 交易大市场， 不是具体品种
class TrdMarket(FtEnum):
    """
    交易市场类型定义
    ..  py:class:: TrdMarket
     ..  py:attribute:: NONE
      未知not
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
    FUTURES = "FUTURES"  # 期货市场

    def load_dic(self):
        return {
            self.NONE: Trd_Common_pb2.TrdMarket_Unknown,
            self.HK: Trd_Common_pb2.TrdMarket_HK,
            self.US: Trd_Common_pb2.TrdMarket_US,
            self.CN: Trd_Common_pb2.TrdMarket_CN,
            self.HKCC: Trd_Common_pb2.TrdMarket_HKCC,
            self.FUTURES: Trd_Common_pb2.TrdMarket_Futures,
        }

# 持仓方向
class PositionSide(FtEnum):
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

    def load_dic(self):
        return {
            self.NONE: Trd_Common_pb2.PositionSide_Unknown,
            self.LONG: Trd_Common_pb2.PositionSide_Long,
            self.SHORT: Trd_Common_pb2.PositionSide_Short,
        }

# 订单类型
class OrderType(FtEnum):
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
    # 港股_特别限价(即市价IOC, 订单到达交易所后，或全部成交， 或部分成交再撤单， 或下单失败)
    SPECIAL_LIMIT = "SPECIAL_LIMIT"
    SPECIAL_LIMIT_ALL = "SPECIAL_LIMIT_ALL"   # 港股_特别限价(要么全部成交，要么自动撤单)

    def load_dic(self):
        return {
            self.NONE: Trd_Common_pb2.OrderType_Unknown,
            self.NORMAL: Trd_Common_pb2.OrderType_Normal,
            self.MARKET: Trd_Common_pb2.OrderType_Market,
            self.ABSOLUTE_LIMIT: Trd_Common_pb2.OrderType_AbsoluteLimit,
            self.AUCTION: Trd_Common_pb2.OrderType_Auction,
            self.AUCTION_LIMIT: Trd_Common_pb2.OrderType_AuctionLimit,
            self.SPECIAL_LIMIT: Trd_Common_pb2.OrderType_SpecialLimit,
            self.SPECIAL_LIMIT_ALL: Trd_Common_pb2.OrderType_SpecialLimit_All,
        }

# 订单状态
class OrderStatus(FtEnum):
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
    FILL_CANCELLED = "FILL_CANCELLED"           # 成交被撤销，一般遇不到，意思是已经成交的订单被回滚撤销，成交无效变为废单

    def load_dic(self):
        return {
            self.NONE: Trd_Common_pb2.OrderStatus_Unknown,
            self.UNSUBMITTED: Trd_Common_pb2.OrderStatus_Unsubmitted,
            self.WAITING_SUBMIT: Trd_Common_pb2.OrderStatus_WaitingSubmit,
            self.SUBMITTING: Trd_Common_pb2.OrderStatus_Submitting,
            self.SUBMIT_FAILED: Trd_Common_pb2.OrderStatus_SubmitFailed,
            self.TIMEOUT: Trd_Common_pb2.OrderStatus_TimeOut,
            self.SUBMITTED: Trd_Common_pb2.OrderStatus_Submitted,
            self.FILLED_PART: Trd_Common_pb2.OrderStatus_Filled_Part,
            self.FILLED_ALL: Trd_Common_pb2.OrderStatus_Filled_All,
            self.CANCELLING_PART: Trd_Common_pb2.OrderStatus_Cancelling_Part,
            self.CANCELLING_ALL: Trd_Common_pb2.OrderStatus_Cancelling_All,
            self.CANCELLED_PART: Trd_Common_pb2.OrderStatus_Cancelled_Part,
            self.CANCELLED_ALL: Trd_Common_pb2.OrderStatus_Cancelled_All,
            self.FAILED: Trd_Common_pb2.OrderStatus_Failed,
            self.DISABLED: Trd_Common_pb2.OrderStatus_Disabled,
            self.DELETED: Trd_Common_pb2.OrderStatus_Deleted,
            self.FILL_CANCELLED: Trd_Common_pb2.OrderStatus_FillCancelled,
        }

class DealStatus(FtEnum):
    OK = 'OK'                 # 正常
    CANCELLED = 'CANCELLED'   # 成交被取消
    CHANGED = 'CHANGED'       # 成交被更改

    def load_dic(self):
        return {
            self.OK: Trd_Common_pb2.OrderFillStatus_OK,
            self.CANCELLED: Trd_Common_pb2.OrderFillStatus_Cancelled,
            self.CHANGED: Trd_Common_pb2.OrderFillStatus_Changed
        }


# 修改订单操作
class ModifyOrderOp(FtEnum):
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

    def load_dic(self):
        return {
            self.NONE: Trd_Common_pb2.ModifyOrderOp_Unknown,
            self.NORMAL: Trd_Common_pb2.ModifyOrderOp_Normal,
            self.CANCEL: Trd_Common_pb2.ModifyOrderOp_Cancel,
            self.DISABLE: Trd_Common_pb2.ModifyOrderOp_Disable,
            self.ENABLE: Trd_Common_pb2.ModifyOrderOp_Enable,
            self.DELETE: Trd_Common_pb2.ModifyOrderOp_Delete,
        }

# 交易方向 (客户端下单只传Buy或Sell即可，SELL_SHORT / BUY_BACK 服务器可能会传回
class TrdSide(FtEnum):
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

    def load_dic(self):
        return {
            TrdSide.NONE: Trd_Common_pb2.TrdSide_Unknown,
            TrdSide.BUY: Trd_Common_pb2.TrdSide_Buy,
            TrdSide.SELL: Trd_Common_pb2.TrdSide_Sell,
            TrdSide.SELL_SHORT: Trd_Common_pb2.TrdSide_SellShort,
            TrdSide.BUY_BACK: Trd_Common_pb2.TrdSide_BuyBack,
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

    (TrdMarket.FUTURES, TrdEnv.REAL): True,
    (TrdMarket.FUTURES, TrdEnv.SIMULATE): False
}

class TRADE(object):
    @staticmethod
    def check_mkt_envtype(trd_mkt, trd_env):
        if (trd_mkt, trd_env) in MKT_ENV_ENABLE_MAP:
            return MKT_ENV_ENABLE_MAP[trd_mkt, trd_env]
        return False


class SecurityReferenceType(FtEnum):
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
    FUTURE = 'FUTURE'

    def load_dic(self):
        return {
           self.NONE: Qot_GetReference_pb2.ReferenceType_Unknow,
           self.WARRANT: Qot_GetReference_pb2.ReferenceType_Warrant,
           self.FUTURE: Qot_GetReference_pb2.ReferenceType_Future,
        }


'''-------------------------WarrantType----------------------------'''


#
class WrtType(FtEnum):
    NONE = "N/A"                                       # 未知
    CALL = "CALL"                                      # 认购
    PUT = "PUT"                                        # 认沽
    BULL = "BULL"                                      # 牛
    BEAR = "BEAR"                                      # 熊
    INLINE = "INLINE"                                  # 界内证

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.WarrantType_Unknown,
            self.CALL: Qot_Common_pb2.WarrantType_Buy,
            self.PUT: Qot_Common_pb2.WarrantType_Sell,
            self.BULL: Qot_Common_pb2.WarrantType_Bull,
            self.BEAR: Qot_Common_pb2.WarrantType_Bear,
            self.INLINE: Qot_Common_pb2.WarrantType_InLine
        }


'''-------------------------SortField----------------------------'''


# 窝轮排序
class SortField(FtEnum):
    NONE = "N/A"                                       # 未知
    CODE = "CODE"                                      # 代码
    CUR_PRICE = "CUR_PRICE"                            # 最新价
    PRICE_CHANGE_VAL = "PRICE_CHANGE_VAL"              # 涨跌额
    CHANGE_RATE = "CHANGE_RATE"                        # 涨跌幅%
    STATUS = "STATUS"                                  # 状态
    BID_PRICE = "BID_PRICE"                            # 买入价
    ASK_PRICE = "ASK_PRICE"                            # 卖出价
    BID_VOL = "BID_VOL"                                # 买量
    ASK_VOL = "ASK_VOL"                                # 卖量
    VOLUME = "VOLUME"                                  # 成交量
    TURNOVER = "TURNOVER"                              # 成交额
    SCORE = "SCORE"                                    # 综合评分
    PREMIUM = "PREMIUM"                                # 溢价%
    EFFECTIVE_LEVERAGE = "EFFECTIVE_LEVERAGE"          # 有效杠杆
    DELTA = "DELTA"                                    # 对冲值,仅认购认沽支持该字段
    IMPLIED_VOLATILITY = "IMPLIED_VOLATILITY"          # 引伸波幅,仅认购认沽支持该字段
    TYPE = "TYPE"                                      # 类型
    STRIKE_PRICE = "STRIKE_PRICE"                      # 行权价
    BREAK_EVEN_POINT = "BREAK_EVEN_POINT"              # 打和点
    MATURITY_TIME = "MATURITY_TIME"                    # 到期日
    LIST_TIME = "LIST_TIME"                            # 上市日期
    LAST_TRADE_TIME = "LAST_TRADE_TIME"                # 最后交易日
    LEVERAGE = "LEVERAGE"                              # 杠杆比率
    IN_OUT_MONEY = "IN_OUT_MONEY"                      # 价内/价外%
    RECOVERY_PRICE = "RECOVERY_PRICE"                  # 收回价,仅牛熊证支持该字段
    CHANGE_PRICE = "CHANGE_PRICE"                      # 换股价
    CHANGE = "CHANGE"                                  # 换股比率
    STREET_RATE = "STREET_RATE"                        # 街货比%
    STREET_VOL = "STREET_VOL"                          # 街货量
    AMPLITUDE = "AMPLITUDE"                            # 振幅%
    WARRANT_NAME = "WARRANT_NAME"                      # 名称
    ISSUER = "ISSUER"                                  # 发行人
    LOT_SIZE = "LOT_SIZE"                              # 每手
    ISSUE_SIZE = "ISSUE_SIZE"                          # 发行量
    PRE_CUR_PRICE = "PRE_CUR_PRICE"  # 盘前最新价
    AFTER_CUR_PRICE = "AFTER_CUR_PRICE"  # 盘后最新价
    PRE_PRICE_CHANGE_VAL = "PRE_PRICE_CHANGE_VAL"  # 盘前涨跌额
    AFTER_PRICE_CHANGE_VAL = "AFTER_PRICE_CHANGE_VAL"  # 盘后涨跌额
    PRE_CHANGE_RATE = "PRE_CHANGE_RATE"  # 盘前涨跌幅%
    AFTER_CHANGE_RATE = "AFTER_CHANGE_RATE"  # 盘后涨跌幅%
    PRE_AMPLITUDE = "PRE_AMPLITUDE"  # 盘前振幅%
    AFTER_AMPLITUDE = "AFTER_AMPLITUDE"  # 盘后振幅%
    PRE_TURNOVER = "PRE_TURNOVER"  # 盘前成交额
    AFTER_TURNOVER = "AFTER_TURNOVER"  # 盘后成交额
    UPPER_STRIKE_PRICE = "UPPER_STRIKE_PRICE"  # 上限价，仅界内证支持该字段
    LOWER_STRIKE_PRICE = "LOWER_STRIKE_PRICE"  # 下限价，仅界内证支持该字段
    INLINE_PRICE_STATUS = "INLINE_PRICE_STATUS"  # 界内界外，仅界内证支持该字段

    LAST_SETTLE_PRICE = "LAST_SETTLE_PRICE" #期货昨结
    POSITION = "POSITION"  # 期货持仓量
    POSITION_CHANGE = "POSITION_CHANGE"  # 期货日持仓

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.SortField_Unknow,
            self.CODE: Qot_Common_pb2.SortField_Code,
            self.CUR_PRICE: Qot_Common_pb2.SortField_CurPrice,
            self.PRICE_CHANGE_VAL: Qot_Common_pb2.SortField_PriceChangeVal,
            self.CHANGE_RATE: Qot_Common_pb2.SortField_ChangeRate,
            self.STATUS: Qot_Common_pb2.SortField_Status,
            self.BID_PRICE: Qot_Common_pb2.SortField_BidPrice,
            self.ASK_PRICE: Qot_Common_pb2.SortField_AskPrice,
            self.BID_VOL: Qot_Common_pb2.SortField_BidVol,
            self.ASK_VOL: Qot_Common_pb2.SortField_AskVol,
            self.VOLUME: Qot_Common_pb2.SortField_Volume,
            self.TURNOVER: Qot_Common_pb2.SortField_Turnover,
            self.SCORE: Qot_Common_pb2.SortField_Score,
            self.PREMIUM: Qot_Common_pb2.SortField_Premium,
            self.EFFECTIVE_LEVERAGE: Qot_Common_pb2.SortField_EffectiveLeverage,
            self.DELTA: Qot_Common_pb2.SortField_Delta,
            self.IMPLIED_VOLATILITY: Qot_Common_pb2.SortField_ImpliedVolatility,
            self.TYPE: Qot_Common_pb2.SortField_Type,
            self.STRIKE_PRICE: Qot_Common_pb2.SortField_StrikePrice,
            self.BREAK_EVEN_POINT: Qot_Common_pb2.SortField_BreakEvenPoint,
            self.MATURITY_TIME: Qot_Common_pb2.SortField_MaturityTime,
            self.LIST_TIME: Qot_Common_pb2.SortField_ListTime,
            self.LAST_TRADE_TIME: Qot_Common_pb2.SortField_LastTradeTime,
            self.LEVERAGE: Qot_Common_pb2.SortField_Leverage,
            self.IN_OUT_MONEY: Qot_Common_pb2.SortField_InOutMoney,
            self.RECOVERY_PRICE: Qot_Common_pb2.SortField_RecoveryPrice,
            self.CHANGE_PRICE: Qot_Common_pb2.SortField_ChangePrice,
            self.CHANGE: Qot_Common_pb2.SortField_Change,
            self.STREET_RATE: Qot_Common_pb2.SortField_StreetRate,
            self.STREET_VOL: Qot_Common_pb2.SortField_StreetVol,
            self.AMPLITUDE: Qot_Common_pb2.SortField_Amplitude,
            self.WARRANT_NAME: Qot_Common_pb2.SortField_WarrantName,
            self.ISSUER: Qot_Common_pb2.SortField_Issuer,
            self.LOT_SIZE: Qot_Common_pb2.SortField_LotSize,
            self.ISSUE_SIZE: Qot_Common_pb2.SortField_IssueSize,
            self.PRE_CUR_PRICE: Qot_Common_pb2.SortField_PreCurPrice,
            self.AFTER_CUR_PRICE: Qot_Common_pb2.SortField_AfterCurPrice,
            self.PRE_PRICE_CHANGE_VAL: Qot_Common_pb2.SortField_PrePriceChangeVal,
            self.AFTER_PRICE_CHANGE_VAL: Qot_Common_pb2.SortField_AfterPriceChangeVal,
            self.PRE_CHANGE_RATE: Qot_Common_pb2.SortField_PreChangeRate,
            self.AFTER_CHANGE_RATE: Qot_Common_pb2.SortField_AfterChangeRate,
            self.PRE_AMPLITUDE: Qot_Common_pb2.SortField_PreAmplitude,
            self.AFTER_AMPLITUDE: Qot_Common_pb2.SortField_AfterAmplitude,
            self.PRE_TURNOVER: Qot_Common_pb2.SortField_PreTurnover,
            self.AFTER_TURNOVER: Qot_Common_pb2.SortField_AfterTurnover,
            self.UPPER_STRIKE_PRICE: Qot_Common_pb2.SortField_UpperStrikePrice,
            self.LOWER_STRIKE_PRICE: Qot_Common_pb2.SortField_LowerStrikePrice,
            self.INLINE_PRICE_STATUS: Qot_Common_pb2.SortField_InLinePriceStatus,
            self.LAST_SETTLE_PRICE: Qot_Common_pb2.SortField_LastSettlePrice,
            self.POSITION: Qot_Common_pb2.SortField_Position,
            self.POSITION_CHANGE: Qot_Common_pb2.SortField_PositionChange,
        }


'''-------------------------IpoPeriod----------------------------'''


# 窝轮上市日
class IpoPeriod(FtEnum):
    NONE = "N/A"                                       # 未知
    TODAY = "TODAY"                                    # 今日上市
    TOMORROW = "TOMORROW"                              # 明日上市
    NEXTWEEK = "NEXTWEEK"                              # 未来一周上市
    LASTWEEK = "LASTWEEK"                              # 过去一周上市
    LASTMONTH = "LASTMONTH"                            # 过去一月上市

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.IpoPeriod_Unknow,
            self.TODAY: Qot_Common_pb2.IpoPeriod_Today,
            self.TOMORROW: Qot_Common_pb2.IpoPeriod_Tomorrow,
            self.NEXTWEEK: Qot_Common_pb2.IpoPeriod_Nextweek,
            self.LASTWEEK: Qot_Common_pb2.IpoPeriod_Lastweek,
            self.LASTMONTH: Qot_Common_pb2.IpoPeriod_Lastmonth
        }


'''-------------------------PriceType----------------------------'''


# 窝轮价外/内,界内证表示界内界外
class PriceType(FtEnum):
    NONE = "N/A"                                       # 未知
    OUTSIDE = "OUTSIDE"                                # 价外,界内证表示界外
    WITH_IN = "WITH_IN"                                # 价内,界内证表示界内

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.PriceType_Unknow,
            self.OUTSIDE: Qot_Common_pb2.PriceType_Outside,
            self.WITH_IN: Qot_Common_pb2.PriceType_WithIn
        }


'''-------------------------WarrantStatus----------------------------'''


# 窝轮状态
class WarrantStatus(FtEnum):
    NONE = "N/A"                                       # 未知
    NORMAL = "NORMAL"                                  # 正常状态
    SUSPEND = "SUSPEND"                                # 停牌
    STOP_TRADE = "STOP_TRADE"                          # 终止交易
    PENDING_LISTING = "PENDING_LISTING"                # 等待上市

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.WarrantStatus_Unknow,
            self.NORMAL: Qot_Common_pb2.WarrantStatus_Normal,
            self.SUSPEND: Qot_Common_pb2.WarrantStatus_Suspend,
            self.STOP_TRADE: Qot_Common_pb2.WarrantStatus_StopTrade,
            self.PENDING_LISTING: Qot_Common_pb2.WarrantStatus_PendingListing
        }


'''-------------------------Issuer----------------------------'''


# 窝轮发行人
class Issuer(FtEnum):
    NONE = "N/A"                                       # 未知
    SG = "SG"                                          # 法兴
    BP = "BP"                                          # 法巴
    CS = "CS"                                          # 瑞信
    CT = "CT"                                          # 花旗
    EA = "EA"                                          # 东亚
    GS = "GS"                                          # 高盛
    HS = "HS"                                          # 汇丰
    JP = "JP"                                          # 摩通
    MB = "MB"                                          # 麦银
    SC = "SC"                                          # 渣打
    UB = "UB"                                          # 瑞银
    BI = "BI"                                          # 中银
    DB = "DB"                                          # 德银
    DC = "DC"                                          # 大和
    ML = "ML"                                          # 美林
    NM = "NM"                                          # 野村
    RB = "RB"                                          # 荷合
    RS = "RS"                                          # 苏皇
    BC = "BC"                                          # 巴克莱
    HT = "HT"                                          # 海通
    VT = "VT"                                          # 瑞通
    KC = "KC"                                          # 比联
    MS = "MS"                                          # 摩利
    GJ = "GJ"                                          # 国君

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.Issuer_Unknow,
            self.SG: Qot_Common_pb2.Issuer_SG,
            self.BP: Qot_Common_pb2.Issuer_BP,
            self.CS: Qot_Common_pb2.Issuer_CS,
            self.CT: Qot_Common_pb2.Issuer_CT,
            self.EA: Qot_Common_pb2.Issuer_EA,
            self.GS: Qot_Common_pb2.Issuer_GS,
            self.HS: Qot_Common_pb2.Issuer_HS,
            self.JP: Qot_Common_pb2.Issuer_JP,
            self.MB: Qot_Common_pb2.Issuer_MB,
            self.SC: Qot_Common_pb2.Issuer_SC,
            self.UB: Qot_Common_pb2.Issuer_UB,
            self.BI: Qot_Common_pb2.Issuer_BI,
            self.DB: Qot_Common_pb2.Issuer_DB,
            self.DC: Qot_Common_pb2.Issuer_DC,
            self.ML: Qot_Common_pb2.Issuer_ML,
            self.NM: Qot_Common_pb2.Issuer_NM,
            self.RB: Qot_Common_pb2.Issuer_RB,
            self.RS: Qot_Common_pb2.Issuer_RS,
            self.BC: Qot_Common_pb2.Issuer_BC,
            self.HT: Qot_Common_pb2.Issuer_HT,
            self.VT: Qot_Common_pb2.Issuer_VT,
            self.KC: Qot_Common_pb2.Issuer_KC,
            self.MS: Qot_Common_pb2.Issuer_MS,
            self.GJ: Qot_Common_pb2.Issuer_GJ
        }


'''-------------------------TradeDateType----------------------------'''


# 交易时间类型
class TradeDateType(FtEnum):
    WHOLE = "WHOLE"                                    # 全天交易
    MORNING = "MORNING"                                # 上午交易，下午休市
    AFTERNOON = "AFTERNOON"                            # 下午交易，上午休市

    def load_dic(self):
        return {
            self.WHOLE: Qot_Common_pb2.TradeDateType_Whole,
            self.MORNING: Qot_Common_pb2.TradeDateType_Morning,
            self.AFTERNOON: Qot_Common_pb2.TradeDateType_Afternoon
        }


'''-------------------------行情权限----------------------------'''


# 行情权限
class QotRight(FtEnum):
    NONE = "N/A"                                       # 未知
    BMP = "BMP"                                        # Bmp，无法订阅
    LEVEL1 = "LV1"                                  # Level1
    LEVEL2 = "LV2"                                  # Level2
    SF = "SF"
    NO = "NO"

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.QotRight_Unknow,
            self.BMP: Qot_Common_pb2.QotRight_Bmp,
            self.LEVEL1: Qot_Common_pb2.QotRight_Level1,
            self.LEVEL2: Qot_Common_pb2.QotRight_Level2,
            self.SF: Qot_Common_pb2.QotRight_SF,
            self.NO: Qot_Common_pb2.QotRight_No
        }


'''-------------------------验证码操作----------------------------'''

#


class VerificationOp(FtEnum):
    NONE = "N/A"                                       # 未知操作
    REQUEST = "REQUEST"                                # 请求验证码
    INPUT_AND_LOGIN = "INPUT_AND_LOGIN"                # 输入验证码并继续登录操作

    def load_dic(self):
        return {
            self.NONE: Verification_pb2.VerificationOp_Unknow,
            self.REQUEST: Verification_pb2.VerificationOp_Request,
            self.INPUT_AND_LOGIN: Verification_pb2.VerificationOp_InputAndLogin
        }


'''-------------------------验证码类型----------------------------'''


#
class VerificationType(FtEnum):
    NONE = "N/A"                                       # 未知操作
    PICTURE = "PICTURE"                                # 图形验证码
    PHONE = "PHONE"                                    # 手机验证码

    def load_dic(self):
        return {
            self.NONE: Verification_pb2.VerificationType_Unknow,
            self.PICTURE: Verification_pb2.VerificationType_Picture,
            self.PHONE: Verification_pb2.VerificationType_Phone
        }


'''-------------------------被强制退出登录,例如修改了登录密码,中途打开设备锁等,详细原因在描述返回----------------------------'''


class ProgramStatusType(FtEnum):
    NONE = "N/A"                                       # 未知
    # 已完成类似加载配置,启动服务器等操作,服务器启动之前的状态无需返回
    LOADED = "LOADED"
    LOGING = "LOGING"                                  # 登录中
    NEED_PIC_VERIFY_CODE = "NEED_PIC_VERIFY_CODE"      # 需要图形验证码
    NEED_PHONE_VERIFY_CODE = "NEED_PHONE_VERIFY_CODE"  # 需要手机验证码
    LOGIN_FAILED = "LOGIN_FAILED"                      # 登录失败,详细原因在描述返回
    FORCE_UPDATE = "FORCE_UPDATE"                      # 客户端版本过低
    NESSARY_DATA_PREPARING = "NESSARY_DATA_PREPARING"  # 正在拉取类似免责声明等一些必要信息
    NESSARY_DATA_MISSING = "NESSARY_DATA_MISSING"      # 缺少必要信息
    UN_AGREE_DISCLAIMER = "UN_AGREE_DISCLAIMER"        # 未同意免责声明
    READY = "READY"                                    # 可以接收业务协议收发,正常可用状态
    # OpenD登录后被强制退出登录，会导致连接全部断开,需要重连后才能得到以下该状态（并且需要在ui模式下）
    FORCE_LOGOUT = "FORCE_LOGOUT"

    def load_dic(self):
        return {
            self.NONE: Common_pb2.ProgramStatusType_None,
            self.LOADED: Common_pb2.ProgramStatusType_Loaded,
            self.LOGING: Common_pb2.ProgramStatusType_Loging,
            self.NEED_PIC_VERIFY_CODE: Common_pb2.ProgramStatusType_NeedPicVerifyCode,
            self.NEED_PHONE_VERIFY_CODE: Common_pb2.ProgramStatusType_NeedPhoneVerifyCode,
            self.LOGIN_FAILED: Common_pb2.ProgramStatusType_LoginFailed,
            self.FORCE_UPDATE: Common_pb2.ProgramStatusType_ForceUpdate,
            self.NESSARY_DATA_PREPARING: Common_pb2.ProgramStatusType_NessaryDataPreparing,
            self.NESSARY_DATA_MISSING: Common_pb2.ProgramStatusType_NessaryDataMissing,
            self.UN_AGREE_DISCLAIMER: Common_pb2.ProgramStatusType_UnAgreeDisclaimer,
            self.READY: Common_pb2.ProgramStatusType_Ready,
            self.FORCE_LOGOUT: Common_pb2.ProgramStatusType_ForceLogout
        }


class ContextStatus:
    START = 'START'
    CONNECTING = 'CONNECTING'
    READY = 'READY'
    CLOSED = 'CLOSED'


class UserInfoField:
    BASIC = 1
    API = 2
    QOTRIGHT = 4
    DISCLAIMER = 8
    UPDATE = 16
    WEBKEY = 2048

    @classmethod
    def fields_to_flag_val(cls, fields):
        list_ret = []
        for x in fields:
            if x not in list_ret:
                list_ret.append(x)

        ret_flags = 0
        for x in list_ret:
            ret_flags += x
        return ret_flags


class UpdateType(FtEnum):
    NO = "NO"
    ADVICE = "ADVICE"
    FORCE = "FORCE"

    def load_dic(self):
        return {
            self.NO: GetUserInfo_pb2.UpdateType_None,
            self.ADVICE: GetUserInfo_pb2.UpdateType_Advice,
            self.FORCE: GetUserInfo_pb2.UpdateType_Force
        }


'''-------------------------DelayStatisticsType----------------------------'''

#


class DelayStatisticsType(FtEnum):
    NONE = "N/A"                                       # 未知类型
    QOT_PUSH = "QOT_PUSH"                              # 行情推送统计
    REQ_REPLY = "REQ_REPLY"                            # 请求回应统计
    PLACE_ORDER = "PLACE_ORDER"                        # 下单统计
    ALL = [QOT_PUSH, REQ_REPLY, PLACE_ORDER]

    describe_dict = {
        QOT_PUSH: "行情推送统计",
        REQ_REPLY: "请求回应统计",
        PLACE_ORDER: "下单统计",
    }

    def load_dic(self):
        return {
            self.NONE: GetDelayStatistics_pb2.DelayStatisticsType_Unkonw,
            self.QOT_PUSH: GetDelayStatistics_pb2.DelayStatisticsType_QotPush,
            self.REQ_REPLY: GetDelayStatistics_pb2.DelayStatisticsType_ReqReply,
            self.PLACE_ORDER: GetDelayStatistics_pb2.DelayStatisticsType_PlaceOrder
        }

    @classmethod
    def get_describe(cls, t):
        obj = cls()
        return obj.describe_dict[t]


'''-------------------------QotPushStage----------------------------'''


# 某段时间的统计数据，SR表示服务器收到数据，目前只有港股支持SR字段，SS表示服务器发出数据，CR表示OpenD收到数据，CS表示OpenD发出数据
class QotPushStage(FtEnum):
    NONE = "N/A"                                       # 未知
    SR2_SS = "SR2_SS"                                  # 统计服务端处理耗时
    SS2_CR = "SS2_CR"                                  # 统计网络耗时
    CR2_CS = "CR2_CS"                                  # 统计OpenD处理耗时
    SS2_CS = "SS2_CS"                                  # 统计服务器发出到OpenD发出的处理耗时
    SR2_CS = "SR2_CS"                                  # 统计服务器收到数据到OpenD发出的处理耗时
    ALL = [SR2_SS, SS2_CR, CR2_CS, SS2_CS, SR2_CS]

    describe_dict = {
        SR2_SS: "统计服务端处理耗时",
        SS2_CR: "统计网络耗时",
        CR2_CS: "统计OpenD处理耗时",
        SS2_CS: "统计服务器发出到OpenD发出的处理耗时",
        SR2_CS: "统计服务器收到数据到OpenD发出的处理耗时(也就是从交易所到用户的总时间，港股市场数据最全，A股和美股部分缺乏交易所下发时间）",
    }

    def load_dic(self):
        return {
            self.NONE: GetDelayStatistics_pb2.QotPushStage_Unkonw,
            self.SR2_SS: GetDelayStatistics_pb2.QotPushStage_SR2SS,
            self.SS2_CR: GetDelayStatistics_pb2.QotPushStage_SS2CR,
            self.CR2_CS: GetDelayStatistics_pb2.QotPushStage_CR2CS,
            self.SS2_CS: GetDelayStatistics_pb2.QotPushStage_SS2CS,
            self.SR2_CS: GetDelayStatistics_pb2.QotPushStage_SR2CS
        }

    @classmethod
    def get_describe(cls, t):
        obj = cls()
        return obj.describe_dict[t]


'''-------------------------QotPushType----------------------------'''


# 行情推送类型
class QotPushType(FtEnum):
    NONE = "N/A"                                       # 未知
    PRICE = "PRICE"                                    # 最新价
    TICKER = "TICKER"                                  # 逐笔
    ORDER_BOOK = "ORDER_BOOK"                          # 摆盘
    BROKER = "BROKER"                                  # 经纪队列

    describe_dict = {
        PRICE: "最新价",
        TICKER: "逐笔",
        ORDER_BOOK: "摆盘",
        BROKER: "经纪队列",
    }

    def load_dic(self):
        return {
            self.NONE: GetDelayStatistics_pb2.QotPushType_Unkonw,
            self.PRICE: GetDelayStatistics_pb2.QotPushType_Price,
            self.TICKER: GetDelayStatistics_pb2.QotPushType_Ticker,
            self.ORDER_BOOK: GetDelayStatistics_pb2.QotPushType_OrderBook,
            self.BROKER: GetDelayStatistics_pb2.QotPushType_Broker
        }

    @classmethod
    def get_describe(cls, t):
        obj = cls()
        return obj.describe_dict[t]


'''-------------------------ModifyUserSecurityOp----------------------------'''


# 自选股操作
class ModifyUserSecurityOp(FtEnum):
    NONE = "N/A"                                       # 未知
    ADD = "ADD"                                        # 新增
    DEL = "DEL"                                        # 删除
    MOVE_OUT = "MOVE_OUT"                                # 移出

    def load_dic(self):
        return {
            self.NONE: Qot_ModifyUserSecurity_pb2.ModifyUserSecurityOp_Unknown,
            self.ADD: Qot_ModifyUserSecurity_pb2.ModifyUserSecurityOp_Add,
            self.DEL: Qot_ModifyUserSecurity_pb2.ModifyUserSecurityOp_Del,
            self.MOVE_OUT: Qot_ModifyUserSecurity_pb2.ModifyUserSecurityOp_MoveOut
        }


# 账户类型
class TrdAccType(FtEnum):
    NONE = 'N/A'     # 未知类型
    CASH = 'CASH'           # 现金账户
    MARGIN = 'MARGIN'       # 保证金账户

    def load_dic(self):
        return {
            self.NONE: Trd_Common_pb2.TrdAccType_Unknown,
            self.CASH: Trd_Common_pb2.TrdAccType_Cash,
            self.MARGIN: Trd_Common_pb2.TrdAccType_Margin
        }


'''-------------------------StockFilter 选股----------------------------'''


# 选股排序

class SortDir(FtEnum):
    NONE = "N/A"                                       # 不排序
    ASCEND = "ASCEND"                                  # 升序
    DESCEND = "DESCEND"                                # 降序

    def load_dic(self):
        return {
            self.NONE: Qot_StockFilter_pb2.SortDir_No,
            self.ASCEND: Qot_StockFilter_pb2.SortDir_Ascend,
            self.DESCEND: Qot_StockFilter_pb2.SortDir_Descend
        }

# 简单属性


class StockField(FtEnum):
    NONE = "N/A"                                       # 未知
    # 以下是简单数据过滤所支持的枚举
    simple_enum_begin = 0
    STOCK_CODE = "STOCK_CODE"                          # 股票代码，不能填区间上下限值。
    STOCK_NAME = "STOCK_NAME"                          # 股票名称，不能填区间上下限值。
    CUR_PRICE = "CUR_PRICE"                            # 最新价 例如填写[10,20]值区间
    # (现价 - 52周最高)/52周最高，对应PC端离52周高点百分比 例如填写[-30,-10]值区间（该字段为百分比字段，默认不展示%，如20实际对应20%，如20实际对应20%）
    CUR_PRICE_TO_HIGHEST52_WEEKS_RATIO = "CUR_PRICE_TO_HIGHEST52_WEEKS_RATIO"
    # (现价 - 52周最低)/52周最低，对应PC端离52周低点百分比 例如填写[20,40]值区间（该字段为百分比字段，默认不展示%，如20实际对应20%）
    CUR_PRICE_TO_LOWEST52_WEEKS_RATIO = "CUR_PRICE_TO_LOWEST52_WEEKS_RATIO"
    # (今日最高 - 52周最高)/52周最高 例如填写[-3,-1]值区间（该字段为百分比字段，默认不展示%，如20实际对应20%）
    HIGH_PRICE_TO_HIGHEST52_WEEKS_RATIO = "HIGH_PRICE_TO_HIGHEST52_WEEKS_RATIO"
    # (今日最低 - 52周最低)/52周最低 例如填写[10,70]值区间（该字段为百分比字段，默认不展示%，如20实际对应20%）
    LOW_PRICE_TO_LOWEST52_WEEKS_RATIO = "LOW_PRICE_TO_LOWEST52_WEEKS_RATIO"
    VOLUME_RATIO = "VOLUME_RATIO"                      # 量比 例如填写[0.5,30]值区间
    BID_ASK_RATIO = "BID_ASK_RATIO"                    # 委比 例如填写[-20,80.5]值区间（该字段为百分比字段，默认不展示%，如20实际对应20%）
    LOT_PRICE = "LOT_PRICE"                            # 每手价格 例如填写[40,100]值区间
    # 市值 例如填写[50000000,3000000000]值区间
    MARKET_VAL = "MARKET_VAL"
    # 市盈率 (静态) 例如填写[-8,65.3]值区间
    PE_ANNUAL = "PE_ANNUAL"
    # 市盈率TTM 例如填写[-10,20.5]值区间
    PE_TTM = "PE_TTM"
    PB_RATE = "PB_RATE"                                # 市净率 例如填写[0.5,20]值区间
    CHANGE_RATE_5MIN = "CHANGE_RATE_5MIN"              # 五分钟价格涨跌幅 例如填写[-5,6.3]值区间（该字段为百分比字段，默认不展示%，如20实际对应20%）
    CHANGE_RATE_BEGIN_YEAR = "CHANGE_RATE_BEGIN_YEAR"  # 年初至今价格涨跌幅 例如填写[-50.1,400.7]值区间（该字段为百分比字段，默认不展示%，如20实际对应20%）
    PS_TTM = "PS_TTM"                                  # 市销率(TTM) 例如填写 [100, 500] 值区间（该字段为百分比字段，默认省略%，如20实际对应20%）
    PCF_TTM = "PCF_TTM"                                # 市现率(TTM) 例如填写 [100, 1000] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    TOTAL_SHARE = "TOTAL_SHARE"                        # 总股数 例如填写 [1000000000,1000000000] 值区间 (单位：股)
    FLOAT_SHARE = "FLOAT_SHARE"                        # 流通股数 例如填写 [1000000000,1000000000] 值区间 (单位：股)
    FLOAT_MARKET_VAL = "FLOAT_MARKET_VAL"              # 流通市值 例如填写 [1000000000,1000000000] 值区间 (单位：元)

    # 以下是累积数据过滤所支持的枚举
    acc_enum_begin = 100
    CHANGE_RATE = "CHANGE_RATE"                        # 涨跌幅 例如填写[-10.2,20.4]值区间（该字段为百分比字段，默认不展示%，如20实际对应20%）
    AMPLITUDE = "AMPLITUDE"                            # 振幅 例如填写[0.5,20.6]值区间（该字段为百分比字段，默认不展示%，如20实际对应20%）
    VOLUME = "VOLUME"                                  # 日均成交量 例如填写[2000,70000]值区间
    TURNOVER = "TURNOVER"                              # 日均成交额 例如填写[1400,890000]值区间
    TURNOVER_RATE = "TURNOVER_RATE"                    # 换手率 例如填写[2,30]值区间（该字段为百分比字段，默认不展示%，如20实际对应20%）

    # 以下是财务数据过滤所支持的枚举
    financial_enum_begin = 200
    NET_PROFIT = "NET_PROFIT"                          # 净利润 例如填写[100000000,2500000000]值区间
    NET_PROFIX_GROWTH = "NET_PROFIX_GROWTH"            # 净利润增长率 例如填写[-10,300]值区间（该字段为百分比字段，默认不展示%，如20实际对应20%）
    SUM_OF_BUSINESS = "SUM_OF_BUSINESS"                # 营业收入 例如填写[100000000,6400000000]值区间
    SUM_OF_BUSINESS_GROWTH = "SUM_OF_BUSINESS_GROWTH"  # 营收同比增长率 例如填写[-5,200]值区间（该字段为百分比字段，默认不展示%，如20实际对应20%）
    NET_PROFIT_RATE = "NET_PROFIT_RATE"                # 净利率 例如填写[10,113]值区间（该字段为百分比字段，默认不展示%，如20实际对应20%）
    GROSS_PROFIT_RATE = "GROSS_PROFIT_RATE"            # 毛利率 例如填写[4,65]值区间（该字段为百分比字段，默认不展示%，如20实际对应20%）
    DEBT_ASSET_RATE = "DEBT_ASSET_RATE"                # 资产负债率 例如填写[5,470]值区间（该字段为百分比字段，默认不展示%，如20实际对应20%）
    RETURN_ON_EQUITY_RATE = "RETURN_ON_EQUITY_RATE"    # 净资产收益率 例如填写[20,230]值区间（该字段为百分比字段，默认不展示%，如20实际对应20%）
    ROIC = "ROIC"                                      # 盈利能力属性投入资本回报率 例如填写 [1.0,10.0] 值区间（该字段为百分比字段，默认省略%，如20实际对应20%）
    ROA_TTM = "ROA_TTM"                                # 资产回报率(TTM) 例如填写 [1.0,10.0] 值区间（该字段为百分比字段，默认省略%，如20实际对应20%。仅适用于年报。）
    EBIT_TTM = "EBIT_TTM"                              # 息税前利润(TTM) 例如填写 [1000000000,1000000000] 值区间（单位：元。仅适用于年报。）
    EBITDA = "EBITDA"                                  # 税息折旧及摊销前利润 例如填写 [1000000000,1000000000] 值区间（单位：元）
    OPERATING_MARGIN_TTM = "OPERATING_MARGIN_TTM"      # 营业利润率(TTM) 例如填写 [1.0,10.0] 值区间（该字段为百分比字段，默认省略%，如20实际对应20%。仅适用于年报。）
    EBIT_MARGIN = "EBIT_MARGIN"                        # EBIT利润率 例如填写 [1.0,10.0] 值区间（该字段为百分比字段，默认省略%，如20实际对应20%）
    EBITDA_MARGIN = "EBITDA_MARGIN"                    # EBITDA利润率 例如填写 [1.0,10.0] 值区间（该字段为百分比字段，默认省略%，如20实际对应20%）
    FINANCIAL_COST_RATE = "FINANCIAL_COST_RATE"        # 财务成本率 例如填写 [1.0,10.0] 值区间（该字段为百分比字段，默认省略%，如20实际对应20%）
    OPERATING_PROFIT_TTM = "OPERATING_PROFIT_TTM"      # 营业利润(TTM) 例如填写 [1000000000,1000000000] 值区间 （单位：元。仅适用于年报。）
    SHAREHOLDER_NET_PROFIT_TTM = "SHAREHOLDER_NET_PROFIT_TTM"  # 归属于母公司的净利润 例如填写 [1000000000,1000000000] 值区间 （单位：元。仅适用于年报。）
    NET_PROFIT_CASH_COVER_TTM = "NET_PROFIT_CASH_COVER_TTM" # 盈利中的现金收入比例 例如填写 [1.0,60.0] 值区间（该字段为百分比字段，默认省略%，如20实际对应20%。仅适用于年报。）
    CURRENT_RATIO = "CURRENT_RATIO"                    # 偿债能力属性流动比率 例如填写 [100,250] 值区间（该字段为百分比字段，默认省略%，如20实际对应20%）
    QUICK_RATIO = "QUICK_RATIO"                        # 速动比率 例如填写 [100,250] 值区间（该字段为百分比字段，默认省略%，如20实际对应20%）
    CURRENT_ASSET_RATIO = "CURRENT_ASSET_RATIO"        # 清债能力属性流动资产率 例如填写 [10,100] 值区间（该字段为百分比字段，默认省略%，如20实际对应20%）
    CURRENT_DEBT_RATIO = "CURRENT_DEBT_RATIO"          # 流动负债率 例如填写 [10,100] 值区间（该字段为百分比字段，默认省略%，如20实际对应20%）
    EQUITY_MULTIPLIER = "EQUITY_MULTIPLIER"            # 权益乘数 例如填写 [100,180] 值区间
    PROPERTY_RATIO = "PROPERTY_RATIO"                  # 产权比率 例如填写 [50,100] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    CASH_AND_CASH_EQUIVALENTS = "CASH_AND_CASH_EQUIVALENTS"  # 现金和现金等价 例如填写 [1000000000,1000000000] 值区间（单位：元）
    TOTAL_ASSET_TURNOVER = "TOTAL_ASSET_TURNOVER"      # 运营能力属性总资产周转率 例如填写 [50,100] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    FIXED_ASSET_TURNOVER = "FIXED_ASSET_TURNOVER"      # 固定资产周转率 例如填写 [50,100] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    INVENTORY_TURNOVER = "INVENTORY_TURNOVER"          # 存货周转率 例如填写 [50,100] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    OPERATING_CASH_FLOW_TTM = "OPERATING_CASH_FLOW_TTM"  # 经营活动现金流(TTM) 例如填写 [1000000000,1000000000] 值区间（单位：元。仅适用于年报。）
    ACCOUNTS_RECEIVABLE = "ACCOUNTS_RECEIVABLE"        # 应收帐款净额 例如填写 [1000000000,1000000000] 值区间 例如填写 [1000000000,1000000000] 值区间 （单位：元）
    EBIT_GROWTH_RATE = "EBIT_GROWTH_RATE"              # 成长能力属性EBIT同比增长率 例如填写 [1.0,10.0] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    OPERATING_PROFIT_GROWTH_RATE = "OPERATING_PROFIT_GROWTH_RATE"  # 营业利润同比增长率 例如填写 [1.0,10.0] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    TOTAL_ASSETS_GROWTH_RATE = "TOTAL_ASSETS_GROWTH_RATE"  # 总资产同比增长率 例如填写 [1.0,10.0] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    PROFIT_TO_SHAREHOLDERS_GROWTH_RATE = "PROFIT_TO_SHAREHOLDERS_GROWTH_RATE"  # 归母净利润同比增长率 例如填写 [1.0,10.0] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    PROFIT_BEFORE_TAX_GROWTH_RATE = "PROFIT_BEFORE_TAX_GROWTH_RATE"  # 总利润同比增长率 例如填写 [1.0,10.0] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    EPS_GROWTH_RATE = "EPS_GROWTH_RATE"                # EPS同比增长率 例如填写 [1.0,10.0] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    ROE_GROWTH_RATE = "ROE_GROWTH_RATE"                # ROE同比增长率 例如填写 [1.0,10.0] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    ROIC_GROWTH_RATE = "ROIC_GROWTH_RATE"              # ROIC同比增长率 例如填写 [1.0,10.0] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    NOCF_GROWTH_RATE = "NOCF_GROWTH_RATE"              # 经营现金流同比增长率 例如填写 [1.0,10.0] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    NOCF_PER_SHARE_GROWTH_RATE = "NOCF_PER_SHARE_GROWTH_RATE"  # 每股经营现金流同比增长率 例如填写 [1.0,10.0] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    OPERATING_REVENUE_CASH_COVER = "OPERATING_REVENUE_CASH_COVER"  # 现金流属性经营现金收入比 例如填写 [10,100] 值区间（该字段为百分比字段，默认省略%，如20实际对应20%）
    OPERATING_PROFIT_TO_TOTAL_PROFIT = "OPERATING_PROFIT_TO_TOTAL_PROFIT"  # 营业利润占比 例如填写 [10,100] 值区间 （该字段为百分比字段，默认省略%，如20实际对应20%）
    BASIC_EPS = "BASIC_EPS"                            # 市场表现属性基本每股收益 例如填写 [0.1,10] 值区间 (单位：元)
    DILUTED_EPS = "DILUTED_EPS"                        # 稀释每股收益 例如填写 [0.1,10] 值区间 (单位：元)
    NOCF_PER_SHARE = "NOCF_PER_SHARE"                  # 每股经营现金净流量 例如填写 [0.1,10] 值区间 (单位：元)

    def load_dic(self):
        return {
            # 简单
            self.NONE: self.simple_enum_begin + Qot_StockFilter_pb2.StockField_Unknown,
            self.STOCK_CODE: self.simple_enum_begin + Qot_StockFilter_pb2.StockField_StockCode,
            self.STOCK_NAME: self.simple_enum_begin + Qot_StockFilter_pb2.StockField_StockName,
            self.CUR_PRICE: self.simple_enum_begin + Qot_StockFilter_pb2.StockField_CurPrice,
            self.CUR_PRICE_TO_HIGHEST52_WEEKS_RATIO: self.simple_enum_begin + Qot_StockFilter_pb2.StockField_CurPriceToHighest52WeeksRatio,
            self.CUR_PRICE_TO_LOWEST52_WEEKS_RATIO: self.simple_enum_begin + Qot_StockFilter_pb2.StockField_CurPriceToLowest52WeeksRatio,
            self.HIGH_PRICE_TO_HIGHEST52_WEEKS_RATIO: self.simple_enum_begin + Qot_StockFilter_pb2.StockField_HighPriceToHighest52WeeksRatio,
            self.LOW_PRICE_TO_LOWEST52_WEEKS_RATIO: self.simple_enum_begin + Qot_StockFilter_pb2.StockField_LowPriceToLowest52WeeksRatio,
            self.VOLUME_RATIO: self.simple_enum_begin + Qot_StockFilter_pb2.StockField_VolumeRatio,
            self.BID_ASK_RATIO: self.simple_enum_begin + Qot_StockFilter_pb2.StockField_BidAskRatio,
            self.LOT_PRICE: self.simple_enum_begin + Qot_StockFilter_pb2.StockField_LotPrice,
            self.MARKET_VAL: self.simple_enum_begin + Qot_StockFilter_pb2.StockField_MarketVal,
            self.PE_ANNUAL: self.simple_enum_begin + Qot_StockFilter_pb2.StockField_PeAnnual,
            self.PE_TTM: self.simple_enum_begin + Qot_StockFilter_pb2.StockField_PeTTM,
            self.PB_RATE: self.simple_enum_begin + Qot_StockFilter_pb2.StockField_PbRate,
            self.CHANGE_RATE_5MIN: self.simple_enum_begin + Qot_StockFilter_pb2.StockField_ChangeRate5min,
            self.CHANGE_RATE_BEGIN_YEAR: self.simple_enum_begin + Qot_StockFilter_pb2.StockField_ChangeRateBeginYear,
            self.PS_TTM: self.simple_enum_begin + Qot_StockFilter_pb2.StockField_PSTTM,
            self.PCF_TTM: self.simple_enum_begin + Qot_StockFilter_pb2.StockField_PCFTTM,
            self.TOTAL_SHARE: self.simple_enum_begin + Qot_StockFilter_pb2.StockField_TotalShare,
            self.FLOAT_SHARE: self.simple_enum_begin + Qot_StockFilter_pb2.StockField_FloatShare,
            self.FLOAT_MARKET_VAL: self.simple_enum_begin + Qot_StockFilter_pb2.StockField_FloatMarketVal,

            # 累积
            self.CHANGE_RATE: self.acc_enum_begin + Qot_StockFilter_pb2.AccumulateField_ChangeRate,
            self.AMPLITUDE: self.acc_enum_begin + Qot_StockFilter_pb2.AccumulateField_Amplitude,
            self.VOLUME: self.acc_enum_begin + Qot_StockFilter_pb2.AccumulateField_Volume,
            self.TURNOVER: self.acc_enum_begin + Qot_StockFilter_pb2.AccumulateField_Turnover,
            self.TURNOVER_RATE: self.acc_enum_begin + Qot_StockFilter_pb2.AccumulateField_TurnoverRate,

            # 财务
            self.NET_PROFIT: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_NetProfit,
            self.NET_PROFIX_GROWTH: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_NetProfitGrowth,
            self.SUM_OF_BUSINESS: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_SumOfBusiness,
            self.SUM_OF_BUSINESS_GROWTH: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_SumOfBusinessGrowth,
            self.NET_PROFIT_RATE: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_NetProfitRate,
            self.GROSS_PROFIT_RATE: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_GrossProfitRate,
            self.DEBT_ASSET_RATE: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_DebtAssetsRate,
            self.RETURN_ON_EQUITY_RATE: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_ReturnOnEquityRate,
            self.ROIC: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_ROIC,
            self.ROA_TTM: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_ROATTM,
            self.EBIT_TTM: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_EBITTTM,
            self.EBITDA: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_EBITDA,
            self.OPERATING_MARGIN_TTM: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_OperatingMarginTTM,
            self.EBIT_MARGIN: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_EBITMargin,
            self.EBITDA_MARGIN: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_EBITDAMargin,
            self.FINANCIAL_COST_RATE: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_FinancialCostRate,
            self.OPERATING_PROFIT_TTM: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_OperatingProfitTTM,
            self.SHAREHOLDER_NET_PROFIT_TTM: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_ShareholderNetProfitTTM,
            self.NET_PROFIT_CASH_COVER_TTM: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_NetProfitCashCoverTTM,
            self.CURRENT_RATIO: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_CurrentRatio,
            self.QUICK_RATIO: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_QuickRatio,
            self.CURRENT_ASSET_RATIO: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_CurrentAssetRatio,
            self.CURRENT_DEBT_RATIO: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_CurrentDebtRatio,
            self.EQUITY_MULTIPLIER: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_EquityMultiplier,
            self.PROPERTY_RATIO: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_PropertyRatio,
            self.CASH_AND_CASH_EQUIVALENTS: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_CashAndCashEquivalents,
            self.TOTAL_ASSET_TURNOVER: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_TotalAssetTurnover,
            self.FIXED_ASSET_TURNOVER: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_FixedAssetTurnover,
            self.INVENTORY_TURNOVER: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_InventoryTurnover,
            self.OPERATING_CASH_FLOW_TTM: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_OperatingCashFlowTTM,
            self.ACCOUNTS_RECEIVABLE: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_AccountsReceivable,
            self.EBIT_GROWTH_RATE: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_EBITGrowthRate,
            self.OPERATING_PROFIT_GROWTH_RATE: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_OperatingProfitGrowthRate,
            self.TOTAL_ASSETS_GROWTH_RATE: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_TotalAssetsGrowthRate,
            self.PROFIT_TO_SHAREHOLDERS_GROWTH_RATE: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_ProfitToShareholdersGrowthRate,
            self.PROFIT_BEFORE_TAX_GROWTH_RATE: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_ProfitBeforeTaxGrowthRate,
            self.EPS_GROWTH_RATE: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_EPSGrowthRate,
            self.ROE_GROWTH_RATE: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_ROEGrowthRate,
            self.ROIC_GROWTH_RATE: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_ROICGrowthRate,
            self.NOCF_GROWTH_RATE: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_NOCFGrowthRate,
            self.NOCF_PER_SHARE_GROWTH_RATE: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_NOCFPerShareGrowthRate,
            self.OPERATING_REVENUE_CASH_COVER: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_OperatingRevenueCashCover,
            self.OPERATING_PROFIT_TO_TOTAL_PROFIT: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_OperatingProfitToTotalProfit,
            self.BASIC_EPS: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_BasicEPS,
            self.DILUTED_EPS: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_DilutedEPS,
            self.NOCF_PER_SHARE: self.financial_enum_begin + Qot_StockFilter_pb2.FinancialField_NOCFPerShare,
        }


#财务指标的周期
class FinancialQuarter(FtEnum):
    NONE = "N/A"
    ANNUAL = "ANNUAL"                            # 年报
    FIRST_QUARTER = "FIRST_QUARTER"              # Q1一季报
    INTERIM = "INTERIM"                          # Q6中期报
    THIRD_QUARTER = "THIRD_QUARTER"              # Q9三季报
    MOST_RECENT_QUARTER = "MOST_RECENT_QUARTER"  # 最近季报
    
    def load_dic(self):
        return {
            self.NONE: Qot_StockFilter_pb2.FinancialQuarter_Unknown,
            self.ANNUAL: Qot_StockFilter_pb2.FinancialQuarter_Annual,
            self.FIRST_QUARTER: Qot_StockFilter_pb2.FinancialQuarter_FirstQuarter,
            self.INTERIM: Qot_StockFilter_pb2.FinancialQuarter_Interim,
            self.THIRD_QUARTER: Qot_StockFilter_pb2.FinancialQuarter_ThirdQuarter,
            self.MOST_RECENT_QUARTER: Qot_StockFilter_pb2.FinancialQuarter_MostRecentQuarter,
        }

#
class CodeChangeType(FtEnum):
    NONE = "N/A"
    GEM_TO_MAIN = "GEM_TO_MAIN"                        # 创业板转主板
    UNPAID = "UNPAID"                                  # 买卖未缴款供股权
    CHANGE_LOT = "CHANGE_LOT"                          # 更改买卖单位
    SPLIT = "SPLIT"                                    # 拆股
    JOINT = "JOINT"                                    # 合股
    JOINT_SPLIT = "JOINT_SPLIT"                        # 股份先并后拆
    SPLIT_JOINT = "SPLIT_JOINT"                        # 股份先拆后并
    OTHER = "OTHER"                                    # 其他

    def load_dic(self):
        return {
            self.NONE: Qot_GetCodeChange_pb2.CodeChangeType_Unkown,
            self.GEM_TO_MAIN: Qot_GetCodeChange_pb2.CodeChangeType_GemToMain,
            self.UNPAID: Qot_GetCodeChange_pb2.CodeChangeType_Unpaid,
            self.CHANGE_LOT: Qot_GetCodeChange_pb2.CodeChangeType_ChangeLot,
            self.SPLIT: Qot_GetCodeChange_pb2.CodeChangeType_Split,
            self.JOINT: Qot_GetCodeChange_pb2.CodeChangeType_Joint,
            self.JOINT_SPLIT: Qot_GetCodeChange_pb2.CodeChangeType_JointSplit,
            self.SPLIT_JOINT: Qot_GetCodeChange_pb2.CodeChangeType_SplitJoint,
            self.OTHER: Qot_GetCodeChange_pb2.CodeChangeType_Other
        }

#
class TimeFilterType(FtEnum):
    NONE = "N/A"                                       # 未知
    PUBLIC = "PUBLIC"                                  # 根据公布时间过滤
    EFFECTIVE = "EFFECTIVE"                            # 根据生效时间过滤
    END = "END"                                        # 根据结束时间过滤

    def load_dic(self):
        return {
            self.NONE: Qot_GetCodeChange_pb2.TimeFilterType_Unknow,
            self.PUBLIC: Qot_GetCodeChange_pb2.TimeFilterType_Public,
            self.EFFECTIVE: Qot_GetCodeChange_pb2.TimeFilterType_Effective,
            self.END: Qot_GetCodeChange_pb2.TimeFilterType_End
        }


class TimeFilter(object):
    type = 0  # 时间筛选类型
    begin_time = ''  # 时间筛选开始点
    end_time = ''  # 时间筛选结束点

    def __init__(self, type, begin_time, end_time):
        self.type = type
        self.begin_time = begin_time
        self.end_time = end_time

#
class SecurityStatus(FtEnum):
    NONE = "N/A"                                                                 #未知
    NORMAL = "NORMAL"                                                            #正常状态
    LISTING = "LISTING"                                                          #待上市
    PURCHASING = "PURCHASING"                                                    #申购中
    SUBSCRIBING = "SUBSCRIBING"                                                  #认购中
    BEFORE_DARK_TRADE_OPEING = "BEFORE_DARK_TRADE_OPEING"                        #暗盘开盘前
    DARK_TRADING = "DARK_TRADING"                                                #暗盘交易中
    DARK_TRAD_END = "DARK_TRAD_END"                                              #暗盘已收盘
    TO_BE_OPEN = "TO_BE_OPEN"                                                    #待开盘
    SUSPENDED = "SUSPENDED"                                                      #停牌
    CALLED = "CALLED"                                                            #已收回
    EXPIRED_LAST_TRADING_DATE = "EXPIRED_LAST_TRADING_DATE"                      #已过最后交易日
    EXPIRED = "EXPIRED"                                                          #已过期
    DELISTED = "DELISTED"                                                        #已退市
    CHANGE_TO_TEMPORARY_CODE = "CHANGE_TO_TEMPORARY_CODE"                        #公司行动中，交易关闭，转至临时代码交易
    TEMPORARY_CODE_TRADE_END = "TEMPORARY_CODE_TRADE_END"                        #临时买卖结束，交易关闭
    CHANGED_PLATE_TRADE_END = "CHANGED_PLATE_TRADE_END"                          #已转板，旧代码交易关闭
    CHANGED_CODE_TRAD_END = "CHANGED_CODE_TRAD_END"                              #已换代码，旧代码交易关闭
    RECOVERABLE_CIRCUIT_BREAKER = "RECOVERABLE_CIRCUIT_BREAKER"                  #可恢复性熔断
    UNRECOVERABLE_CIRCUIT_BREAKER = "UNRECOVERABLE_CIRCUIT_BREAKER"              #不可恢复性熔断
    AFTER_COMBINATION = "AFTER_COMBINATION"                                      #盘后撮合
    AFTER_TRANSACTION = "AFTER_TRANSACTION"                                      #盘后交易

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.SecurityStatus_Unknown,
            self.NORMAL: Qot_Common_pb2.SecurityStatus_Normal,
            self.LISTING: Qot_Common_pb2.SecurityStatus_Listing,
            self.PURCHASING: Qot_Common_pb2.SecurityStatus_Purchasing,
            self.SUBSCRIBING: Qot_Common_pb2.SecurityStatus_Subscribing,
            self.BEFORE_DARK_TRADE_OPEING: Qot_Common_pb2.SecurityStatus_BeforeDrakTradeOpening,
            self.DARK_TRADING: Qot_Common_pb2.SecurityStatus_DrakTrading,
            self.DARK_TRAD_END: Qot_Common_pb2.SecurityStatus_DrakTradeEnd,
            self.TO_BE_OPEN: Qot_Common_pb2.SecurityStatus_ToBeOpen,
            self.SUSPENDED: Qot_Common_pb2.SecurityStatus_Suspended,
            self.CALLED: Qot_Common_pb2.SecurityStatus_Called,
            self.EXPIRED_LAST_TRADING_DATE: Qot_Common_pb2.SecurityStatus_ExpiredLastTradingDate,
            self.EXPIRED: Qot_Common_pb2.SecurityStatus_Expired,
            self.DELISTED: Qot_Common_pb2.SecurityStatus_Delisted,
            self.CHANGE_TO_TEMPORARY_CODE: Qot_Common_pb2.SecurityStatus_ChangeToTemporaryCode,
            self.TEMPORARY_CODE_TRADE_END: Qot_Common_pb2.SecurityStatus_TemporaryCodeTradeEnd,
            self.CHANGED_PLATE_TRADE_END: Qot_Common_pb2.SecurityStatus_ChangedPlateTradeEnd,
            self.CHANGED_CODE_TRAD_END: Qot_Common_pb2.SecurityStatus_ChangedCodeTradeEnd,
            self.RECOVERABLE_CIRCUIT_BREAKER: Qot_Common_pb2.SecurityStatus_RecoverableCircuitBreaker,
            self.UNRECOVERABLE_CIRCUIT_BREAKER: Qot_Common_pb2.SecurityStatus_UnRecoverableCircuitBreaker,
            self.AFTER_COMBINATION: Qot_Common_pb2.SecurityStatus_AfterCombination,
            self.AFTER_TRANSACTION: Qot_Common_pb2.SecurityStatus_AfterTransation
        }

#
class IndexOptionType(FtEnum):
    NONE = "N/A"                                                                 #未知
    NORMAL = "NORMAL"                                                            #正常
    SMALL = "SMALL"                                                              #小型

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.IndexOptionType_Unknown,
            self.NORMAL: Qot_Common_pb2.IndexOptionType_Normal,
            self.SMALL: Qot_Common_pb2.IndexOptionType_Small
        }


class OptionAreaType(FtEnum):
    NONE = "N/A"                                                                 #未知
    AMERICAN = "AMERICAN"                                                        #美式
    EUROPEAN = "EUROPEAN"                                                        #欧式
    BERMUDA = "BERMUDA"                                                          #百慕大

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.OptionAreaType_Unknown,
            self.AMERICAN: Qot_Common_pb2.OptionAreaType_American,
            self.EUROPEAN: Qot_Common_pb2.OptionAreaType_European,
            self.BERMUDA: Qot_Common_pb2.OptionAreaType_Bermuda
        }


class Currency(FtEnum):
    NONE = 'N/A' # 未知
    HKD = 'HKD'  # 港币
    USD = 'USD'  # 美元
    CNH = 'CNH'  # 离岸人民币

    def load_dic(self):
        return {
            self.NONE: Trd_Common_pb2.Currency_Unknown,
            self.HKD: Trd_Common_pb2.Currency_HKD,
            self.USD: Trd_Common_pb2.Currency_USD,
            self.CNH: Trd_Common_pb2.Currency_CNH
        }

class CltRiskLevel(FtEnum):
    NONE = 'N/A'    # 未知
    SAFE = 'SAFE'   # 安全
    WARNING = 'WARNING'     # 预警
    DANGER = 'DANGER'       # 危险
    ABSOLUTE_SAFE = 'ABSOLUTE_SAFE'     # 绝对安全
    OPT_DANGER = 'OPT_DANGER'           # 危险，期权相关

    def load_dic(self):
        return {
            self.NONE: Trd_Common_pb2.CltRiskLevel_Unknown,
            self.SAFE: Trd_Common_pb2.CltRiskLevel_Safe,
            self.WARNING: Trd_Common_pb2.CltRiskLevel_Warning,
            self.DANGER: Trd_Common_pb2.CltRiskLevel_Danger,
            self.ABSOLUTE_SAFE: Trd_Common_pb2.CltRiskLevel_AbsoluteSafe,
            self.OPT_DANGER: Trd_Common_pb2.CltRiskLevel_OptDanger
        }


class CltRiskStatus(FtEnum):
    NONE = 'N/A'
    LEVEL1 = 'LEVEL1'
    LEVEL2 = 'LEVEL2'
    LEVEL3 = 'LEVEL3'
    LEVEL4 = 'LEVEL4'
    LEVEL5 = 'LEVEL5'
    LEVEL6 = 'LEVEL6'
    LEVEL7 = 'LEVEL7'
    LEVEL8 = 'LEVEL8'
    LEVEL9 = 'LEVEL9'

    def load_dic(self):
        return {
            self.NONE: Trd_Common_pb2.CltRiskStatus_Unknown,
            self.LEVEL1: Trd_Common_pb2.CltRiskStatus_Level1,
            self.LEVEL2: Trd_Common_pb2.CltRiskStatus_Level2,
            self.LEVEL3: Trd_Common_pb2.CltRiskStatus_Level3,
            self.LEVEL4: Trd_Common_pb2.CltRiskStatus_Level4,
            self.LEVEL5: Trd_Common_pb2.CltRiskStatus_Level5,
            self.LEVEL6: Trd_Common_pb2.CltRiskStatus_Level6,
            self.LEVEL7: Trd_Common_pb2.CltRiskStatus_Level7,
            self.LEVEL8: Trd_Common_pb2.CltRiskStatus_Level8,
            self.LEVEL9: Trd_Common_pb2.CltRiskStatus_Level9,
        }

class TradeDateMarket(FtEnum):
    NONE = 'N/A'  # 未知
    HK = 'HK'  # 港股市场
    US = 'US'  # 美股市场
    CN = 'CN'  # A股市场
    NT = 'NT'  # 深（沪）股通
    ST = 'ST'  # 港股通（深、沪）

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.TradeDateMarket_Unknown,
            self.HK: Qot_Common_pb2.TradeDateMarket_HK,
            self.US: Qot_Common_pb2.TradeDateMarket_US,
            self.CN: Qot_Common_pb2.TradeDateMarket_CN,
            self.NT: Qot_Common_pb2.TradeDateMarket_NT,
            self.ST: Qot_Common_pb2.TradeDateMarket_ST
        }

class SetPriceReminderOp(FtEnum):
    NONE = "N/A"                                       # 未知
    ADD = "ADD"                                        # 新增
    DEL = "DEL"                                        # 删除
    ENABLE = "ENABLE"                                  # 启用
    DISABLE = "DISABLE"                                # 禁用
    MODIFY = "MODIFY"                                  # 修改
    DEL_ALL = "DEL_ALL"                                # 删除某支股票下所有到价提醒

    def load_dic(self):
        return {
            self.NONE: Qot_SetPriceReminder_pb2.SetPriceReminderOp_Unknown,
            self.ADD: Qot_SetPriceReminder_pb2.SetPriceReminderOp_Add,
            self.DEL: Qot_SetPriceReminder_pb2.SetPriceReminderOp_Del,
            self.ENABLE: Qot_SetPriceReminder_pb2.SetPriceReminderOp_Enable,
            self.DISABLE: Qot_SetPriceReminder_pb2.SetPriceReminderOp_Disable,
            self.MODIFY: Qot_SetPriceReminder_pb2.SetPriceReminderOp_Modify,
            self.DEL_ALL: Qot_SetPriceReminder_pb2.SetPriceReminderOp_DelAll,
        }

class PriceReminderFreq(FtEnum):
    NONE = "N/A"                                       # 未知
    ALWAYS = "ALWAYS"                                  # 持续提醒
    ONCE_A_DAY = "ONCE_A_DAY"                          # 每日一次
    ONCE = "ONCE"                                      # 仅提醒一次

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.PriceReminderFreq_Unknown,
            self.ALWAYS: Qot_Common_pb2.PriceReminderFreq_Always,
            self.ONCE_A_DAY: Qot_Common_pb2.PriceReminderFreq_OnceADay,
            self.ONCE: Qot_Common_pb2.PriceReminderFreq_OnlyOnce,
        }

class PriceReminderType(FtEnum):
    NONE = "N/A"
    PRICE_UP = "PRICE_UP"  # 当前价涨到
    PRICE_DOWN = "PRICE_DOWN"  # 当前价跌到
    CHANGE_RATE_UP = "CHANGE_RATE_UP"  # 当前涨幅
    CHANGE_RATE_DOWN = "CHANGE_RATE_DOWN"  # 当前跌幅
    FIVE_MIN_CHANGE_RATE_UP = "FIVE_MIN_CHANGE_RATE_UP"  # 5分钟涨幅
    FIVE_MIN_CHANGE_RATE_DOWN = "FIVE_MIN_CHANGE_RATE_DOWN"  # 5分钟跌幅
    VOLUME_UP = "VOLUME_UP"  # 成交量大于
    TURNOVER_UP = "TURNOVER_UP"  # 成交额大于
    TURNOVER_RATE_UP = "TURNOVER_RATE_UP"  # 换手率大于
    BID_PRICE_UP = "BID_PRICE_UP"  # 买一价高于
    ASK_PRICE_DOWN = "ASK_PRICE_DOWN"  # 卖一价低于
    BID_VOL_UP = "BID_VOL_UP"  # 买一量高于
    ASK_VOL_UP = "ASK_VOL_UP"  # 卖一量高于

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.PriceReminderFreq_Unknown,
            self.PRICE_UP: Qot_Common_pb2.PriceReminderType_PriceUp,
            self.PRICE_DOWN: Qot_Common_pb2.PriceReminderType_PriceDown,
            self.CHANGE_RATE_UP: Qot_Common_pb2.PriceReminderType_ChangeRateUp,
            self.CHANGE_RATE_DOWN: Qot_Common_pb2.PriceReminderType_ChangeRateDown,
            self.FIVE_MIN_CHANGE_RATE_UP: Qot_Common_pb2.PriceReminderType_5MinChangeRateUp,
            self.FIVE_MIN_CHANGE_RATE_DOWN: Qot_Common_pb2.PriceReminderType_5MinChangeRateDown,
            self.VOLUME_UP: Qot_Common_pb2.PriceReminderType_VolumeUp,
            self.TURNOVER_UP: Qot_Common_pb2.PriceReminderType_TurnoverUp,
            self.TURNOVER_RATE_UP: Qot_Common_pb2.PriceReminderType_TurnoverRateUp,
            self.BID_PRICE_UP: Qot_Common_pb2.PriceReminderType_BidPriceUp,
            self.ASK_PRICE_DOWN: Qot_Common_pb2.PriceReminderType_AskPriceDown,
            self.BID_VOL_UP: Qot_Common_pb2.PriceReminderType_BidVolUp,
            self.ASK_VOL_UP: Qot_Common_pb2.PriceReminderType_AskVolUp,
        }

class PriceReminderMarketStatus(FtEnum):
    NONE = "N/A"
    OPEN = "OPEN"
    US_PRE = "US_PRE"
    US_AFTER = "US_AFTER"

    def load_dic(self):
        return {
            self.NONE: Qot_UpdatePriceReminder_pb2.MarketStatus_Unknow,
            self.OPEN: Qot_UpdatePriceReminder_pb2.MarketStatus_Open,
            self.US_PRE: Qot_UpdatePriceReminder_pb2.MarketStatus_USPre,
            self.US_AFTER: Qot_UpdatePriceReminder_pb2.MarketStatus_USAfter,
        }


# 自选股的类型
class UserSecurityGroupType(FtEnum):
    NONE = "N/A"                                       # 未知
    CUSTOM = "CUSTOM"                                  # 自定义分组
    SYSTEM = "SYSTEM"                                  # 系统分组
    ALL = "ALL"                                        # 全部分组

    def load_dic(self):
        return {
            self.NONE: Qot_GetUserSecurityGroup_pb2.GroupType_Unknown,
            self.CUSTOM: Qot_GetUserSecurityGroup_pb2.GroupType_Custom,
            self.SYSTEM: Qot_GetUserSecurityGroup_pb2.GroupType_System,
            self.ALL: Qot_GetUserSecurityGroup_pb2.GroupType_All
        }

# 资产类别
class AssetClass(FtEnum):
    NONE = "N/A"  # 未知
    STOCK = "STOCK"  # 股票
    BOND = "BOND" # 债券
    COMMODITY = "COMMODITY"  # 商品
    CURRENCY_MARKET = "CURRENCY_MARKET"  # 货币市场
    FUTURE = "FUTURE"  # 期货
    SWAP = "SWAP"  # 掉期

    def load_dic(self):
        return {
            self.NONE: Qot_Common_pb2.AssetClass_Unknow,
            self.STOCK: Qot_Common_pb2.AssetClass_Stock,
            self.BOND: Qot_Common_pb2.AssetClass_Bond,
            self.COMMODITY: Qot_Common_pb2.AssetClass_Commodity,
            self.CURRENCY_MARKET: Qot_Common_pb2.AssetClass_CurrencyMarket,
            self.FUTURE: Qot_Common_pb2.AssetClass_Future,
            self.SWAP: Qot_Common_pb2.AssetClass_Swap,
        }


# 订单有效期
class TimeInForce(FtEnum):
    DAY = 'DAY'   # 当日有效
    GTC = 'GTC'   # 撤单前有效

    def load_dic(self):
        return {
            self.DAY: Trd_Common_pb2.TimeInForce_DAY,
            self.GTC: Trd_Common_pb2.TimeInForce_GTC
        }


# 券商
class SecurityFirm(FtEnum):
    NONE = 'N/A'
    FUTUSECURITIES = 'FUTUSECURITIES'
    FUTUINC = 'FUTUINC'

    def load_dic(self):
        return {
            self.NONE: Trd_Common_pb2.SecurityFirm_Unknown,
            self.FUTUSECURITIES: Trd_Common_pb2.SecurityFirm_FutuSecurities,
            self.FUTUINC: Trd_Common_pb2.SecurityFirm_FutuInc
        }

# 模拟交易账号类型
class SimAccType(FtEnum):
    NONE = 'N/A'
    STOCK = 'STOCK'
    OPTION = 'OPTION'

    def load_dic(self):
        return {
            self.NONE: Trd_Common_pb2.SimAccType_Unknown,
            self.STOCK: Trd_Common_pb2.SimAccType_Stock,
            self.OPTION: Trd_Common_pb2.SimAccType_Option
        }
