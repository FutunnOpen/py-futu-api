#-*-coding:utf-8-*-

import futu
from futu.quote.quote_response_handler import StockQuoteHandlerBase
from futu.common.constant import *
# from futu import *
from evatest.utils.logUtil import Logs

class GetStockQuote(object):
    def test1(self):
        quote_ctx = futu.OpenQuoteContext(host='127.0.0.1',port=11116)
        quote_ctx.start()
        # 设置异步数据监听
        handler = StockQuoteTest()
        quote_ctx.set_handler(handler)
        #获取股票列表
        ret_code_stock_basicinfo,ret_data_stock_basicinfo = quote_ctx.get_stock_basicinfo(Market.HK,SecurityType.STOCK)
        # codes = ret_data_stock_basicinfo['code'].tolist()[:10]
        codes = ['HK.00700']
        #订阅股票
        for code in codes:
            quote_ctx.subscribe(code,SubType.QUOTE)
        #调用待测接口
        ret_code, ret_data = quote_ctx.get_stock_quote(codes)
        # print(ret_code)
        # print(ret_data)

class StockQuoteTest(StockQuoteHandlerBase):
    # 获取报价get_stock_quote和StockQuoteHandlerBase
    # logger = Logs().getNewLogger('StockQuoteTest')
    def on_recv_rsp(self, rsp_str):
        ret_code, ret_data = super(StockQuoteTest,self).on_recv_rsp(rsp_str) # 基类的on_recv_rsp方法解包返回了报价信息，格式与get_stock_quote一样
        #打印,记录日志
        # StockQuoteTest.logger.info('StockQuoteTest')
        # StockQuoteTest.logger.info(ret_code)
        # StockQuoteTest.logger.info(ret_data)
        print(ret_code)
        print(ret_data)

        return RET_OK, ret_data

if __name__ == '__main__':
    gsq = GetStockQuote()
    gsq.test1()