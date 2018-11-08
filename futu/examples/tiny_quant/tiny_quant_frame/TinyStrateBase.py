# encoding: UTF-8

'''

'''
from abc import abstractmethod
from datetime import datetime
from .TinyDefine import *
# from .vnpyInc import *
import futu as ft


class TinyStrateBase(object):
    """策略名称, setting.json中作为该策略配置的key"""
    name = 'tiny_strate_base'

    """策略需要用到行情数据的股票池"""
    symbol_pools = ['HK.00700', 'HK.00001']

    def __init__(self):
        # 这里没有用None,因为None在 __loadSetting中当作错误参数检查用了
        self._quant_frame = 0
        self._event_engine = 0
        self._market_opened= False

    @abstractmethod
    def on_init_strate(self):
        """策略加载完配置后的回调
        1. 可修改symbol_pools 或策略内部其它变量的初始化
        2. 此时还不能调用futu api的接口
        """
        pass

    @abstractmethod
    def on_start(self):
        """策略启动完成后的回调
        1. 框架已经完成初始化， 可调用任意的futu api接口
        2. 修改symbol_pools无效, 不会有动态的行情数据回调
        """
        pass

    @abstractmethod
    def on_quote_changed(self, tiny_quote):
        """报价、摆盘实时数据变化时，会触发该回调"""
        # TinyQuoteData
        data = tiny_quote
        str_log = "on_quote_changed symbol=%s open=%s high=%s close=%s low=%s" % (data.symbol, data.openPrice, data.highPrice, data.lastPrice, data.lowPrice)
        self.log(str_log)

    @abstractmethod
    def on_bar_min1(self, tiny_bar):
        """每一分钟触发一次回调"""
        bar = tiny_bar
        dt = bar.datetime.strftime("%Y%m%d %H:%M:%S")
        str_log = "on_bar_min1 symbol=%s open=%s high=%s close=%s low=%s vol=%s dt=%s" % (
            bar.symbol, bar.open, bar.high, bar.close, bar.low, bar.volume, dt)
        self.log(str_log)

    @abstractmethod
    def on_bar_day(self, tiny_bar):
        """收盘时会触发一次日k数据推送"""
        bar = tiny_bar
        dt = bar.datetime.strftime("%Y%m%d %H:%M:%S")
        str_log = "on_bar_day symbol=%s open=%s high=%s close=%s low=%s vol=%s dt=%s" % (
            bar.symbol, bar.open, bar.high, bar.close, bar.low, bar.volume, dt)
        self.log(str_log)

    @abstractmethod
    def on_before_trading(self, date_time):
        """开盘时触发一次回调, 脚本挂机切换交易日时，港股会在09:30:00回调"""
        str_log = "on_before_trading - %s" % date_time.strftime('%Y-%m-%d %H:%M:%S')
        self.log(str_log)

    @abstractmethod
    def on_after_trading(self, date_time):
        """收盘时触发一次回调, 脚本挂机时，港股会在16:00:00回调"""
        str_log = "on_after_trading - %s" % date_time.strftime('%Y-%m-%d %H:%M:%S')
        self.log(str_log)

    def get_rt_tiny_quote(self, symbol):
        """得到股票的实时行情数据"""
        return self._quant_frame.get_rt_tiny_quote(symbol)

    def get_kl_min1_am(self, symbol):
        """一分钟k线的array manager数据"""
        return self._quant_frame.get_kl_min1_am(symbol)

    def get_kl_day_am(self, symbol):
        """日k线的array manager数据"""
        return self._quant_frame.get_kl_day_am(symbol)

    def buy(self, price, volume, symbol, order_type=ft.OrderType.NORMAL, adjust_limit=0, acc_id=0):
        """买入
        :param price: 报价，浮点数 精度0.001
        :param volume: 数量（股）
        :param symbol: 股票 eg: 'HK.00700'
        :param order_type: 订单类型
        :param adjust_limit: 当非0时，会自动调整报价，以符合价位表要求， 但不会超过指定的幅度, 为0时不调整报价
        :param acc_id: int, 交易账户id, 为0时取第1个可交易账户
        :return: (ret, data)
        ret == 0 , data = order_id
        ret != 0 , data = 错误字符串
        """
        return self._quant_frame.buy(price, volume, symbol, order_type, adjust_limit, acc_id)

    def sell(self, price, volume, symbol, order_type=ft.OrderType.NORMAL, adjust_limit=0, acc_id=0):
        """卖出
        :param price: 报价，浮点数 精度0.001
        :param volume: 数量（股）
        :param symbol: 股票 eg: 'HK.00700'
        :param order_type: 订单类型
        :param adjust_limit: 当非0时，会自动调整报价，以符合价位表要求， 但不会超过指定的幅度, 为0时不调整报价
        :param acc_id: int, 交易账户id, 为0时取第1个可交易账户
        :return: (ret, data)
        ret == 0 , data = order_id
        ret != 0 , data = 错误字符串
        """
        return self._quant_frame.sell(price, volume, symbol, order_type, adjust_limit, acc_id)

    def cancel_order(self, order_id):
        """取消订单
        :return: (ret, data)
        ret == 0 , data = '' 空串
        ret != 0 , data = 错误字符串
        """
        return self._quant_frame.cancel_order(order_id)

    def get_tiny_trade_order(self, order_id):
        """
        通过订单id得到详细的订单信息
        :param order_id:
        :return: (ret, data)
        ret == 0 , data = TinyTradeOrder 对象
        ret != 0 , data = 错误字符串
        """
        return self._quant_frame.get_tiny_trade_order(order_id)

    def get_tiny_position(self, symbol):
        '''
        得到股票的持仓信息
        :param symbol: 股票code
        :return: TinyPosition 对象，找不到就返回None
        '''
        return self._quant_frame.get_tiny_position(symbol)

    def log(self, content):
        """写log的接口"""
        content = self.name + ':' + content
        if self._quant_frame is not None:
            self._quant_frame.writeCtaLog(content)

    def init_strate(self, global_setting, quant_frame, event_engine):
        """TinyQuantFrame 初始化策略的接口"""

        if type(self._quant_frame) is not int:
            return True

        self._quant_frame = quant_frame
        self._event_engine = event_engine
        init_ret = self.__loadSetting(global_setting)

        # 注册事件
        self._event_engine.register(EVENT_BEFORE_TRADING, self.__event_before_trading)
        self._event_engine.register(EVENT_AFTER_TRADING, self.__event_after_trading)
        self._event_engine.register(EVENT_QUOTE_CHANGE, self.__event_quote_change)
        self._event_engine.register(EVENT_CUR_KLINE_BAR, self.__event_cur_kline_bar)

        self.log("init_strate '%s' ret = %s" % (self.name, init_ret))

        # 对外通知初始化事件
        self.on_init_strate()

        return init_ret

    def __loadSetting(self, global_setting):
        # 从json配置中读取数据
        if self.name not in global_setting:
            str_error = "setting.json - no config '%s'!" % self.name
            raise Exception(str_error)

        cta_setting = global_setting[self.name]

        d = self.__dict__
        for key in d.keys():
            if key in cta_setting.keys():
                d[key] = cta_setting[key]

        # check paramlist
        for key in d.keys():
            if d[key] is None:
                str_error = "setting.json - '%s' config no key:'%s'" % (self.name, key)
                raise Exception(str_error)

        return True

    def __event_before_trading(self, event):
        self._market_opened= True
        date_time = datetime.fromtimestamp(int(event.dict_['timestamp']))
        self.on_before_trading(date_time)

    def __event_after_trading(self, event):
        self._market_opened= False
        date_time = datetime.fromtimestamp(int(event.dict_['timestamp']))

        self.on_after_trading(date_time)

    def __event_quote_change(self, event):
        # 没开盘不向外推送数据
        if not self._market_opened:
            return

        tiny_quote = event.dict_['data']
        self.on_quote_changed(tiny_quote)

    def __event_cur_kline_bar(self, event):
        symbol = event.dict_['symbol']
        bar = event.dict_['data']
        ktype = event.dict_['ktype']

        if ktype == KTYPE_MIN1:
            self.on_bar_min1(bar)
        elif ktype == KTYPE_DAY:
            self.on_bar_day(bar)






