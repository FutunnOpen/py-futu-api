#-*-coding:utf-8-*-

from evatest.datas.collect_stock import get_codes_cvs
import futuquant
from evatest.pressure_test.opend_pressure.quotation_handler import *

class SubLimit(object):

    def sub_allType_500(self):
        #挂机测稳定性：订阅额度范围内（500），订阅n只股票的13种数据类型

        subTypes = [SubType.QUOTE, SubType.ORDER_BOOK,SubType.BROKER, SubType.TICKER, SubType.RT_DATA]
        sub_limit = 500
        # sub_weight = [5,1,5,5,2,2]
        code_list = get_codes_cvs()

        #上下文实例
        quote_ctx = futuquant.OpenQuoteContext(host= '127.0.0.1' ,port= 11111)
        quote_ctx.start()

        #订阅n只股票的13种实时行情数据，订阅权重<=500
        for code in code_list:
            #订阅
            for subType in subTypes:
                quote_ctx.subscribe(code,subType)
            #设置监听
            logDir = 'sub_allType_500'
            handlers = [StockQuoteTest(), OrderBookTest(), BrokerTest(), TickerTest(),RTDataTest(),CurKlineTest() ]
            for handler in handlers:
                handler.set_loggerDir(logDir)
                quote_ctx.set_handler(handler)

            #获取已占用的订阅额度
            ret_code ,ret_data = quote_ctx.query_subscription()
            sub_weight_used = ret_data.get('total_used')
            print('sub_weight_used = %d'%sub_weight_used)
            if sub_weight_used ==sub_limit:
                break


    def sub_K_100(self):
        #挂机测稳定性：K线种类数（8）*股票个数<=100
        kTypes = [SubType.K_1M,SubType.K_5M,SubType.K_15M, SubType.K_30M, SubType.K_60M, SubType.K_DAY, SubType.K_WEEK, SubType.K_MON]
        limit = 100
        code_list = get_codes_cvs()

        # 上下文实例
        quote_ctx = futuquant.OpenQuoteContext(host='172.18.10.58', port=11111)
        quote_ctx.start()

        #设置监听
        handler = CurKlineTest()
        handler.set_loggerDir('sub_K_100')
        quote_ctx.set_handler(handler)
        #订阅
        sk = 0
        for code in code_list:
            for kType in kTypes:
                ret_code, ret_data = quote_ctx.subscribe(code,kType)
                if ret_code is RET_OK:
                    sk += 1
                    if sk == limit:
                        break
            if sk == limit:
                break



if __name__ =='__main__':
    SubLimit().sub_K_100()

