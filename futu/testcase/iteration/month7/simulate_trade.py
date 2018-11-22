#-*-coding:utf-8-*-
import pandas

from futu.testcase.person.eva.trade.Handler import *
from futu.trade.open_trade_context import *


class SimuluateTrade(object):
    # 模拟交易

    def __init__(self):
        pandas.set_option('max_columns', 100)
        pandas.set_option('display.width', 1000)

    def test_accinfo_query(self):
        #查询账户信息

        host = '127.0.0.1'
        port = 11111

        trade_hk = OpenHKTradeContext(host, port)
        trade_us = OpenUSTradeContext(host, port)
        trade_sh_m = OpenCNTradeContext(host, port)

        print(trade_hk.accinfo_query(trd_env=TrdEnv.SIMULATE, acc_id=0))
        print(trade_us.accinfo_query(trd_env=TrdEnv.SIMULATE, acc_id=0))
        print(trade_sh_m.accinfo_query(trd_env=TrdEnv.SIMULATE, acc_id=0))

    def test_place_order(self):
        host = '127.0.0.1'
        port = 11111

        trade_hk = OpenHKTradeContext(host, port)
        trade_us = OpenUSTradeContext(host, port)
        trade_sh_m = OpenCNTradeContext(host, port)

        # 设置监听
        handler_tradeOrder = TradeOrderTest()
        handler_tradeDealtrade = TradeDealTest()
        trade_hk.set_handler(handler_tradeOrder)
        trade_hk.set_handler(handler_tradeDealtrade)

        trade_us.set_handler(handler_tradeOrder)
        trade_sh_m.set_handler(handler_tradeOrder)
        # 开启异步
        trade_hk.start()
        trade_us.start()
        trade_sh_m.start()
        #下单
        print(trade_hk.place_order(price = 6.06, qty = 500, code = 'HK.01357', trd_side=TrdSide.BUY,
                                  order_type=OrderType.NORMAL,adjust_limit=0, trd_env=TrdEnv.SIMULATE, acc_id=0))

        # price = 3.04, qty = 10, code = 'US.DDE'
        # price = 192, qty = 10, code = 'US.AAPL'
        print(trade_us.place_order(price = 197, qty = 2, code = 'US.AAPL', trd_side=TrdSide.BUY,
                                   order_type=OrderType.NORMAL,adjust_limit=0, trd_env=TrdEnv.SIMULATE, acc_id=0))

        # price = 9.62, qty = 200, code = 'SZ.002078'
        # price=10.2, qty=200, code='SH.601007'
        print(trade_sh_m.place_order(price=9.16, qty=100, code='SZ.000001', trd_side=TrdSide.BUY,
                                   order_type=OrderType.NORMAL,adjust_limit=0, trd_env=TrdEnv.SIMULATE, acc_id=0))


if __name__ == '__main__':
    st = SimuluateTrade()
    st.test_accinfo_query()
    st.test_place_order()
