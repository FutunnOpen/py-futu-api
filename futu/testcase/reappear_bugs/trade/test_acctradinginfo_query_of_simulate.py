# -*- coding:utf-8 -*-
from futuquant import *
import random
import pandas
import unittest


class AcctradinginfoQuery(unittest.TestCase):
    # bug单1：当入参order_id正确时，未按照该order_id的价格计算最大可买可卖
    # bug单2：港股下单后最大可买可卖的max_cash_buy字段有时显示为0--如果执行print(order_id)不会显示0，否则显示0.偶现。
    # bug单3：place_order指定价格和下单提交的价格不一致
    def test_acctradinginfo_query_hk_normal_order_id(self):
        # 测试点：港股普通订单
        order_type = OrderType.NORMAL
        code = 'HK.00700'
        price = 0.1
        order_id = None
        # 获取最新价格
        ret_code_ms, ret_data_ms = quote_ctx.get_market_snapshot(code)
        if ret_code_ms == RET_OK:
            price = ret_data_ms['last_price'][0]
        adjust_limit = random.random()
        # 下单
        ret_code_po,ret_data_po = trade_ctx_hk.place_order(100,100,'HK.00700',trd_side=TrdSide.BUY,
                                                           adjust_limit=adjust_limit,trd_env=TrdEnv.SIMULATE)
        print(ret_data_po)
        order_id = ret_data_po['order_id'][0]
        print(order_id)
        ret_code, ret_data = trade_ctx_hk.acctradinginfo_query(order_type, code, price, order_id,
                                                               adjust_limit=adjust_limit, trd_env=TrdEnv.SIMULATE,
                                                               acc_id=0, acc_index=0)
        # self.assertEqual(ret_code, RET_OK)
        # keys = ['max_cash_buy', 'max_cash_and_margin_buy', 'max_position_sell', 'max_sell_short', 'max_buy_back']
        # for k in keys:
        #     self.assertTrue(ret_data[k][0] != '')
        print(ret_data)


    # bug单：模拟交易查询美股普通订单的最大可买可卖返回失败
    def test_acctradinginfo_query_us_normal(self):
        # 测试点：美股普通订单
        order_type = OrderType.NORMAL
        code = 'US.VIPS'
        price = 5.7
        order_id = None
        adjust_limit = round(random.random(),3)
        ret_code, ret_data = trade_ctx_us.acctradinginfo_query(order_type, code, price, order_id,
                                                               adjust_limit=adjust_limit, trd_env=TrdEnv.SIMULATE,
                                                               acc_id=0, acc_index=0)
        # self.assertEqual(ret_code, RET_OK)
        print(adjust_limit)
        print(ret_code)
        print(ret_data)

    # bug单：美股下单后获取最大可买可卖时字段max_cash_buy为0
    def test_acctradinginfo_query_us_normal_order_id(self):
        # 测试点：美股普通订单
        order_type = OrderType.NORMAL
        code = 'US.AAPL'
        price = 0.1
        order_id = None
        # 获取最新价格
        ret_code_ms, ret_data_ms = quote_ctx.get_market_snapshot(code)
        if ret_code_ms == RET_OK:
            price = ret_data_ms['last_price'][0]
        adjust_limit = random.random()
        # 下单
        ret_code_po,ret_data_po = trade_ctx_us.place_order(price,1,code,trd_side=TrdSide.BUY,
                                                           adjust_limit=adjust_limit,trd_env=TrdEnv.SIMULATE)
        print(ret_data_po)
        order_id = ret_data_po['order_id'][0]
        ret_code, ret_data = trade_ctx_us.acctradinginfo_query(order_type, code, price, order_id,
                                                               adjust_limit=adjust_limit, trd_env=TrdEnv.SIMULATE,
                                                               acc_id=0, acc_index=0)
        print(ret_code)
        print(ret_data)




    # bug单：下A股普通订单之后查询最大可买可卖数据有误
    def test_acctradinginfo_query_cn_normal_order_id(self):
        # 测试点：A股普通订单
        order_type = OrderType.NORMAL
        code = 'SZ.002089'
        price = 0.1
        order_id = None
        # 获取最新价格
        ret_code_ms, ret_data_ms = quote_ctx.get_market_snapshot(code)
        if ret_code_ms == RET_OK:
            price = ret_data_ms['last_price'][0]
        adjust_limit = random.random()
        # 下单
        ret_code_po,ret_data_po = trade_ctx_cn.place_order(price,100,code,trd_side=TrdSide.BUY,
                                                           adjust_limit=adjust_limit,trd_env=TrdEnv.SIMULATE)
        print(ret_data_po,price)
        order_id = ret_data_po['order_id'][0]
        ret_code, ret_data = trade_ctx_cn.acctradinginfo_query(order_type, code, price, order_id,
                                                                    adjust_limit=adjust_limit, trd_env=TrdEnv.SIMULATE,
                                                                    acc_id=0, acc_index=0)
        self.assertEqual(ret_code, RET_OK)
        keys = ['max_cash_buy', 'max_cash_and_margin_buy', 'max_position_sell', 'max_sell_short', 'max_buy_back']
        for k in keys:
            self.assertTrue(ret_data[k][0] != '')
        print(ret_data)


    # bug单：入参price==-1时acctradinginfo_query返回提示信息不明确
    def test_acctradinginfo_query_err_price2(self):
        order_type = OrderType.NORMAL
        code = 'HK.00700'
        price = -1
        order_id = None
        adjust_limit = random.random()
        ret_code, ret_data = trade_ctx_hk.acctradinginfo_query(order_type, code, price, order_id,
                                                               adjust_limit=adjust_limit, trd_env=TrdEnv.SIMULATE,
                                                               acc_id=0, acc_index=0)
        print(ret_code)
        print(ret_data)

    # bug单：错误的order_id可以返回最大可买可卖
    def test_acctradinginfo_query_err_orderid(self):
        order_type = OrderType.NORMAL
        code = 'HK.00700'
        price = 100
        order_id = '12345'
        adjust_limit = random.random()
        ret_code, ret_data = trade_ctx_hk.acctradinginfo_query(order_type, code, price, order_id,
                                                                    adjust_limit=adjust_limit, trd_env=TrdEnv.SIMULATE,
                                                                    acc_id=0, acc_index=0)
        # self.assertEqual(ret_code, RET_ERROR)
        print(ret_code)
        print(ret_data)


if __name__ == '__main__':
    SysConfig.set_all_thread_daemon(True)
    quote_ctx = OpenQuoteContext('127.0.0.1', 11111)
    trade_ctx_hk = OpenHKTradeContext('127.0.0.1', 11111)
    trade_ctx_us = OpenUSTradeContext('127.0.0.1', 11111)
    trade_ctx_cn = OpenCNTradeContext('127.0.0.1', 11111)
    pandas.set_option('max_columns', 100)
    pandas.set_option('display.width', 1000)
    # unittest.main()
    aq = AcctradinginfoQuery()
    aq.test_acctradinginfo_query_us_normal()
