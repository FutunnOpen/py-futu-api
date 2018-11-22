#-*-coding:utf-8-*-

from evatest.utils.logUtil import *
from futu import *
import numpy
from evatest.datas.collect_stock import *

class SubAllTimeUse(object):
    '''
    订阅实时报价，股票个数：用满500个订阅额度为止
    '''
    def __init__(self):
        # 日志
        self.logger = Logs().getNewLogger(name=self.__class__.__name__)
        # 行情上下文实例
        self.quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
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
        types = [SecurityType.STOCK, SecurityType.WARRANT]       #, SecurityType.ETF, SecurityType.IDX, SecurityType.BOND
        for type in types:
            ret_code , ret_data = self.quote_ctx.get_stock_basicinfo(Market.HK,type)
            if ret_code == RET_OK:
                codes += ret_data['code'].tolist()

        return codes

    def sub_rang(self):
        codes_len = 10000 # 31, 10000
        codes = self.get_stock_warrant()[0:codes_len]
        subTypes = [SubType.QUOTE, SubType.ORDER_BOOK, SubType.BROKER, SubType.TICKER]

        start_sub = time.time() * 1000
        i = 0
        for code in codes:
            ret_code_sub, ret_data_sub = self.quote_ctx.subscribe(code, subTypes)  # 订阅
            print(i,' sub ',ret_code_sub,ret_data_sub)
            i+=1

        end_sub = time.time() * 1000

        #反订阅
        time.sleep(60)
        start_unsub = time.time()*1000
        i = 0
        for code in codes:
            ret_code_unsub, ret_data_unsub = self.quote_ctx.unsubscribe(code, subTypes)  # 订阅
            print(i,' unsub ',ret_code_unsub,ret_data_unsub)
            i+=1

        end_unsub = time.time() * 1000

        self.logger.info('start_sub = %d' % start_sub)
        self.logger.info('end_sub = %d' % end_sub)
        self.logger.info('订阅，耗时(ms) = %d' % (end_sub - start_sub))
        self.logger.info('start_unsub = %d' % start_unsub)
        self.logger.info('end_unsub = %d' % end_unsub)
        self.logger.info('反订阅，耗时(ms) = %d' % (end_unsub - start_unsub))


    def sub(self):
        # sub_weight = [1,5,5,5]  #订阅权重
        # sub_limit = 500
        codes_len = 10000
        codes = self.get_stock_warrant()[0:codes_len]
        # codes_len = sub_limit//numpy.sum(sub_weight)
        # codes = get_codes_cvs()[0:codes_len]
        subTypes = [SubType.QUOTE, SubType.ORDER_BOOK, SubType.BROKER, SubType.TICKER]

        start_sub = time.time() * 1000
        self.logger.info('start_sub = %d' % start_sub)
        ret_code_sub, ret_data_sub = self.quote_ctx.subscribe(codes, subTypes)  # 订阅
        end_sub = time.time() * 1000
        self.logger.info('end_sub = %d' % end_sub)
        self.logger.info('订阅，耗时(ms) = %d' % (end_sub - start_sub))

        # 记录订阅结果
        self.logger.info('subType '+ ' ret_code_sub = ' + str(ret_code_sub) + ' ret_data_sub = ' + str(ret_data_sub))

        time.sleep(61)
        start_unsub = time.time() * 1000
        self.logger.info('start_unsub = %d' % start_unsub)
        ret_code_unsub, ret_data_unsub = self.quote_ctx.unsubscribe(codes, subTypes)  # 反订阅
        end_unsub = time.time() * 1000
        self.logger.info('end_unsub = %d' % end_unsub)
        self.logger.info('反订阅，耗时(ms) = %d' % (end_unsub - start_unsub))

        # 记录反订阅结果
        self.logger.info(
            'unsubType '+ ' ret_code_unsub = ' + str(ret_code_unsub) + ' ret_data_unsub = ' + str(ret_data_unsub))

        return end_sub - start_sub, end_unsub - start_unsub

if __name__ == '__main__':

    tu = SubAllTimeUse()
    tu.sub_rang()
    tu.close()



