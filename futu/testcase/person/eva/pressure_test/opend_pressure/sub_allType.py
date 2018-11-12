#-*-coding:utf-8-*-

import futuquant
from evatest.datas.collect_stock import *
from evatest.pressure_test.opend_pressure.quotation_handler import *

class SubAllType(object):
    '''
    OpenD压力测试_同时订阅50只股票的13类实时行情数据
    '''
    timestamp = (int)(time.time())
    dir = 'SubAllType_' + str(timestamp)

    def __init__(self):
        # 加密通道
        # SysConfig.enable_proto_encrypt(True)
        # SysConfig.enable_proto_encrypt(True)

        self.quote_ctx = futuquant.OpenQuoteContext(host='193.112.189.131',port=11125)
        self.quote_ctx.start()

    def close(self):
        self.quote_ctx.stop()
        self.quote_ctx.close()

    def subAll(self,codes):
        '''
        13类数据同时订阅
        :param codes: 股票列表
        :return:
        '''
        logger = Logs().getNewLogger('subALL', SubAllType.dir)
        subTypes = [SubType.QUOTE,SubType.ORDER_BOOK,SubType.TICKER,SubType.RT_DATA,SubType.K_1M,SubType.K_5M,SubType.K_15M,SubType.K_30M,SubType.K_60M,SubType.K_DAY,SubType.K_WEEK,SubType.K_MON,SubType.BROKER]
        # 触发订阅
        ret_code_sub, ret_data_sub = self.quote_ctx.subscribe(codes, subTypes)
        #设置监听
        handlers = [TickerTest(),BrokerTest(),CurKlineTest(),OrderBookTest(),RTDataTest(),StockQuoteTest()]
        for handler in handlers:
            # 设置监听
            handler.set_loggerDir(self.dir)
            self.quote_ctx.set_handler(handler)

        logger.info('len(codes) = '+str(len(codes))+' ret_code_sub = '+str(ret_code_sub) +' ret_data_sub = '+str(ret_data_sub))
        return ret_code_sub

if __name__ == '__main__':
    s = SubAllType()
    codes = get_codes_cvs()[:50]
    s.subAll(codes)

