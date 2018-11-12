#-*-coding:utf-8-*-

import futuquant
from futuquant.quote.quote_response_handler import *
from futuquant.common.constant import *
from futuquant.testcase.person.eva.utils.logUtil import Logs

class TestAll(object):
    dir = 'one_CentOs7'

    def __init__(self):
        # 加密通道
        # SysConfig.enable_proto_encrypt(True)
        # SysConfig.enable_proto_encrypt(True)


        # port=11111挂机CentOs7  1010503
        self.quote_ctx=futuquant.OpenQuoteContext(host='127.0.0.1',port=11111)
        self.quote_ctx.start()

    def test_GetBrokerQueue(self):
        #获取经纪队列 get_broker_queue 和 BrokerHandlerBase

        #设置监听
        handler = BrokerTest()
        self.quote_ctx.set_handler(handler)
        code = 'HK.00388'
        #订阅
        self.quote_ctx.subscribe(code,SubType.BROKER)
        #调用待测接口
        ret_code,bid_frame_table, ask_frame_table = self.quote_ctx.get_broker_queue(code)
        print(ret_code)
        print(bid_frame_table)
        print(ask_frame_table)

    def test_GetCurKline(self):
        #获取实时K线 get_cur_kline 和 CurKlineHandlerBase

        # 设置异步数据监听
        handler = CurKlineTest()
        self.quote_ctx.set_handler(handler)
        # 待测数据
        codes = ['HK.00700','US.JD', 'SH.601318', 'SZ.000001']  # 'HK.00700', 'US.AAPL', 'SH.601318', 'SZ.000001'
        kTypes = [SubType.K_1M, SubType.K_DAY]  # ,SubType.K_15M,SubType.K_60M,SubType.K_WEEK,SubType.K_MON
        # 订阅股票
        # quote_ctx.subscribe(codes, kTypes)
        for code in codes:
            for kType in kTypes:
                # 订阅股票
                self.quote_ctx.subscribe(code, kType)
                # 调用待测接口
                ret_code, ret_data = self.quote_ctx.get_cur_kline(code, 10, kType, AuType.QFQ)
                print(ret_code)
                print(ret_data)
                time.sleep(2)

    def test_GetOrderBook(self):
        #获取摆盘 get_order_book 和 OrderBookHandlerBase

        #设置监听
        handler = OrderBookTest()
        self.quote_ctx.set_handler(handler)

        #订阅股票
        code = 'HK.00772'
        self.quote_ctx.subscribe(code,SubType.ORDER_BOOK)
        #调用待测接口
        ret_code ,ret_data = self.quote_ctx.get_order_book(code)
        print(ret_code)
        print(ret_data)

    def test_GetRtData(self):
        #获取分时数据 get_rt_data 和 RTDataHandlerBase

        #设置监听
        handler= RTDataTest()
        self.quote_ctx.set_handler(handler)
        # code = 'HK.00772'
        codes = ['HK.01752','SZ.000858','SH.600109','US.GOOG']

        for code in codes:
            #订阅
            self.quote_ctx.subscribe(code,SubType.RT_DATA)
            #调用待测接口
            ret_code,ret_data = self.quote_ctx.get_rt_data(code)
            print(ret_code)
            print(ret_data)

    def test_GetRtTicker(self):
        #获取逐笔 get_rt_ticker 和 TickerHandlerBase

        # 设置异步数据监听
        handler = TickerTest()
        self.quote_ctx.set_handler(handler)
        codes = ['HK.01357','US.MSFT','SH.600519','SZ.000613']
        for code in codes:
            #订阅股票
            self.quote_ctx.subscribe(code,SubType.TICKER)
            # 调用待测接口
            ret_code,ret_data = self.quote_ctx.get_rt_ticker(code)
            print(ret_code)
            print(ret_data)

    def test_GetStockQuote(self):
        #获取报价 get_stock_quote 和 StockQuoteHandlerBase

        # 设置异步数据监听
        handler = StockQuoteTest()
        self.quote_ctx.set_handler(handler)
        codes = ['US.AAPL']  #'HK.02007','US.XNET','SH.603288','SZ.002396'

        #订阅股票
        for code in codes:
            self.quote_ctx.subscribe(code,SubType.QUOTE)
        #调用待测接口
        ret_code, ret_data = self.quote_ctx.get_stock_quote(codes)
        print(ret_code)
        print(ret_data)


