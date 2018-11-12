# -*-coding:utf-8-*-
from futuquant.trade.open_trade_context import *
from futuquant.testcase.person.winnie.trade.Handler import *
import pandas


class ModifyOrder(object):
    def __init__(self):
        pandas.set_option('max_columns', 100)
        pandas.set_option('display.width', 1000)

    def test_hk(self):
        trd_ctx = OpenHKTradeContext(host='127.0.0.1', port=11111)
        trd_ctx.unlock_trade('123123')
        ret_code, ret_data = trd_ctx.order_list_query(trd_env=TrdEnv.SIMULATE, acc_id=0)
        print(ret_data)
        # 1改单，修改数量
        ret_code, ret_data = trd_ctx.modify_order(modify_order_op=ModifyOrderOp.NORMAL,
                                                  order_id=3610190749957526613, qty=2000, price=2.2,
                                                  trd_env=TrdEnv.SIMULATE)
        print('改单：', ret_data)
        # 2改单，修改价格

        # 3改单，数量和价格同时修改

        # 4改单，订单ID不存在

        # 5模拟环境修改正式环境的ID

        # 6改单，已成交

        # 7改单，已撤单
        # ret_code, ret_data = trd_ctx.modify_order(modify_order_op=ModifyOrderOp.NORMAL,
        #                                           order_id=3610146760902480591, qty=2000, price=2)
        # print('改单：', ret_data)
        ret_code, ret_data = trd_ctx.order_list_query(trd_env=TrdEnv.SIMULATE, acc_id=0)
        print(ret_data)

    def test_us(self):
        trd_us = OpenUSTradeContext(host='127.0.0.1', port=11112)
        trd_us.unlock_trade('123123')
        ret_code, ret_data = trd_us.order_list_query(trd_env=TrdEnv.REAL, acc_id=0)
        print(ret_data)
        ret_code, ret_data = trd_us.modify_order(modify_order_op=ModifyOrderOp.CANCEL, order_id=1355707863574253342, qty=3,
                                                 price=10, trd_env=TrdEnv.REAL)
        print(ret_data)
        ret_code, ret_data = trd_us.order_list_query(trd_env=TrdEnv.REAL, acc_id=0)
        print(ret_data)


if __name__ == '__main__':
    mo = ModifyOrder()
    mo.test_us()
