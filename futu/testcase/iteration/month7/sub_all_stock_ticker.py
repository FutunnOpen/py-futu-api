#-*-coding:utf-8-*-

import futuquant
from futuquant.common.constant import *
from futuquant.quote.quote_response_handler import TickerHandlerBase
from futuquant.testcase.person.eva.utils.logUtil import Logs


class GetRtTicker(object):
    #获取逐笔 get_rt_ticker 和 TickerHandlerBase

    def test1(self):
        quote_ctx = futuquant.OpenQuoteContext(host='127.0.0.1',port=11111)
        quote_ctx.start()
        # 设置异步数据监听
        handler = TickerTest()
        quote_ctx.set_handler(handler)
        #所有正股
        codes_hk = quote_ctx.get_stock_basicinfo(market=Market.HK, stock_type=SecurityType.STOCK).tolist()[:100]
        codes_us = quote_ctx.get_stock_basicinfo(market=Market.US, stock_type=SecurityType.STOCK)[:100]
        #订阅股票
        codes = codes_hk + codes_us
        print('sub',quote_ctx.subscribe(codes,SubType.TICKER))


class TickerTest(TickerHandlerBase):
    '''获取逐笔 get_rt_ticker 和 TickerHandlerBase'''
    logger = Logs().getNewLogger(name='TickerTest')
    def on_recv_rsp(self, rsp_pb):
        ret_code, ret_data = super(TickerTest, self).on_recv_rsp(rsp_pb)
        # 打印,记录日志
        TickerTest.logger.info('TickerTest')
        TickerTest.logger.info(ret_code)
        TickerTest.logger.info(ret_data)
        return RET_OK, ret_data

if __name__ == '__main__':
    grt = GetRtTicker()
    grt.test1()