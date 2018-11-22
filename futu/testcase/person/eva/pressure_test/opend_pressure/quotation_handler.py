#-*-coding:utf-8-*-

from futu.quote.quote_response_handler import *
from evatest.utils.logUtil import Logs

class CurKlineTest(CurKlineHandlerBase):
    '''获取实时K线 get_cur_kline 和 CurKlineHandlerBase'''

    # logger = Logs().getNewLogger('CurKlineTest', None)

    def set_loggerDir(self,logger_dir=None):
        self.logger = Logs().getNewLogger('CurKlineTest', logger_dir)

    def on_recv_rsp(self, rsp_pb):
        ret_code, ret_data = super(CurKlineTest, self).on_recv_rsp(rsp_pb)
        # 打印,记录日志
        self.logger.info('CurKlineTest')
        self.logger.info(ret_code)
        self.logger.info(ret_data)
        return RET_OK, ret_data

class OrderBookTest(OrderBookHandlerBase):

    def set_loggerDir(self,logger_dir=None):
        self.logger = Logs().getNewLogger('OrderBookTest', logger_dir)

    def on_recv_rsp(self, rsp_pb):
        ret_code ,ret_data = super(OrderBookTest, self).on_recv_rsp(rsp_pb)
        #打印
        self.logger.info('OrderBookTest')
        self.logger.info(ret_code)
        self.logger.info(ret_data)
        return RET_OK, ret_data

class RTDataTest(RTDataHandlerBase):

    def set_loggerDir(self,logger_dir=None):
        self.logger = Logs().getNewLogger('RTDataTest', logger_dir)

    def on_recv_rsp(self, rsp_pb):
        ret_code,ret_data = super(RTDataTest, self).on_recv_rsp(rsp_pb)
        #打印信息
        self.logger.info('RTDataTest')
        self.logger.info(ret_code)
        self.logger.info(ret_data)

        return RET_OK,ret_data

class TickerTest(TickerHandlerBase):
    '''获取逐笔 get_rt_ticker 和 TickerHandlerBase'''

    def set_loggerDir(self,logger_dir=None):
        self.logger = Logs().getNewLogger('TickerTest', logger_dir)

    def on_recv_rsp(self, rsp_pb):
        ret_code, ret_data = super(TickerTest, self).on_recv_rsp(rsp_pb)
        # 打印,记录日志
        self.logger.info('TickerTest')
        self.logger.info(ret_code)
        self.logger.info(ret_data)
        return RET_OK, ret_data

class StockQuoteTest(StockQuoteHandlerBase):
    # 获取报价get_stock_quote和StockQuoteHandlerBase

    def set_loggerDir(self,logger_dir=None):
        self.logger = Logs().getNewLogger('StockQuoteTest', logger_dir)

    def on_recv_rsp(self, rsp_str):
        ret_code, ret_data = super(StockQuoteTest,self).on_recv_rsp(rsp_str) # 基类的on_recv_rsp方法解包返回了报价信息，格式与get_stock_quote一样
        #打印,记录日志
        self.logger.info('StockQuoteTest')
        self.logger.info(ret_code)
        self.logger.info(ret_data)
        return RET_OK, ret_data

class BrokerTest(BrokerHandlerBase):

    def set_loggerDir(self,logger_dir=None):
        self.logger = Logs().getNewLogger('BrokerTest', logger_dir)

    def on_recv_rsp(self, rsp_pb):
        ret_code,stock_code,ret_data = super(BrokerTest, self).on_recv_rsp(rsp_pb)
        #打印日志
        self.logger.info('BrokerTest')
        self.logger.info(stock_code)
        self.logger.info(ret_code)
        self.logger.info(ret_data)

        return RET_OK,ret_data
