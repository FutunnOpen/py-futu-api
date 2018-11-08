# encoding: UTF-8

'''
    实盘策略范例，接口用法见注释及范例代码
'''
import talib
from TinyStrateBase import *

class TinyStrateSample(TinyStrateBase):
    """策略名称, setting.json中作为该策略配置的key"""
    name = 'tiny_strate_sample'

    """策略需要用到行情数据的股票池"""
    symbol_pools = ['HK.00700', 'HK.00001']

    def __init__(self):
       super(TinyStrateSample, self).__init__()

       """请在setting.json中配置参数"""
       self.param1 = None
       self.param2 = None

    def on_init_strate(self):
        """策略加载完配置"""
        pass

    def on_start(self):
        """策略启动入口"""
        self.log("on_start param1=%s param2=%s" %(self.param1, self.param2))

        """交易接口测试
        ret, data = self.buy(4.60, 1000, 'HK.03883')
        if 0 == ret:
            order_id = data
            ret, data = self.get_tiny_trade_order(order_id)
            if 0 == ret:
                str_info = ''
                for key in data.__dict__.keys():
                    str_info += "%s='%s' " % (key, data.__dict__[key])
                print str_info

        ret, data = self.sell(11.4, 1000, 'HK.01357')
        if 0 == ret:
            order_id = data
            self.cancel_order(order_id)
        """

    def on_quote_changed(self, tiny_quote):
        """报价、摆盘实时数据变化时，会触发该回调"""
        # TinyQuoteData
        data = tiny_quote
        symbol = data.symbol
        str_dt = data.datetime.strftime("%Y%m%d %H:%M:%S")

        # 得到日k数据的ArrayManager(vnpy)对象
        am = self.get_kl_day_am(data.symbol)
        array_high = am.high
        array_low = am.low
        array_open = am.open
        array_close = am.close
        array_vol = am.volume

        n = 5
        ma_high = self.sma(array_high, n)
        ma_low = self.sma(array_low, n)
        ma_open = self.sma(array_open, n)
        ma_close = self.sma(array_close, n)
        ma_vol = self.sma(array_vol, n)

        str_log = "on_quote_changed symbol=%s dt=%s sma(%s) open=%s high=%s close=%s low=%s vol=%s" % (
                    symbol, str_dt, n, ma_open, ma_high, ma_close, ma_low, ma_vol)
        self.log(str_log)

    def on_bar_min1(self, tiny_bar):
        """每一分钟触发一次回调"""
        bar = tiny_bar
        symbol = bar.symbol
        str_dt = bar.datetime.strftime("%Y%m%d %H:%M:%S")

        # 得到分k数据的ArrayManager(vnpy)对象
        am = self.get_kl_min1_am(symbol)
        array_high = am.high
        array_low = am.low
        array_open = am.open
        array_close = am.close
        array_vol = am.volume

        n = 5
        ma_high = self.ema(array_high, n)
        ma_low = self.ema(array_low, n)
        ma_open = self.ema(array_open, n)
        ma_close = self.ema(array_close, n)
        ma_vol = self.ema(array_vol, n)

        str_log = "on_bar_min1 symbol=%s dt=%s ema(%s) open=%s high=%s close=%s low=%s vol=%s" % (
            symbol, str_dt, n, ma_open, ma_high, ma_close, ma_low, ma_vol)
        self.log(str_log)

    def on_bar_day(self, tiny_bar):
        """收盘时会触发一次日k回调"""
        bar = tiny_bar
        symbol = bar.symbol
        str_dt = bar.datetime.strftime("%Y%m%d %H:%M:%S")
        str_log = "on_bar_day symbol=%s dt=%s  open=%s high=%s close=%s low=%s vol=%s" % (
            symbol, str_dt, bar.open, bar.high, bar.close, bar.low, bar.volume)
        self.log(str_log)

    def on_before_trading(self, date_time):
        """开盘时触发一次回调, 港股是09:30:00"""
        str_log = "on_before_trading - %s" % date_time.strftime('%Y-%m-%d %H:%M:%S')
        self.log(str_log)

    def on_after_trading(self, date_time):
        """收盘时触发一次回调, 港股是16:00:00"""
        str_log = "on_after_trading - %s" % date_time.strftime('%Y-%m-%d %H:%M:%S')
        self.log(str_log)

    def sma(self, np_array, n, array=False):
        """简单均线"""
        if n < 2:
            result = np_array
        else:
            result = talib.SMA(np_array, n)
        if array:
            return result
        return result[-1]

    def ema(self, np_array, n, array=False):
        """移动均线"""
        if n < 2:
            result = np_array
        else:
            result = talib.EMA(np_array, n)
        if array:
            return result
        return result[-1]

