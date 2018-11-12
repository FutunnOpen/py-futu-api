#-*-coding:utf-8-*-
from futuquant.trade.open_trade_context import *
import pandas

class DealListQuery(object):
    # 查询今日成交列表 deal_list_query

    def __init__(self):
        pandas.set_option('max_columns', 100)
        pandas.set_option('display.width', 1000)

    def test1(self):
        host = '127.0.0.1'
        port = 11112
        trade_ = OpenUSTradeContext(host, port)
        ret_code_unlock_trade, ret_data_unlock_trade = trade_.unlock_trade(password='123123')
        print('unlock_trade  ret_code= %d, ret_data= %s' % (ret_code_unlock_trade, ret_data_unlock_trade))

        ret_code,ret_data = trade_.deal_list_query(code="", trd_env=TrdEnv.REAL, acc_id=0,acc_index=1)
        #281756455982434220 现金0268
        #281756457982434020  现金0178
        #281756455982434020  融资0068

        print(ret_code)
        print(ret_data)

    def test_sh(self):
        trade_ctx_sh = OpenHKCCTradeContext('127.0.0.1',11112)
        ret_code, ret_data = trade_ctx_sh.deal_list_query()
        print(ret_code)
        print(ret_data)

    def test2(self):
        host = '127.0.0.1'
        port = 11111

        trade_hk = OpenHKTradeContext(host, port)
        trade_us = OpenUSTradeContext(host, port)
        trade_sh_m = OpenCNTradeContext(host, port)

        print(trade_hk.deal_list_query(code="", trd_env=TrdEnv.SIMULATE, acc_id=0))
        print(trade_us.deal_list_query(code="", trd_env=TrdEnv.SIMULATE, acc_id=0))
        print(trade_sh_m.deal_list_query(code="", trd_env=TrdEnv.SIMULATE, acc_id=0))

if __name__ == '__main__':
    dlq = DealListQuery()
    dlq.test1()