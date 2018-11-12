#-*-coding:utf-8-*-
from futuquant.trade.open_trade_context import *
import pandas

class HistoryOrderListQuery(object):
    # 查询历史订单列表 history_order_list_query

    def __init__(self):
        pandas.set_option('max_columns', 100)
        pandas.set_option('display.width', 1000)

    def test_hk(self):
        host = '127.0.0.1'
        port = 11111
        self.tradehk_ctx = OpenHKTradeContext(host, port)
        ret_code_unlock_trade, ret_data_unlock_trade = self.tradehk_ctx.unlock_trade(password='123456')
        print('unlock_trade  ret_code= %d, ret_data= %s' % (ret_code_unlock_trade, ret_data_unlock_trade))

        ret_code,ret_data = self.tradehk_ctx.history_order_list_query(status_filter_list=[], code='', start='', end='',
                                 trd_env=TrdEnv.REAL, acc_id=0)
        pandas.set_option('display.width', 3000)
        print(ret_code)
        print(ret_data)
        #281756455982434220 现金0268
        #281756457982434020  现金0178
        #281756455982434020  融资0068
    def test_us(self):
        host = '127.0.0.1'
        port = 11112
        trade_us = OpenUSTradeContext(host, port)
        ret_code_unlock_trade, ret_data_unlock_trade = trade_us.unlock_trade(password='123123')
        print('unlock_trade  ret_code= %d, ret_data= %s' % (ret_code_unlock_trade, ret_data_unlock_trade))

        ret_code,ret_data = trade_us.history_order_list_query(status_filter_list=[], code='', start='', end='',
                                 trd_env=TrdEnv.REAL, acc_id=0,acc_index = 1)
        print(ret_code)
        print(ret_data)

    def test_sh(self):
        trade_ctx_sh = OpenHKCCTradeContext('127.0.0.1', 11113)

        ret_code, ret_data = trade_ctx_sh.history_order_list_query(status_filter_list=[], code='', start='2018-7-17',
                                                                       end='',
                                                                       trd_env=TrdEnv.REAL, acc_id=0)
        print(ret_code)
        print(ret_data)

    def test1(self):
        host = '127.0.0.1'
        port = 11111

        trade_hk = OpenHKTradeContext(host, port)
        trade_us = OpenUSTradeContext(host, port)
        trade_sh_m = OpenCNTradeContext(host, port)

        print(trade_hk.history_order_list_query(status_filter_list=[], code='', start='', end='',
                                 trd_env=TrdEnv.SIMULATE, acc_id=0))
        print(trade_us.history_order_list_query(status_filter_list=[OrderStatus.CANCELLED_ALL], code='', start='', end='',
                                                trd_env=TrdEnv.SIMULATE, acc_id=0))
        print(trade_sh_m.history_order_list_query(status_filter_list=[], code='', start='', end='',
                                                trd_env=TrdEnv.SIMULATE, acc_id=0))



if __name__ == '__main__':
    holq = HistoryOrderListQuery()
    holq.test1()