#-*-coding:utf-8-*-

from futuquant import *

class GetAccList(object):
    '''获取交易业务账户列表'''

    def test_hk(self):
        host = '127.0.0.1'  # mac-kathy:172.18.6.144
        port = 11114
        trade_ctx_hk = OpenHKTradeContext(host, port)
        ret_code_acc_list, ret_data_acc_list = trade_ctx_hk.get_acc_list()
        print('hk-----------------')
        print(ret_code_acc_list)
        print(ret_data_acc_list)

    def test_us(self):
        host = '127.0.0.1'  # mac-kathy:172.18.6.144
        port = 11114
        trade_ctx_us = OpenUSTradeContext(host, port)
        ret_code_acc_list, ret_data_acc_list = trade_ctx_us.get_acc_list()
        print('us-----------------')
        print(ret_code_acc_list)
        print(ret_data_acc_list)

    def test_sh(self):
        host = '127.0.0.1'  # mac-kathy:172.18.6.144
        port = 11111
        trade_ctx_sh = OpenHKCCTradeContext(host, port)
        # 获取账户id 100068 281756468867335908
        ret_code_acc_list, ret_data_acc_list = trade_ctx_sh.get_acc_list()
        print('sh-----------------------真实')
        print(ret_code_acc_list)
        print(ret_data_acc_list)

        trade_ctx_sh_m = OpenCNTradeContext(host, port)
        ret_code_acc_list_m, ret_data_acc_list_m = trade_ctx_sh_m.get_acc_list()
        print('sh-----------------------模拟')
        print(ret_code_acc_list_m)
        print(ret_data_acc_list_m)


if __name__ == '__main__':
    gal = GetAccList()
    gal.test_hk()
    gal.test_us()
    # gal.test_sh()