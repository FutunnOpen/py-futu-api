# -*- coding: utf-8 -*-
import time
from futuquant import *
from futuquant.testcase.person.winnie.trade.Handler import *


class SimulateTradeOptimization(object):
    def test_simulate_trade_hk_get_position_and_funds(self):
        SysConfig.set_all_thread_daemon(True)
        trade_ctx_hk = OpenHKTradeContext(host='127.0.0.1', port=11111)
        '''
        执行步骤：
        0、获取持仓和资金
        1、下单
        2、sleep 30秒
        3、获取持仓和资金
        '''
        print('资金：')
        print(trade_ctx_hk.accinfo_query(trd_env=TrdEnv.SIMULATE))
        print('持仓：')
        print(trade_ctx_hk.position_list_query(code='HK.00434', trd_env=TrdEnv.SIMULATE))

        pwd_unlock = '123123'
        trade_ctx_hk.unlock_trade(pwd_unlock)
        # print(trade_ctx_hk.place_order(price=2, qty=1000, code='HK.00434',
        #                                trd_side=TrdSide.BUY, trd_env=TrdEnv.SIMULATE))
        # time.sleep(150)
        print('订单列表：')
        print(trade_ctx_hk.order_list_query(trd_env=TrdEnv.SIMULATE))
        print(trade_ctx_hk.deal_list_query(trd_env=TrdEnv.SIMULATE))
        print('资金：')
        print(trade_ctx_hk.accinfo_query(trd_env=TrdEnv.SIMULATE))
        print('持仓：')
        print(trade_ctx_hk.position_list_query(code='HK.00434', trd_env=TrdEnv.SIMULATE))

    def test_push_order_state(self):
        # SysConfig.set_all_thread_daemon(True)
        trade_ctx_hk = OpenHKTradeContext(host='127.0.0.1', port=11111)
        print('资金：')
        print(trade_ctx_hk.accinfo_query(trd_env=TrdEnv.SIMULATE))
        print('持仓：')
        print(trade_ctx_hk.position_list_query(code='HK.00528', trd_env=TrdEnv.SIMULATE))

        handler_tradeOrder = TradeOrderTest()
        handler_tradeDealtrade = TradeDealTest()
        trade_ctx_hk.set_handler(handler_tradeOrder)
        trade_ctx_hk.set_handler(handler_tradeDealtrade)
        # 开启异步
        trade_ctx_hk.start()
        # print(trade_ctx_hk.history_order_list_query([OrderStatus.FILLED_ALL, OrderStatus.FILLED_PART], 'HK.01685'))
        # ret_code, ret_data = trade_ctx_hk.place_order(price=1.2, qty=2000, code='HK.00528',
        #                                               trd_side=TrdSide.BUY, trd_env=TrdEnv.SIMULATE)
        # print(ret_data)
        print(trade_ctx_hk.order_list_query(trd_env=TrdEnv.SIMULATE))


if __name__ == '__main__':
    sto = SimulateTradeOptimization()
    sto.test_push_order_state()
