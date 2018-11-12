#-*-coding:utf-8-*-

from futuquant import *
import logging
import pandas

class TestShareOption(object):

    def __init__(self):
        pandas.set_option('max_columns', 100)
        pandas.set_option('display.width', 1000)

    def test_shareOption(self):
        host = '172.18.7.65' #mac 172.18.6.144
        port = 11111
        quote_cxt = OpenQuoteContext(host,port)
        quote_cxt.start()
        handlers = [CurKlineTest(),OrderBookTest(),RTDataTest(),TickerTest(),StockQuoteTest()]
        for h in handlers:
            #设置监听
            print('set_handler',quote_cxt.set_handler(handler=h))
        # 订阅
        print('subscribe',quote_cxt.subscribe(code_list=['US.AAPL180921C215000','HK.00700'],
                                subtype_list=[SubType.QUOTE, SubType.RT_DATA, SubType.ORDER_BOOK, SubType.TICKER,
                                              SubType.K_1M]))

class Tools(object):
    def getNewLogger(self, name, dir=None):
        '''
        :param name: 日志实例名
        :param dir: 日志所在文件夹名
        :return:
        '''
        logger = logging.getLogger(name)
        dir_path = os.getcwd() + os.path.sep + 'log'
        if dir is None:
            dir = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        dir_path = dir_path + os.path.sep + dir
        if os.path.exists(dir_path) is False:
            os.makedirs(dir_path)
        log_abs_name = dir_path + os.path.sep + name + '.txt'
        print(log_abs_name + '\n')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler = logging.FileHandler(log_abs_name)
        handler.setFormatter(formatter)
        console = logging.StreamHandler(stream=sys.stdout)

        logger.addHandler(handler)  # 设置日志输出到文件
        logger.addHandler(console)  # 设置日志输出到屏幕控制台
        logger.setLevel(logging.DEBUG)  # 设置打印的日志等级

        return logger

class CurKlineTest(CurKlineHandlerBase):
    '''获取实时K线 get_cur_kline 和 CurKlineHandlerBase'''
    logger = Tools().getNewLogger('CurKlineTest')
    def on_recv_rsp(self, rsp_pb):
        ret_code, ret_data = super(CurKlineTest, self).on_recv_rsp(rsp_pb)
        # 打印,记录日志
        CurKlineTest.logger.info('CurKlineTest')
        CurKlineTest.logger.info(ret_code)
        CurKlineTest.logger.info(ret_data)
        return RET_OK, ret_data

class OrderBookTest(OrderBookHandlerBase):
    #摆盘
    logger = Tools().getNewLogger('OrderBookTest')

    def on_recv_rsp(self, rsp_pb):
        ret_code ,ret_data = super(OrderBookTest, self).on_recv_rsp(rsp_pb)
        #打印
        OrderBookTest.logger.info('OrderBookTest')
        OrderBookTest.logger.info(ret_code)
        OrderBookTest.logger.info(ret_data)
        return RET_OK, ret_data

class RTDataTest(RTDataHandlerBase):
    #分时
    logger = Tools().getNewLogger('RTDataTest')
    def on_recv_rsp(self, rsp_pb):
        ret_code,ret_data = super(RTDataTest, self).on_recv_rsp(rsp_pb)
        #打印信息
        RTDataTest.logger.info('RTDataTest')
        RTDataTest.logger.info(ret_code)
        RTDataTest.logger.info(ret_data)

        return RET_OK,ret_data

class TickerTest(TickerHandlerBase):
    '''获取逐笔 get_rt_ticker 和 TickerHandlerBase'''
    logger = Tools().getNewLogger('TickerTest')
    def on_recv_rsp(self, rsp_pb):
        ret_code, ret_data = super(TickerTest, self).on_recv_rsp(rsp_pb)
        # 打印,记录日志
        TickerTest.logger.info('TickerTest')
        TickerTest.logger.info(ret_code)
        TickerTest.logger.info(ret_data)
        return RET_OK, ret_data

class StockQuoteTest(StockQuoteHandlerBase):
    # 获取报价get_stock_quote和StockQuoteHandlerBase
    logger = Tools().getNewLogger('StockQuoteTest')
    def on_recv_rsp(self, rsp_str):
        ret_code, ret_data = super(StockQuoteTest,self).on_recv_rsp(rsp_str) # 基类的on_recv_rsp方法解包返回了报价信息，格式与get_stock_quote一样
        #打印,记录日志
        StockQuoteTest.logger.info('StockQuoteTest')
        StockQuoteTest.logger.info(ret_code)
        StockQuoteTest.logger.info(ret_data)
        return RET_OK, ret_data


class BrokerTest(BrokerHandlerBase):
    #经济队列
    logger = Tools().getNewLogger('BrokerTest')
    def on_recv_rsp(self, rsp_pb):
        ret_code,stock_code,ret_data = super(BrokerTest, self).on_recv_rsp(rsp_pb)
        #打印日志
        BrokerTest.logger.info('BrokerTest')
        BrokerTest.logger.info(stock_code)
        BrokerTest.logger.info(ret_code)
        BrokerTest.logger.info(ret_data)
        return RET_OK,ret_data

def test1():
    pandas.set_option('max_columns', 100)
    pandas.set_option('display.width', 1000)

    host = '127.0.0.1' #mac 172.18.6.144
    port = 11111
    quote_cxt = OpenQuoteContext(host,port)
    quote_cxt.start()
    #设置监听
    print('set_handler',quote_cxt.set_handler(handler=CurKlineTest()))
    # 订阅
    print('subscribe',quote_cxt.subscribe(code_list=['US.AAPL180921C215000'],
                            subtype_list=[SubType.K_1M]))


if __name__ == '__main__':
    tso = TestShareOption()
    tso.test_shareOption()
    # test1()
