# -*- coding:utf-8 -*-
from futuquant import *
import logging
import random
import pandas


def test_stock_quote():
    pandas.set_option('max_columns', 100)
    pandas.set_option('display.width', 1000)
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    logger = logging.getLogger('mylogger')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('hangup.log')
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    logger.info('test')
    print(logger)
    print(quote_ctx.query_subscription())
    while True:
        ret_code, ret_data = quote_ctx.get_stock_basicinfo(Market.HK, SecurityType.STOCK)
        code_list = list(ret_data['code'])
        index = random.randint(0, len(code_list)-1)
        code = code_list[index]
        logger.info(code)
        logger.info('[stock_quote]')
        logger.info(quote_ctx.subscribe(code, SubType.QUOTE))
        logger.info(quote_ctx.get_stock_quote(code))
        logger.info('[cur_kline]')
        logger.info(quote_ctx.subscribe(code, SubType.K_1M))
        logger.info(quote_ctx.get_cur_kline(code, 1, SubType.K_1M))
        time.sleep(60)
        logger.info(quote_ctx.unsubscribe(code, [SubType.QUOTE, SubType.K_1M]))


class StockQuoteTest(StockQuoteHandlerBase):
    def on_recv_rsp(self, rsp_str):
        ret_code, data = super(StockQuoteTest,self).on_recv_rsp(rsp_str)
        if ret_code != RET_OK:
            print("StockQuoteTest: error, msg: %s" % data)
            return RET_ERROR, data

        print("StockQuoteTest ", data) # StockQuoteTest自己的处理逻辑

        return RET_OK, data



if __name__ == '__main__':
    # test_stock_quote()
    # SysConfig.set_all_thread_daemon(True)
    pandas.set_option('max_columns', 100)
    pandas.set_option('display.width', 1000)
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    # print(quote_ctx.get_plate_stock('SH.BK0287'))
    # print(quote_ctx.get_multi_points_history_kline(['sz'], ['2017-06-20', '2017-06-25'], KL_FIELD.ALL, KLType.K_1M,
    #                                                AuType.QFQ))
    # ret_code, ret_data = quote_ctx.get_market_snapshot('US.DIS181116C130000')
    # print(ret_data)
    # print(ret_data['option_valid'])
    # if list(ret_data['option_valid'])[0] is True:
    #     print(list(ret_data['option_valid']))
    #     print('111')
    # if ret_data['avg_price'][2] is None:
    #     print('111')

    # ret_code, ret_data = quote_ctx.get_stock_basicinfo(Market.HK, SecurityType.STOCK)
    # code_list = list(ret_data['code'])
    # code_list = code_list[10:291]
    # print(len(code_list))
    #
    # handler = StockQuoteTest()
    # quote_ctx.set_handler(handler)
    print(quote_ctx.subscribe('SZ.300751', SubType.K_DAY))
    print(quote_ctx.get_cur_kline('SZ.300751',10, SubType.K_DAY))