class BrokerTest(BrokerHandlerBase):
    logger = Logs().getNewLogger('BrokerTest',TestAll.dir)
    def on_recv_rsp(self, rsp_pb):
        ret_code,stock_code,ret_data = super(BrokerTest, self).on_recv_rsp(rsp_pb)
        #打印日志
        BrokerTest.logger.info('BrokerTest')
        BrokerTest.logger.info(stock_code)
        BrokerTest.logger.info(ret_code)
        BrokerTest.logger.info(ret_data)
        return RET_OK,ret_data

class CurKlineTest(CurKlineHandlerBase):
    '''获取实时K线 get_cur_kline 和 CurKlineHandlerBase'''
    logger = Logs().getNewLogger('CurKlineTest',TestAll.dir)
    def on_recv_rsp(self, rsp_pb):
        ret_code, ret_data = super(CurKlineTest, self).on_recv_rsp(rsp_pb)
        # 打印,记录日志
        CurKlineTest.logger.info('CurKlineTest')
        CurKlineTest.logger.info(ret_code)
        CurKlineTest.logger.info(ret_data)
        return RET_OK, ret_data

class OrderBookTest(OrderBookHandlerBase):
    logger = Logs().getNewLogger('OrderBookTest',TestAll.dir)

    def on_recv_rsp(self, rsp_pb):
        ret_code ,ret_data = super(OrderBookTest, self).on_recv_rsp(rsp_pb)
        #打印
        OrderBookTest.logger.info('OrderBookTest')
        OrderBookTest.logger.info(ret_code)
        OrderBookTest.logger.info(ret_data)
        return RET_OK, ret_data

class RTDataTest(RTDataHandlerBase):
    logger = Logs().getNewLogger('RTDataTest',TestAll.dir)
    def on_recv_rsp(self, rsp_pb):
        ret_code,ret_data = super(RTDataTest, self).on_recv_rsp(rsp_pb)
        #打印信息
        RTDataTest.logger.info('RTDataTest')
        RTDataTest.logger.info(ret_code)
        RTDataTest.logger.info(ret_data)

        return RET_OK,ret_data

class TickerTest(TickerHandlerBase):
    '''获取逐笔 get_rt_ticker 和 TickerHandlerBase'''
    logger = Logs().getNewLogger('TickerTest',TestAll.dir)
    def on_recv_rsp(self, rsp_pb):
        ret_code, ret_data = super(TickerTest, self).on_recv_rsp(rsp_pb)
        # 打印,记录日志
        TickerTest.logger.info('TickerTest')
        TickerTest.logger.info(ret_code)
        TickerTest.logger.info(ret_data)
        return RET_OK, ret_data

class StockQuoteTest(StockQuoteHandlerBase):
    # 获取报价get_stock_quote和StockQuoteHandlerBase
    logger = Logs().getNewLogger('StockQuoteTest',TestAll.dir)
    def on_recv_rsp(self, rsp_str):
        ret_code, ret_data = super(StockQuoteTest,self).on_recv_rsp(rsp_str) # 基类的on_recv_rsp方法解包返回了报价信息，格式与get_stock_quote一样
        #打印,记录日志
        StockQuoteTest.logger.info('StockQuoteTest')
        StockQuoteTest.logger.info(ret_code)
        StockQuoteTest.logger.info(ret_data)
        return RET_OK, ret_data

if __name__ =='__main__':
    ta = TestAll()
    ta.test_GetBrokerQueue()
    ta.test_GetCurKline()
    ta.test_GetOrderBook()
    ta.test_GetRtData()
    ta.test_GetRtTicker()
    ta.test_GetStockQuote()