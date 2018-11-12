# -*-coding:utf-8-*-
from futuquant.trade.open_trade_context import *
import pandas


class AccinfoQuery(object):
    def __init__(self):
        pandas.set_option('max_columns', 100)
        pandas.set_option('display.width', 1000)

    def test_hk(self):
        pwd = '123123'
        trd_ctx = OpenHKTradeContext(host='127.0.0.1', port=11111)
        ret_code, ret_data = trd_ctx.accinfo_query(trd_env=TrdEnv.SIMULATE, acc_id=6376)
        print(ret_data)
        trd_ctx.close()

    def test_us(self):
        pwd = '123123'
        trd_ctx = OpenUSTradeContext(host='127.0.0.1', port=11111)
        trd_ctx.unlock_trade(pwd)
        ret_code, ret_data = trd_ctx.accinfo_query(trd_env=TrdEnv.REAL, acc_id=0)
        print('us：')
        print(ret_data)
        trd_ctx.close()

    def test_ch(self):
        pwd = '123123'
        trd_ctx = OpenCNTradeContext(host='127.0.0.1', port=11111)
        ret_code, ret_data = trd_ctx.accinfo_query(trd_env=TrdEnv.SIMULATE, acc_id=6381)
        print('A股：')
        print(ret_data)
        trd_ctx.close()


if __name__ == '__main__':
    aq = AccinfoQuery()
    # aq.test_hk()
    aq.test_us()
    # aq.test_ch()
