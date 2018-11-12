#-*-coding:utf-8-*-

import futuquant
from evatest.pressure_test.opend_pressure.quotation_handler import *
from evatest.utils.logUtil import Logs
from evatest.datas.collect_stock import *
from evatest.utils.test_setting import *
import time
import numpy

class SubQuoteTimeUse(object):
    '''
    订阅实时报价，股票个数：用满500个订阅额度为止
    '''
    def __init__(self):
        # 日志
        self.logger = Logs().getNewLogger(name=self.__class__.__name__)
        # 行情上下文实例
        self.quote_ctx = futuquant.OpenQuoteContext(host='127.0.0.1', port=11111)
        self.quote_ctx.start()

    def close(self):
        self.quote_ctx.stop()
        self.quote_ctx.close()

    def get_stock_warrant(self):
        '''
        获取港股所有正股和涡轮
        :return: code列表
        '''
        codes = []
        types = [SecurityType.STOCK, SecurityType.WARRANT]  # , SecurityType.ETF, SecurityType.IDX, SecurityType.BOND
        for type in types:
            ret_code, ret_data = self.quote_ctx.get_stock_basicinfo(Market.HK, type)
            if ret_code == RET_OK:
                codes += ret_data['code'].tolist()

        return codes

    def sub_rang(self):
        codes_len = 10000 # 500, 10000
        codes = self.get_stock_warrant()[0:codes_len]
        subTypes = [SubType.QUOTE]

        start_sub = time.time() * 1000
        i = 0
        for code in codes:
            ret_code_sub, ret_data_sub = self.quote_ctx.subscribe(code, subTypes)  # 订阅
            print(i, ' sub ', ret_code_sub, ret_data_sub)
            i += 1

        end_sub = time.time() * 1000
        self.logger.info('start_sub = %d' % start_sub)
        self.logger.info('end_sub = %d' % end_sub)
        self.logger.info('订阅，耗时(ms) = %d' % (end_sub - start_sub))

        # 反订阅
        time.sleep(60)
        start_unsub = time.time() * 1000
        i = 0
        for code in codes:
            ret_code_unsub, ret_data_unsub = self.quote_ctx.unsubscribe(code, subTypes)  # 订阅
            print(i, ' unsub ', ret_code_unsub, ret_data_unsub)
            i += 1

        end_unsub = time.time() * 1000

        self.logger.info('start_unsub = %d' % start_unsub)
        self.logger.info('end_unsub = %d' % end_unsub)
        self.logger.info('反订阅，耗时(ms) = %d' % (end_unsub - start_unsub))


    def sub(self):

        # 设置监听
        # handler = StockQuoteTest()  #报价
        # handler.set_loggerDir(logger_dir)
        # quote_ctx.set_handler(handler)
        #订阅
        # sub_weight = 1  #订阅权重
        # sub_limit = 500
        codes_len = 10000
        codes = self.get_stock_warrant()[0:codes_len]
        subtype = SubType.QUOTE #订阅类型

        start_sub = time.time()*1000
        self.logger.info('start_sub = %d'%start_sub)
        ret_code_sub, ret_data_sub = self.quote_ctx.subscribe(codes,subtype) #订阅
        end_sub = time.time()*1000
        self.logger.info('end_sub = %d'%end_sub)
        self.logger.info('订阅，耗时(ms) = %d' %(end_sub-start_sub))

        # 记录订阅结果
        self.logger.info('subType = ' + subtype + ' ret_code_sub = ' + str(ret_code_sub) + ' ret_data_sub = ' + str(ret_data_sub))

        time.sleep(61)
        start_unsub = time.time()*1000
        self.logger.info('start_unsub = %d' %start_unsub)
        ret_code_unsub, ret_data_unsub = self.quote_ctx.unsubscribe(codes, subtype)  # 反订阅
        end_unsub = time.time()*1000
        self.logger.info('end_unsub = %d' %end_unsub)
        self.logger.info('反订阅，耗时(ms) = %d'% (end_unsub - start_unsub))

        # 记录反订阅结果
        self.logger.info('unsubType = ' + subtype + ' ret_code_unsub = ' + str(ret_code_unsub) + ' ret_data_unsub = ' + str(ret_data_unsub))
        return  end_sub-start_sub, end_unsub - start_unsub

if __name__ == '__main__':

    tu = SubQuoteTimeUse()
    tu.sub_rang()
    tu.close()

    # tu = SubQuoteTimeUse()
    # sub_timeUse = []
    # unsub_timeUse = []
    # for i in range(10):
    #     sub_time , unsub_time = tu.sub()
    #     sub_timeUse.append(sub_time)
    #     unsub_timeUse.append(unsub_time)
    #
    # tu.logger.info('订阅，平均耗时(ms)：%d' % (numpy.mean(sub_timeUse)))
    # tu.logger.info('反订阅，平均耗时(ms)：%d' % (numpy.mean(unsub_timeUse)))
    #
    # tu.close()