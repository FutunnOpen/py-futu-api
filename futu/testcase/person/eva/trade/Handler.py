#-*-coding:utf-8-*-

from futuquant.quote import *
from futuquant.trade.trade_response_handler import *
from futuquant.quote.quote_response_handler import *

class TradeOrderTest(TradeOrderHandlerBase):
    '''订单状态推送'''
    def on_recv_rsp(self, rsp_pb):
        ret_code,ret_data = super(TradeOrderTest, self).on_recv_rsp(rsp_pb)
        print('TradeOrderTest  ret_code = %d, ret_data = \n%s'%(ret_code,str(ret_data)))

        return RET_OK,ret_data

class TradeDealTest(TradeDealHandlerBase):
    '''订单成交推送 '''
    def on_recv_rsp(self, rsp_pb):
        ret_code,ret_data = super(TradeDealTest, self).on_recv_rsp(rsp_pb)
        print('TradeDealTest  ret_code = %d, ret_data = \n%s' % (ret_code,str(ret_data)))
        return RET_OK,ret_data

class SysNotifyTest(SysNotifyHandlerBase):
    """sys notify"""
    def on_recv_rsp(self, rsp_pb):
        """receive response callback function"""
        ret_code, content = super(SysNotifyTest, self).on_recv_rsp(rsp_pb)

        if ret_code == RET_OK:
            main_type, sub_type, msg = content
            print("* SysNotify main_type='{}' sub_type='{}' msg='{}'\n".format(main_type, sub_type, msg))
        else:
            print("* SysNotify error:{}\n".format(content))
        return ret_code, content