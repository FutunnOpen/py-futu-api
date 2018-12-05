# encoding: UTF-8

'''
    实盘策略范例，接口用法见注释及范例代码
'''
import talib
from futu.examples.tiny_quant.tiny_quant_frame.TinyStrateBase import *
from futu.examples.tiny_quant.tiny_quant_frame.TinyQuantFrame import *


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
        """策略加载完配置后的回调
        1. 可修改symbol_pools 或策略内部其它变量的初始化
        2. 此时还不能调用futu api的接口
        """

    def on_start(self):
        """策略启动完成后的回调
        1. 框架已经完成初始化， 可调用任意的futu api接口
        2. 修改symbol_pools无效, 不会有动态的行情数据回调
        """
        self.log("on_start param1=%s param2=%s" %(self.param1, self.param2))


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
        """开盘时触发一次回调, 脚本挂机切换交易日时，港股会在09:30:00回调"""
        str_log = "on_before_trading - %s" % date_time.strftime('%Y-%m-%d %H:%M:%S')
        self.log(str_log)

    def on_after_trading(self, date_time):
        """收盘时触发一次回调, 脚本挂机时，港股会在16:00:00回调"""
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


if __name__ == '__main__':
    my_strate = TinyStrateSample()
    frame = TinyQuantFrame(my_strate)
    frame.run()

