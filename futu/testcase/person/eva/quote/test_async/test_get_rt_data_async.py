#-*-coding:utf-8-*-

import futuquant
from futuquant.quote.quote_response_handler import RTDataHandlerBase
from futuquant.common.constant import *
from evatest.utils.logUtil import Logs

class GetRtData():
    #获取分时数据 get_rt_data 和 RTDataHandlerBase

    def test1(self):
        quote_ctx = futuquant.OpenQuoteContext(host='127.0.0.1',port=11111)
        quote_ctx.start()
        #设置监听
        handler= RTDataTest()
        quote_ctx.set_handler(handler)
        # code = 'HK.00772'
        codes = ['HK.00700','HK.01752','SZ.000858','SH.600109','US.GOOG']

        for code in codes:
            #订阅
            quote_ctx.subscribe(code,SubType.RT_DATA)
            #调用待测接口
            ret_code,ret_data = quote_ctx.get_rt_data(code)
            print(ret_code)
            print(ret_data)

    def test2(self):
        quote_ctx = futuquant.OpenQuoteContext(host='127.0.0.1',port=11111)
        code = 'HK.00772'
        #订阅
        quote_ctx.subscribe(code,SubType.RT_DATA)
        #调用待测接口
        ret_code,ret_data = quote_ctx.get_rt_data(code)
        print(ret_code)
        print(ret_data)

    def test3(self):
        quote_ctx = futuquant.OpenQuoteContext(host='127.0.0.1', port=11111)
        ret_code, ret_data = quote_ctx.get_stock_basicinfo(Market.HK, SecurityType.STOCK)
        codes = ['HK.00700','HK.01752','SZ.000858','SH.600109','US.GOOG']
        subTypes = SubType.RT_DATA
        print( quote_ctx.unsubscribe(codes,subTypes) )

class RTDataTest(RTDataHandlerBase):
    logger = Logs().getNewLogger(name='RTDataTest')
    def on_recv_rsp(self, rsp_pb):
        ret_code,ret_data = super(RTDataTest, self).on_recv_rsp(rsp_pb)
        #打印信息
        RTDataTest.logger.info('RTDataTest')
        RTDataTest.logger.info(ret_code)
        RTDataTest.logger.info(ret_data)

        return RET_OK,ret_data




if __name__ == '__main__':
   grd = GetRtData()
   grd.test3()