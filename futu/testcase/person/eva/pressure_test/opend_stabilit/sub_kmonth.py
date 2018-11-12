#-*-coding:utf-8-*-

import futuquant
from evatest.pressure_test.opend_pressure.quotation_handler import *
from evatest.utils.logUtil import Logs
from evatest.datas.collect_stock import *
from evatest.utils.test_setting import *
import time

class SubKMonth(object):
    '''
    订阅实时K线：月k，股票个数：用满500个订阅额度为止
    '''
    def sub(self):
        #日志
        logger_dir = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        self.logger = Logs().getNewLogger(name=self.__class__.__name__,dir=logger_dir)
        #行情上下文实例
        quote_ctx = futuquant.OpenQuoteContext(host= host, port= port_kmonth )
        quote_ctx.start()
        # 设置监听
        handler = CurKlineTest()  #月K
        handler.set_loggerDir(logger_dir)
        quote_ctx.set_handler(handler)
        #订阅
        sub_weight = 2  #订阅权重
        sub_limit = 500
        codes_len = sub_limit//sub_weight
        codes = get_codes_cvs()[0:codes_len]
        subtype = SubType.K_MON #订阅类型
        ret_code_sub, ret_data_sub = quote_ctx.subscribe(codes,subtype)
        # 记录订阅结果
        self.logger.info('subType = ' + subtype + ' ret_code_sub = ' + str(ret_code_sub) + ' ret_data_sub = ' + str(ret_data_sub))


if __name__ == '__main__':
    SubKMonth().sub()