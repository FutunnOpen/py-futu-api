#-*-coding:utf-8-*-

import futuquant
from futuquant.common.constant import *
from futuquant.quote.quote_response_handler import StockQuoteHandlerBase
from futuquant.testcase.person.eva.utils.logUtil import Logs
import pandas


class GetStockQuote(object):
    #获取报价 get_stock_quote 和 StockQuoteHandlerBase

    def __init__(self):
        pandas.set_option('max_columns', 100)
        pandas.set_option('display.width', 1000)


    def test1(self):
        quote_ctx = futuquant.OpenQuoteContext(host='172.18.7.65',port=11111) #mac-kathy:172.18.6.144
        quote_ctx.start()
        # 设置异步数据监听
        handler = StockQuoteTest()
        quote_ctx.set_handler(handler)
        #获取股票列表
        # print(quote_ctx.get_stock_basicinfo(Market.HK,SecurityType.STOCK))
        # codes = ret_data_stock_basicinfo['code'].tolist()[:10]
        codes = ['HK.00700']    #,'US.AAPL','HK.62423','US.MSFT','SH.601318','SZ.000001'
        #订阅股票
        for code in codes:
            quote_ctx.subscribe(code,SubType.QUOTE)
        #调用待测接口
        ret_code, ret_data = quote_ctx.get_stock_quote(codes)
        print('get_stock_quote ',ret_code)
        print(ret_data)

    def test2(self):
        quote_ctx = futuquant.OpenQuoteContext(host='127.0.0.1',port=11111)
        code = 'US.AAPL181026C240000'
        quote_ctx.subscribe(code, SubType.QUOTE)
        ret_code, ret_data = quote_ctx.get_stock_quote(code)
        print('get_stock_quote ', ret_code)
        print(ret_data)

class StockQuoteTest(StockQuoteHandlerBase):
    # 获取报价get_stock_quote和StockQuoteHandlerBase
    logger = Logs().getNewLogger(name='StockQuoteTest')
    def on_recv_rsp(self, rsp_str):
        ret_code, ret_data = super(StockQuoteTest,self).on_recv_rsp(rsp_str) # 基类的on_recv_rsp方法解包返回了报价信息，格式与get_stock_quote一样
        #打印,记录日志
        StockQuoteTest.logger.info('StockQuoteTest')
        StockQuoteTest.logger.info(ret_code)
        StockQuoteTest.logger.info(ret_data)
        return RET_OK, ret_data

if __name__ == '__main__':
    gsq = GetStockQuote()
    gsq.test2()