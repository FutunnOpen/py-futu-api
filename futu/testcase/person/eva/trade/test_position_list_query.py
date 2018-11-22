#-*-coding:utf-8-*-
from futu.trade.open_trade_context import *
import pandas

class PositionListQuery(object):
    # 查询持仓列表 position_list_query

    def __init__(self):
        pandas.set_option('max_columns', 100)
        pandas.set_option('display.width', 1000)

    def test_hk(self):
        host = '127.0.0.1'
        port = 11112
        trade_hk = OpenHKTradeContext(host, port)
        # self.trade_hk = OpenUSTradeContext(host, port)
        ret_code_unlock_trade, ret_data_unlock_trade = trade_hk.unlock_trade(password='123123')
        print('unlock_trade  ret_code= %d, ret_data= %s' % (ret_code_unlock_trade, ret_data_unlock_trade))

        ret_code,ret_data = trade_hk.position_list_query(code='', pl_ratio_min= None, pl_ratio_max= None, trd_env=TrdEnv.REAL, acc_id=0)
        #281756455982434220 现金0268
        #281756457982434020  现金0178
        #281756455982434020  融资0068
        print(ret_code)
        print(ret_data)

    def test_sh(self):
        host = '127.0.0.1'
        port = 11112
        tradehk_ctx_sh = OpenHKCCTradeContext(host, port)
        tradehk_ctx_sh.unlock_trade('123123')

        ret_code, ret_data = tradehk_ctx_sh.position_list_query(code='', pl_ratio_min=None, pl_ratio_max=0.5, trd_env=TrdEnv.REAL, acc_id=0)

        print(ret_code)
        print(ret_data)

    def test1(self):
        host =  '127.0.0.1'
        port = 11111

        # host = '172.18.6.144'#mac-patrick
        # port = 11111

        trade_hk = OpenHKTradeContext(host, port)
        trade_us = OpenUSTradeContext(host, port)
        trade_sh_m = OpenCNTradeContext(host, port)

        print(trade_us.unlock_trade('123123'))
        print(trade_hk.position_list_query(code='', pl_ratio_min=None, pl_ratio_max=None, trd_env=TrdEnv.SIMULATE, acc_id=0,acc_index=0))
        print(trade_us.position_list_query(code='', pl_ratio_min=None, pl_ratio_max=None, trd_env=TrdEnv.SIMULATE, acc_id=0))
        print(trade_sh_m.position_list_query(code='', pl_ratio_min=None, pl_ratio_max=None, trd_env=TrdEnv.SIMULATE, acc_id=0))


if __name__ == '__main__':
    plq = PositionListQuery()
    # plq.test_sh()
    plq.test1()