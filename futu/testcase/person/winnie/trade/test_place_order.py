# -*-coding:utf-8-*-
from futuquant.trade.open_trade_context import *
from futuquant.quote.open_quote_context import *
from futuquant.testcase.person.winnie.trade.Handler import *
import pandas


class PlaceOrder(object):
    # 下单
    def __init__(self):
        pandas.set_option('max_columns', 100)
        pandas.set_option('display.width', 1000)

    def test_hk_normal(self):
        # 港股下普通订单(00434)
        pwd_unlock = '123123'
        trd_ctx = OpenHKTradeContext(host='127.0.0.1', port=11111)
        trd_ctx.unlock_trade(pwd_unlock)
        # 设置监听
        # handler_tradeOrder = TradeOrderTest()
        # handler_tradeDealtrade = TradeDealTest()
        # trd_ctx.set_handler(handler_tradeOrder)
        # trd_ctx.set_handler(handler_tradeDealtrade)
        # 开启异步
        trd_ctx.start()
        # 港股买入
        ret_code, ret_data = trd_ctx.place_order(price=2.001,
                                                 qty=1000,
                                                 code='HK.00434',
                                                 trd_side=TrdSide.BUY,
                                                 order_type=OrderType.NORMAL,
                                                 adjust_limit=0,
                                                 trd_env=TrdEnv.REAL,
                                                 acc_id=0)
        print(ret_data)
        # 卖出
        # ret_code, ret_data = trd_ctx.place_order(price=2.2,
        #                                          qty=1000,
        #                                          code='HK.00434',
        #                                          trd_side=TrdSide.SELL,
        #                                          order_type=OrderType.NORMAL,
        #                                          adjust_limit=-0.001,
        #                                          trd_env=TrdEnv.SIMULATE,
        #                                          acc_id=0)
        # print(ret_data)
        print('获取今日订单列表:')
        ret_code, ret_data = trd_ctx.order_list_query(trd_env=TrdEnv.REAL, acc_id=0)
        print(ret_data)
        # trd_ctx.close()

    def test_hk_zheng(self):
        pwd_unlock = '123123'
        trd_ctx = OpenHKTradeContext(host='127.0.0.1', port=11111)
        trd_ctx.unlock_trade(pwd_unlock)
        # 港股正股买入
        # ret_code, ret_data = trd_ctx.place_order(price=0.37,
        #                                          qty=10000,
        #                                          code='HK.08140',
        #                                          trd_side=TrdSide.BUY,
        #                                          order_type=OrderType.NORMAL,
        #                                          adjust_limit=0,
        #                                          trd_env=TrdEnv.SIMULATE,
        #                                          acc_id=0)
        # print(ret_data)

        # ret_code, ret_data = trd_ctx.place_order(price=2.2,
        #                                          qty=1000,
        #                                          code='HK.00434',
        #                                          trd_side=TrdSide.SELL,
        #                                          order_type=OrderType.NORMAL,
        #                                          adjust_limit=-0.001,
        #                                          trd_env=TrdEnv.SIMULATE,
        #                                          acc_id=0)
        # print(ret_data)
        print('获取今日订单列表:')
        ret_code, ret_data = trd_ctx.order_list_query(trd_env=TrdEnv.SIMULATE,
                                                      acc_id=0)
        print(ret_data)
        trd_ctx.close()

    def test_us(self):
        # 美股下单
        trd_ctx = OpenUSTradeContext(host='127.0.0.1', port=11111)
        pwd_unlock = '123123'
        trd_ctx.unlock_trade(pwd_unlock)
        # ret_code, ret_data = trd_ctx.place_order(price=191.44,
        #                                          qty=1,
        #                                          code='US.AAPL',
        #                                          trd_side=TrdSide.SELL,
        #                                          order_type=OrderType.NORMAL,
        #                                          adjust_limit=0,
        #                                          trd_env=TrdEnv.SIMULATE,
        #                                          acc_id=0)
        # print(ret_data)
        ret_code, ret_data = trd_ctx.order_list_query(trd_env=TrdEnv.SIMULATE,
                                                      acc_id=0)
        print(ret_data)
        trd_ctx.close()

    def test_ch(self):
        trd_ctx = OpenCNTradeContext(host='127.0.0.1', port=11111)
        pwd_unlock = '123123'
        trd_ctx.unlock_trade(pwd_unlock)
        # ret_code, ret_data = trd_ctx.place_order(price=3.61,
        #                                          qty=100,
        #                                          code='SZ.000700',
        #                                          trd_side=TrdSide.BUY,
        #                                          order_type=OrderType.NORMAL,
        #                                          adjust_limit=0,
        #                                          trd_env=TrdEnv.SIMULATE,
        #                                          acc_id=0)
        # print(ret_data)
        ret_code, ret_data = trd_ctx.order_list_query(trd_env=TrdEnv.SIMULATE,
                                                      acc_id=0)
        print(ret_data)
        trd_ctx.close()

    def test_hk_wolun(self):
        pwd_unlock = '123123'
        trd_ctx = OpenHKTradeContext(host='127.0.0.1', port=11111)
        trd_ctx.unlock_trade(pwd_unlock)
        # 设置监听
        handler_tradeOrder = TradeOrderTest()
        handler_tradeDealtrade = TradeDealTest()
        trd_ctx.set_handler(handler_tradeOrder)
        trd_ctx.set_handler(handler_tradeDealtrade)
        # 开启异步
        trd_ctx.start()
        ret_code, ret_data = trd_ctx.place_order(price=0.093,
                                                 qty=10000,
                                                 code='HK.15375',
                                                 trd_side=TrdSide.BUY,
                                                 order_type=OrderType.NORMAL,
                                                 adjust_limit=0,
                                                 trd_env=TrdEnv.SIMULATE,
                                                 acc_id=0)
        print(ret_data)
        ret_code, ret_data = trd_ctx.order_list_query(trd_env=TrdEnv.SIMULATE,
                                                      acc_id=0)
        print(ret_data)

    def test_us_option(self):
        pwd_unlock = '123123'
        trd_ctx = OpenUSTradeContext(host='127.0.0.1', port=11112)
        trd_ctx.unlock_trade(pwd_unlock)
        # 设置监听
        handler_tradeOrder = TradeOrderTest()
        handler_tradeDealtrade = TradeDealTest()
        trd_ctx.set_handler(handler_tradeOrder)
        trd_ctx.set_handler(handler_tradeDealtrade)
        # 开启异步
        trd_ctx.start()

        ret_code, ret_data = trd_ctx.place_order(price=2,
                                                 qty=2,
                                                 code='US.AAPL',
                                                 trd_side=TrdSide.BUY,
                                                 order_type=OrderType.NORMAL,
                                                 adjust_limit=0,
                                                 trd_env=TrdEnv.SIMULATE,
                                                 acc_id=0)
        # print(ret_data)
        # ret_code, ret_data = trd_ctx.order_list_query(trd_env=TrdEnv.REAL,
        #                                               acc_id=0)
        # print(ret_data)


if __name__ == '__main__':
    po = PlaceOrder()
    # po.test_hk_normal()
    # po.test_hk_zheng()
    # po.test_us()
    # po.test_ch()
    # po.test_hk_wolun()
    po.test_us_option()
