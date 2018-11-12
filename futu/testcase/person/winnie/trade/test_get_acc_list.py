# -*-coding:utf-8-*-
from futuquant.trade.open_trade_context import *
import pandas


class AccList(object):
    # 获取交易业务账户列表
    def __init__(self):
        pandas.set_option('max_columns', 100)
        pandas.set_option('display.width', 1000)

    def test_hk(self):
        trd_ctx = OpenHKTradeContext(host='127.0.0.1', port=11111)
        trd_ctx.unlock_trade('123123')
        print('hk:')
        ret_code, ret_data = trd_ctx.get_acc_list()
        print(ret_data)
        trd_ctx.close()

    def test_us(self):
        trd_ctx = OpenUSTradeContext(host='127.0.0.1', port=11111)
        trd_ctx.unlock_trade('123123')
        print('us:')
        ret_code, ret_data = trd_ctx.get_acc_list()
        print(ret_data)
        trd_ctx.close()

    def test_ch(self):
        trd_ctx = OpenCNTradeContext(host='127.0.0.1', port=11111)
        # trd_ctx = OpenHKCCTradeContext(host='127.0.0.1', port=11111)
        trd_ctx.unlock_trade('123123')
        print('A股：')
        ret_code, ret_data = trd_ctx.get_acc_list()
        print(ret_data)
        trd_ctx.close()


if __name__ == '__main__':
    al = AccList()
    # al.test_hk()
    al.test_us()
    # al.test_ch()
