#-*-coding:utf-8-*-
from futuquant.trade.open_trade_context import *
import pandas

class OrderListQuery(object):
    # 查询今日订单列表 order_list_query

    def __init__(self):
        pandas.set_option('max_columns', 100)
        pandas.set_option('display.width', 1000)

    def test1(self):
        host = '127.0.0.1'
        port = 11111
        trade_ = OpenHKTradeContext(host, port)
        ret_code_unlock_trade, ret_data_unlock_trade = trade_.unlock_trade(password='321321')
        print('unlock_trade  ret_code= %d, ret_data= %s' % (ret_code_unlock_trade, ret_data_unlock_trade))
        # ret_code,ret_data = trade_.order_list_query(order_id="", status_filter_list=[], code='', start='2018-10-08 00:00:00', end='2018-10-08 23:59:59',trd_env=TrdEnv.REAL,acc_id=0,acc_index=0)
        ret_code, ret_data = trade_.order_list_query(order_id="", status_filter_list='全部成交', code='',start='', end='',trd_env=TrdEnv.REAL, acc_id=0, acc_index=0)

        print(ret_code)
        print(ret_data)

    def test_sh(self):
        host = '127.0.0.1'
        port = 11112
        trade_sh = OpenHKCCTradeContext(host, port)
        trade_sh_m = OpenCNTradeContext(host, port)

        trade_sh.unlock_trade('123123')

        print(trade_sh.order_list_query())
        print(trade_sh_m.order_list_query(trd_env=TrdEnv.SIMULATE))

    def test2(self):
        host = '127.0.0.1'
        port = 11111

        trade_hk = OpenHKTradeContext(host, port)
        trade_us = OpenUSTradeContext(host, port)
        trade_sh_m = OpenCNTradeContext(host, port)

        print(trade_hk.order_list_query(order_id="", status_filter_list=[], code='', start='', end='',
                         trd_env=TrdEnv.SIMULATE, acc_id=0))
        print(trade_us.order_list_query(order_id="", status_filter_list=[], code='', start='', end='',
                                          trd_env=TrdEnv.SIMULATE, acc_id=0))
        print(trade_sh_m.order_list_query(order_id="", status_filter_list=[], code='', start='', end='',
                                        trd_env=TrdEnv.SIMULATE, acc_id=0))

    def test3(self):
        host = '127.0.0.1'
        port = 11113

        trade_hk = OpenHKTradeContext(host, port)
        trade_us = OpenUSTradeContext(host, port)
        trade_cn = OpenHKCCTradeContext(host, port)
        trade_cn_s = OpenCNTradeContext(host,port)
        print('模拟交易 今日订单')
        print(trade_hk.order_list_query(order_id="", status_filter_list=[], code='', start='', end='',
                         trd_env=TrdEnv.SIMULATE, acc_id=0))
        print(trade_us.order_list_query(order_id="", status_filter_list=[], code='', start='', end='',
                                          trd_env=TrdEnv.SIMULATE, acc_id=0))
        print(trade_cn_s.order_list_query(order_id="", status_filter_list=[], code='', start='', end='',
                                        trd_env=TrdEnv.SIMULATE, acc_id=0))
        print('真实交易 今日订单')
        print(trade_hk.order_list_query(order_id="", status_filter_list=[], code='', start='', end='',
                                        trd_env=TrdEnv.REAL, acc_id=0))
        print(trade_us.order_list_query(order_id="", status_filter_list=[], code='', start='', end='',
                                        trd_env=TrdEnv.REAL, acc_id=0))
        print(trade_cn.order_list_query(order_id="", status_filter_list=[], code='', start='', end='',
                                          trd_env=TrdEnv.REAL, acc_id=0))



if __name__ == '__main__':
    olq = OrderListQuery()
    olq.test1()
