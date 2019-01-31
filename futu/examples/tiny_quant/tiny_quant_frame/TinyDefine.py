# encoding: UTF-8

'''
    TinyQuant定义的结构
'''

from __future__ import division
import threading
import futu as ft
from .event.eventEngine import *

EVENT_TINY_LOG = 'tiny_quant_log'
EVENT_INI_FUTU_API = 'init futu api'

EVENT_BEFORE_TRADING = 'before trading'
EVENT_AFTER_TRADING = 'after trading'
EVENT_AFTER_TRADING_FINAL = 'after trading final'

EVENT_TINY_TICK = 'tiny tick'
EVENT_QUOTE_CHANGE ='tiny quote data change'

EVENT_CUR_KLINE_PUSH = 'cur kline push'
EVENT_CUR_KLINE_BAR = 'kline min1 bar'

MARKET_HK = ft.Market.HK
MARKET_US = ft.Market.US
MARKET_SH = ft.Market.SH
MARKET_SZ = ft.Market.SZ

# futu api k线定阅类型转定义
KTYPE_DAY = ft.KLType.K_DAY
KTYPE_MIN1 = ft.KLType.K_1M
KTYPE_MIN5 = ft.KLType.K_5M
KTYPE_MIN15 = ft.KLType.K_15M
KTYPE_MIN30 = ft.KLType.K_30M
KTYPE_MIN60 = ft.KLType.K_60M

TRADE_DIRECT_BUY = ft.TrdSide.BUY
TRADE_DIRECT_SELL = ft.TrdSide.SELL

# 定义array_manager中的kline数据最大个数
MAP_KLINE_SIZE = {KTYPE_DAY: 200,
                  KTYPE_MIN1: 3000,
                  KTYPE_MIN5: 1000,
                  KTYPE_MIN15: 500,
                  KTYPE_MIN30: 500,
                  KTYPE_MIN60: 500,
                  }


class GLOBAL(object):
    """ datetime.strptime 有线程安全问题"""
    dt_lock = threading.RLock()

class TinyQuoteData(object):
    """行情数据类"""
    def __init__(self):
        # 代码相关
        self.symbol = ''  # 合约代码

        # 成交数据
        self.lastPrice = 0  # 最新成交价
        self.volume = 0  # 今天总成交量
        self.time = ''  # 时间 11:20:56.0
        self.date = ''  # 日期 20151009
        self.datetime = None

        # 常规行情
        self.openPrice = 0  # 今日开盘价
        self.highPrice = 0  # 今日最高价
        self.lowPrice = 0  # 今日最低价
        self.preClosePrice = 0

        # 五档行情
        self.bidPrice1 = 0
        self.bidPrice2 = 0
        self.bidPrice3 = 0
        self.bidPrice4 = 0
        self.bidPrice5 = 0

        self.askPrice1 = 0
        self.askPrice2 = 0
        self.askPrice3 = 0
        self.askPrice4 = 0
        self.askPrice5 = 0

        self.bidVolume1 = 0
        self.bidVolume2 = 0
        self.bidVolume3 = 0
        self.bidVolume4 = 0
        self.bidVolume5 = 0

        self.askVolume1 = 0
        self.askVolume2 = 0
        self.askVolume3 = 0
        self.askVolume4 = 0
        self.askVolume5 = 0
        self.priceSpread = 0  #摆盘的价差


class TinyBarData(object):
    """K线数据"""

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        super(TinyBarData, self).__init__()

        self.symbol = ''  # 代码

        self.open = 0
        self.high = 0
        self.low = 0
        self.close = 0
        self.volume = 0  # 成交量
        self.datetime = None


class TinyTradeOrder(object):
    """订单信息"""
    def __init__(self):
        """Constructor"""
        super(TinyTradeOrder, self).__init__()

        self.symbol = ''          # 代码
        self.order_id = ''        # futu 订单ID
        self.direction = ''       # 方向
        self.price = 0            # 报价
        self.total_volume = 0     # 总数量
        self.trade_volume = 0     # 成交数量
        self.create_time = ''     # 创建时间
        self.updated_time = ''    # 更新时间
        self.trade_avg_price = 0  # 成交均价
        self.order_status = 0     # 订单状态 0=服务器处理中 1=等待成交 2=部分成交 3=全部成交 4=已失效 5=下单失败 6=已撤单 7=已删除 8=等待开盘


class TinyPosition(object):
    """持仓信息"""
    def __init__(self):
        super(TinyPosition, self).__init__()

        self.symbol = ''
        self.position = 0
        self.frozen = 0
        self.price = 0
        self.market_value = 0

