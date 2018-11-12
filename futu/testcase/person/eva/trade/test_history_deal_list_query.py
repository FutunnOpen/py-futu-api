#-*-coding:utf-8-*-
from futuquant.trade.open_trade_context import *
import pandas

class HistoryDealListQuery(object):
    # 查询历史成交列表 history_deal_list_query

    def __init__(self):
        pandas.set_option('max_columns', 100)
        pandas.set_option('display.width', 1000)

    def test1(self):
        host = '127.0.0.1'
        port = 11112

        trade_hk = OpenHKTradeContext(host, port)
        trade_us = OpenUSTradeContext(host, port)
        trade_sh_m = OpenCNTradeContext(host, port)

        print(trade_hk.unlock_trade(password='123123'))

        # print(trade_hk.history_deal_list_query(code = '', start = '', end = '', trd_env=TrdEnv.SIMULATE, acc_id=0))
        print(trade_us.history_deal_list_query(code='', start='', end='', trd_env=TrdEnv.REAL, acc_id=0, acc_index =1))
        # print(trade_sh_m.history_deal_list_query(code='', start='', end='', trd_env=TrdEnv.SIMULATE, acc_id=0))
        #281756455982434220 现金0268
        #281756457982434020  现金0178
        #281756455982434020  融资0068
        #牛号：5913971    281756455988247923

    def test_sh(self):
        trade_sh = OpenHKCCTradeContext('127.0.0.1',11112)
        ret_code, ret_data = trade_sh.history_deal_list_query( code='600007', start='', end='', trd_env=TrdEnv.REAL, acc_id=0)
        print(ret_code)
        print(ret_data)

if __name__ == '__main__':
    hdlq = HistoryDealListQuery()
    hdlq.test1()