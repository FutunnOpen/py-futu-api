#-*-coding=utf-8-*-

import pandas
from futu import *

class TestAccId(object):
    #账户ID下标

    def __init__(self):
        pandas.set_option('display.width', 1000)
        pandas.set_option('max_columns', 1000)

    def test1(self):
        host = '127.0.0.1'
        port = 11114
        trade_ = OpenUSTradeContext(host, port)
        print(trade_.unlock_trade('123123'))
        print('accinfo_query',trade_.accinfo_query(acc_id=0, acc_index=1))    #281756457982434020
        print('position_list_query',trade_.position_list_query(acc_id=0, acc_index=1))
        print('place_order',trade_.place_order(price = 35.07, qty=2, code='US.JD', trd_side=TrdSide.BUY,acc_id=0, acc_index=1))
        print('order_list_query',trade_.order_list_query(acc_id=0, acc_index=1))
        print('deal_list_query',trade_.deal_list_query(acc_id=0, acc_index=1))
        print('history_order_list_query',trade_.history_order_list_query(acc_id=0, acc_index=1))
        print('history_deal_list_query',trade_.history_deal_list_query(code='',start='', end='',acc_id=0, acc_index=1))

if __name__ == '__main__':
    tai = TestAccId()
    tai.test1()
