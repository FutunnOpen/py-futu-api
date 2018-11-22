#-*-coding:utf-8-*-

from futu.testcase.eva.datas.collect_stock import *

import futu
from futu.testcase.person.eva.utils import Logs


class GetBrokerQueue(object):
    #获取经纪队列 get_broker_queue 和 BrokerHandlerBase

    def test1(self):
        quote_ctx = futu.OpenQuoteContext(host='127.0.0.1',port=11111)
        quote_ctx.start()
        #设置监听
        handler = BrokerTest()
        quote_ctx.set_handler(handler)
        codes = get_codes_cvs()[:50]
        #订阅
        for code in codes:
            quote_ctx.subscribe(code,SubType.BROKER)
        #调用待测接口
        # # ret_code,bid_frame_table, ask_frame_table = quote_ctx.get_broker_queue(code)
        # print(ret_code)
        # print(bid_frame_table)
        # print(ask_frame_table)

    def test2(self):
        # 经纪队列
        quote_ctx = futu.OpenQuoteContext(host='127.0.0.1', port=11111)
        code = 'HK.00700'
        quote_ctx.set_handler(BrokerTest())
        quote_ctx.subscribe(code, SubType.BROKER)
        print(quote_ctx.get_broker_queue(code))



class BrokerTest(BrokerHandlerBase):
    logger = Logs().getNewLogger(name='BrokerTest')
    def on_recv_rsp(self, rsp_pb):
        ret_code,stock_code, ret_data = super(BrokerTest, self).on_recv_rsp(rsp_pb)
        #打印日志
        BrokerTest.logger.info('BrokerTest')
        BrokerTest.logger.info(ret_code)
        BrokerTest.logger.info(ret_data)

        return RET_OK,stock_code, ret_data

if __name__ =='__main__':
    gbq = GetBrokerQueue()
    gbq.test2()