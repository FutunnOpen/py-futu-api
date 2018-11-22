#-*-coding:utf-8-*-

import futu
from futu.quote.quote_response_handler import OrderBookHandlerBase
from futu.common.constant import *
from evatest.utils.logUtil import Logs

class GetOrderBook(object):
    #获取摆盘 get_order_book 和 OrderBookHandlerBase

    def test1(self):
        quote_ctx = futu.OpenQuoteContext(host='127.0.0.1',port=11111)
        quote_ctx.start()
        #设置监听
        handler = OrderBookTest()
        quote_ctx.set_handler(handler)

        #订阅股票
        code = 'HK.999010'
        quote_ctx.subscribe(code,SubType.ORDER_BOOK)
        #调用待测接口
        ret_code ,ret_data = quote_ctx.get_order_book(code)
        print(ret_code)
        print(ret_data)


class OrderBookTest(OrderBookHandlerBase):
    logger = Logs().getNewLogger(name='OrderBookTest')

    def on_recv_rsp(self, rsp_pb):
        ret_code ,ret_data = super(OrderBookTest, self).on_recv_rsp(rsp_pb)
        #打印
        OrderBookTest.logger.info('OrderBookTest')
        OrderBookTest.logger.info(ret_code)
        OrderBookTest.logger.info(ret_data)
        return RET_OK, ret_data

if __name__ == '__main__':
    gob = GetOrderBook()
    gob.test1()