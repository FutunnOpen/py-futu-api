#-*-coding:utf-8-*-

from futuquant import *
from futuquant.trade.open_trade_context import *
from futuquant.testcase.person.eva.trade.Handler import *
import pandas

from futuquant.testcase.person.eva.trade.Handler import *
from futuquant.trade.open_trade_context import *


class PlaceOrder(object):
    # 下单接口 place_order

    def __init__(self):
        pandas.set_option('max_columns', 100)
        pandas.set_option('display.width', 1000)
    #     # 启动协议加密
    #     SysConfig.set_init_rsa_file('E:/test/testing/conn_key.txt')
    #     SysConfig.enable_proto_encrypt(True)

    def test_sh(self):
        host = '127.0.0.1'
        port = 11112
        trade_ctx_sh = OpenHKCCTradeContext(host, port)

        #解锁交易
        ret_code_unlock, ret_data_unlock = trade_ctx_sh.unlock_trade('123123')
        print('unlock ret_code = %d'%ret_code_unlock)
        print('unlock ret_data = %s' % ret_data_unlock)
        # 设置监听
        handler_tradeOrder = TradeOrderTest()
        handler_tradeDealtrade = TradeDealTest()
        trade_ctx_sh.set_handler(handler_tradeOrder)
        trade_ctx_sh.set_handler(handler_tradeDealtrade)
        # 开启异步
        trade_ctx_sh.start()

        #下单
        # price = 14.94, qty=700, code='SH.600007'
        # price = 28.8, qty=700, code='SZ.300003'
        #price = 3.512, qty=700, code='SZ.300005'
        ret_code_place_order, ret_data_place_order = trade_ctx_sh.place_order(price = 13.1, qty=500, code='SH.600007', trd_side=TrdSide.BUY, order_type=OrderType.NORMAL,adjust_limit=0, trd_env=TrdEnv.REAL, acc_id=0)
        print(ret_code_place_order)
        print(ret_data_place_order)

        # trade_ctx_sh.stop()
        # trade_ctx_sh.close()


    def test_hk(self):
        host =  '127.0.0.1'
        port = 11111
        trade = OpenHKTradeContext(host, port)

        ret_code_unlock_trade, ret_data_unlock_trade = trade.unlock_trade(password='321321')
        print('unlock_trade  ret_code= %d, ret_data= %s' % (ret_code_unlock_trade, ret_data_unlock_trade))
        # 设置监听
        handler_tradeOrder = TradeOrderTest()
        handler_tradeDealtrade = TradeDealTest()
        trade.set_handler(handler_tradeOrder)
        trade.set_handler(handler_tradeDealtrade)
        # 开启异步
        trade.start()
        #下单
        # ret_code, ret_data = trade_hk.place_order(price = 2.64, qty= 2000, code= 'HK.01758', trd_side= TrdSide.BUY, order_type= OrderType.ABSOLUTE_LIMIT, adjust_limit=0, trd_env= TrdEnv.REAL,acc_id=0)
        # print('真实环境',ret_code)
        # print('真实环境',ret_data)
        print(trade.place_order(price = 5.05, qty=500, code='HK.01357', trd_side=TrdSide.BUY, order_type=OrderType.NORMAL,
                    adjust_limit=0, trd_env=TrdEnv.REAL, acc_id=0))

    def test_us(self):
        host = '127.0.0.1'
        port = 21111
        tradeus_ctx = OpenUSTradeContext(host,port)
        ret_code_unlock_trade, ret_data_unlock_trade = tradeus_ctx.unlock_trade(password='321321')
        print('unlock_trade  ret_code= %d, ret_data= %s' % (ret_code_unlock_trade, ret_data_unlock_trade))
        # 设置监听
        handler_tradeOrder = TradeOrderTest()
        handler_tradeDealtrade = TradeDealTest()
        tradeus_ctx.set_handler(handler_tradeOrder)
        tradeus_ctx.set_handler(handler_tradeDealtrade)
        # 开启异步
        tradeus_ctx.start()
        code = 'US.AAPL'  # US.AAPL180914P205000
        price = 215
        qty = 1
        trd_side = TrdSide.BUY
        order_type = OrderType.NORMAL
        adjust_limit = 0
        trd_env = TrdEnv.REAL
        acc_id = 0
        acc_index = 0
        ret_code, ret_data = tradeus_ctx.place_order(price, qty, code, trd_side, order_type, adjust_limit, trd_env,acc_id, acc_index)
        print('place_order  ret_code= %d ,ret_data =\n%s' % (ret_code, str(ret_data)))

    def test1(self):
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
        #解锁
        print(trade_hk.unlock_trade('123123'))
        #下单
        print('港股下单place_order\n',trade_hk.place_order(price = 5.82, qty = 1000, code = 'HK.01357', trd_side=TrdSide.BUY,
                                  order_type=OrderType.NORMAL,adjust_limit=0, trd_env=TrdEnv.SIMULATE, acc_id=0))

        # price = 3.04, qty = 10, code = 'US.DDE'
        # price = 192, qty = 10, code = 'US.AAPL'
        print('美股下单place_order\n',trade_us.place_order(price = 36.34, qty = 2, code = 'US.JD', trd_side=TrdSide.BUY,
                                   order_type=OrderType.NORMAL,adjust_limit=0, trd_env=TrdEnv.SIMULATE, acc_id=0))

        # price = 9.62, qty = 200, code = 'SZ.002078'
        # price=10.2, qty=200, code='SH.601007'
        print('A股下单place_order\n',trade_sh_m.place_order(price=10.27, qty=100, code='SZ.000001', trd_side=TrdSide.BUY,
                                   order_type=OrderType.NORMAL,adjust_limit=0, trd_env=TrdEnv.SIMULATE, acc_id=0))

    def test2(self):
        host = '127.0.0.1'
        port = 11113
        trade_hk = OpenHKTradeContext(host, port)

        #解锁交易
        print(trade_hk.unlock_trade(password='321321'))

        # 设置监听
        trade_hk.set_handler(TradeOrderTest())
        trade_hk.set_handler(TradeDealTest())
        # 开启异步
        trade_hk.start()
        # 下单
        ret_code, ret_data = trade_hk.place_order(price=17.04, qty=200, code='HK.01810', trd_side=TrdSide.SELL,
                                                     order_type=OrderType.NORMAL, adjust_limit=0, trd_env=TrdEnv.REAL,
                                                     acc_id=0)
        print('真实环境', ret_code)
        print('真实环境', ret_data)
        #-------------------------------------------------------
        ret_code_s, ret_data_s = trade_hk.place_order(price=350, qty=100, code='HK.00700', trd_side=TrdSide.SELL,
                                                        order_type=OrderType.NORMAL,
                                                        adjust_limit=0, trd_env=TrdEnv.SIMULATE, acc_id=0)
        print('模拟交易', ret_code_s)
        print('模拟交易', ret_data_s)


if __name__ == '__main__':
    po = PlaceOrder()
    po.test_hk()
    # po.test1()