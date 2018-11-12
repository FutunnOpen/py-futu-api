#-*-coding:utf-8-*-

import futuquant
from evatest.pressure_test.opend_pressure.quotation_handler import *
from evatest.utils.logUtil import Logs
from evatest.datas.collect_stock import *
import time

class SubAType(object):
    '''
    压测：同时订阅500只股票的一种实时数据
    '''
    subTypes = [SubType.QUOTE, SubType.ORDER_BOOK, SubType.TICKER, SubType.RT_DATA, SubType.BROKER, SubType.K_1M,SubType.K_5M,SubType.K_15M, SubType.K_30M, SubType.K_60M, SubType.K_DAY, SubType.K_WEEK, SubType.K_MON] #

    def __init__(self):
        timestamp = (int)(time.time())
        self.dir = 'SubAType_' + str(timestamp)
        self.logger = Logs().getNewLogger('sub', self.dir)

    def sub(self, codes,subType,port):

        #行情上下文实例
        quote_ctx = futuquant.OpenQuoteContext(host='127.0.0.1', port= port)
        quote_ctx.start()
        # 判断监听类型
        subType_index = SubAType.subTypes.index(subType)
        print('subType_index = %s'%subType_index)
        handler = None
        if subType_index is SubAType.subTypes.index(SubType.QUOTE):
            handler = StockQuoteTest()
        elif subType_index is SubAType.subTypes.index(SubType.ORDER_BOOK):
            handler = OrderBookTest()
        elif subType_index is SubAType.subTypes.index(SubType.TICKER):
            handler = TickerTest()
        elif subType_index is SubAType.subTypes.index(SubType.RT_DATA):
            handler = RTDataTest()
        elif subType_index is SubAType.subTypes.index(SubType.BROKER):
            handler = BrokerTest()
        else:
            handler = CurKlineTest()
        # 设置监听
        handler.set_loggerDir(self.dir)
        quote_ctx.set_handler(handler)
        # 触发订阅
        ret_code_sub, ret_data_sub = quote_ctx.subscribe(codes, subType)
        print(quote_ctx.query_subscription())
        #记录订阅结果
        self.logger.info('subType = '+subType+' ret_code_sub = ' + str(ret_code_sub) + ' ret_data_sub = ' + str(ret_data_sub))
        return ret_code_sub


if __name__ == '__main__':
    port = 11111
    codes = get_codes_cvs()[:250]
    # sat = SubAType()
    # sat.sub(codes, SubType.K_WEEK, port)
    for subType in SubAType.subTypes:
        port += 1
        sat.sub(codes, subType, port)
