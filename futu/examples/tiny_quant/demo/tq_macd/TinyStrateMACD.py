# encoding: UTF-8

'''
    实盘策略范例，接口用法见注释及范例代码
'''
import talib
from futu.examples.tiny_quant.tiny_quant_frame.TinyStrateBase import *
from futu.examples.tiny_quant.tiny_quant_frame.TinyQuantFrame import *
from futu import *
import datetime
import pandas as pd

class TinyStrateMACD(TinyStrateBase):
    """策略名称, setting.json中作为该策略配置的key"""
    name = 'tiny_strate_macd'

    """策略需要用到行情数据的股票池"""
    symbol_pools = ['HK.00700']
    pwd_unlock= '201791'

    def __init__(self):
       super(TinyStrateMACD, self).__init__()

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
        pass

    def on_quote_changed(self, tiny_quote):
        """报价、摆盘实时数据变化时，会触发该回调"""
        pass

    def on_bar_min1(self, tiny_bar):
        """每一分钟触发一次回调"""

        symbol = self.symbol_pools[0]
        now = datetime.datetime.now()
        work_time = now.replace(hour=15, minute=55, second=0)

        if now == work_time:
            quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
            data = tiny_bar
            price = data.open
            start_day = (now - datetime.timedelta(days=100)).strftime('%Y-%m-%d')
            end_day = now.strftime('%Y-%m-%d')
            history_result, history_kline_result, page_req_key = quote_ctx.request_history_kline(symbol, start=start_day, end=end_day)
            result, kline_result, page_req_key = quote_ctx.request_history_kline(symbol, start=start_day, end=end_day, ktype='K_5M')
            if history_result == 0 and result == 0 and history_kline_result.shape[0] >= 25 and kline_result.shape[0] > 0 :
                close_price = kline_result[-1:]
                close_price_array = history_kline_result['close']
                close_price_array.append(close_price)
                df = pd.DataFrame()
                df['EMA12'] = talib.EMA(np.array(close_price_array), timeperiod=6)
                df['EMA26'] = talib.EMA(np.array(close_price_array), timeperiod=12)
                df['MACD'], df['MACDsignal'], df['MACDhist'] = talib.MACD(np.array(close_price_array), fastperiod=6, slowperiod=12, signalperiod=9)
                signal = df['MACDsignal'][-1:].values[0]
                if signal > 0:
                    self.do_trade(symbol, price, "buy")
                elif signal <0:
                    self.do_trade(symbol, price, "sell")
            quote_ctx = OpenQuoteContext(host='172.24.31.139', port=11111)



    def on_bar_day(self, tiny_bar):
        """收盘时会触发一次日k回调"""
        pass

    def on_before_trading(self, date_time):
        """开盘时触发一次回调, 脚本挂机切换交易日时，港股会在09:30:00回调"""
        # 取前26个交易日的收盘价


        str_log = "on_before_trading - %s" % date_time.strftime('%Y-%m-%d %H:%M:%S')
        self.log(str_log)

    def on_after_trading(self, date_time):
        """收盘时触发一次回调, 脚本挂机时，港股会在16:00:00回调"""
        str_log = "on_after_trading - %s" % date_time.strftime('%Y-%m-%d %H:%M:%S')
        self.log(str_log)

    def ema(self, np_array, n, array=False):
        """移动均线"""
        if n < 2:
            result = np_array
        else:
            result = talib.EMA(np_array, n)
        if array:
            return result
        return result[-1]

    def do_trade(self, symbol, price, trd_side):
        # 获取账户信息
        trd_ctx = OpenHKTradeContext(host='127.0.0.1', port=11111)
        trd_ctx.unlock_trade(self.pwd_unlock)
        result, accinfo = trd_ctx.accinfo_query()
        if result != 0:
            return
        accinfo_cash = accinfo.cash.values[0]
        accinfo_market_val = accinfo.market_val.values[0]

        if trd_side == 'buy':
            qty = int(accinfo_cash / price)
            trd_ctx.place_order(price=price, qty=qty, code=symbol, trd_side=TrdSide.BUY)
        elif trd_side == 'sell':
            qty = int(accinfo_market_val / price)
            trd_ctx.place_order(price=price, qty=qty, code=symbol, trd_side=TrdSide.SELL)

        trd_ctx.close()



if __name__ == '__main__':
    my_strate = TinyStrateMACD()
    frame = TinyQuantFrame(my_strate)
    frame.run()