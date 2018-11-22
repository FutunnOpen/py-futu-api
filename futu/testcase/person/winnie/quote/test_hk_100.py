from datetime import datetime
from futu import *
import collect_stock
import simple_logger
import sys
import signal
import pdb
import pandas

f = open('1012.txt','a')
log_tick = simple_logger.SimpleLogger('log/tick_{}.log'.format(datetime.now().date()))
log_price = simple_logger.SimpleLogger('log/price_{}.log'.format(datetime.now().date()))
log_obook = simple_logger.SimpleLogger('log/obook_{}.log'.format(datetime.now().date()))

quote_ctx = None
tick_count = 0

def on_signal(signum, tb):
    global quote_ctx
    # pdb.set_trace()
    logger.debug('signal: {}'.format(quote_ctx))
    if quote_ctx:
        logger.debug('close: {}'.format(quote_ctx))
        quote_ctx.close()
        quote_ctx = None
    log_tick.info('tick_count={}'.format(tick_count))
    log_tick.flush()

    log_price.flush()
    log_obook.flush()

    sys.exit(0)

signal.signal(signal.SIGINT, on_signal)
signal.signal(signal.SIGTERM, on_signal)


class TradeOrderTest(TradeOrderHandlerBase):
    """ order update push"""
    def on_recv_rsp(self, rsp_pb):
        ret, content = super(TradeOrderTest, self).on_recv_rsp(rsp_pb)
        print(ret, content)
        return ret, content


class TradeDealTest(TradeDealHandlerBase):
    """ order update push"""
    def on_recv_rsp(self, rsp_pb):
        ret, content = super(TradeDealTest, self).on_recv_rsp(rsp_pb)
        print(ret, content)
        return ret, content

class TickerTest(TickerHandlerBase):
    """ 获取逐笔推送数据 """
    def on_recv_rsp(self, rsp_pb):
        """数据响应回调函数"""
        ret_code, content = super(TickerTest, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            print("* TickerTest: error, msg: %s" % content)
            return RET_ERROR, content
        pandas.set_option('max_columns', 100)
        pandas.set_option('display.width', 1000)
        print("TICKER", content)# ,file=f,flush=True
        return RET_OK, content

class StockQuoteTest(StockQuoteHandlerBase):
    """
    获得报价推送数据
    """
    def on_recv_rsp(self, rsp_pb):
        """数据响应回调函数"""
        ret_code, content = super(StockQuoteTest, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            logger.debug("StockQuoteTest: error, msg: %s" % content)
            return RET_ERROR, content
        print("* StockQuoteTest : %s" % content)
        return RET_OK, content

class CurKlineTest(CurKlineHandlerBase):
    '''获取实时K线 get_cur_kline 和 CurKlineHandlerBase'''
    def on_recv_rsp(self, rsp_pb):
        ret_code, content = super(CurKlineTest, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            logger.debug("CurKlineTest: error, msg: %s" % content)
            return RET_ERROR, content
        print("* CurKlineTest : %s" % content)
        return RET_OK, content

class OrderBookTest(OrderBookHandlerBase):
    """
    获得报价推送数据
    """
    def on_recv_rsp(self, rsp_pb):
        """数据响应回调函数"""
        ret_code, content = super(OrderBookTest, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            logger.debug("OrderBookTest: error, msg: %s" % content)
            return RET_ERROR, content
        print("* OrderBookTest : %s" % content)
        return RET_OK, content

class SysNotifyTest(SysNotifyHandlerBase):

    def on_recv_rsp(self, rsp_pb):
        ret_code, content = super(SysNotifyTest, self).on_recv_rsp(rsp_pb)
        notify_type, sub_type, msg = content
        if ret_code != RET_OK:
            logger.debug("SysNotifyTest: error, msg: %s" % msg)
            return RET_ERROR, content
        print(msg)
        return ret_code, content

def test_tick():
    global quote_ctx
    codes = collect_stock.load_stock_code('stock-hk.csv')

    ip = '127.0.0.1'
    port = 11112
    quote_ctx = OpenQuoteContext(ip, port)

    quote_ctx.set_handler(StockQuoteTest())
    quote_ctx.set_handler(TickerTest())
    quote_ctx.set_handler(SysNotifyTest())
    quote_ctx.set_handler(CurKlineTest())
    quote_ctx.set_handler(OrderBookTest())

    ret, data = quote_ctx.get_global_state()
    if ret != RET_OK:
        return

    quote_ctx.start()

    code_sub = codes[:920]
    print(len(code_sub))
    #code_sub = ["HK.00700"]
    print("sub")
    print(quote_ctx.query_subscription())
    print(quote_ctx.subscribe(code_sub, [SubType.TICKER])) #


if __name__ == "__main__":

    test_tick()
    while True:
        time.sleep(0.2)

