#-*-coding:utf-8-*-

from futuquant import *
from futuquant.testcase.person.eva.utils.logUtil import Logs
from futuquant.testcase.person.eva.datas.collect_stock import *

class GetCurKline(object):
    #获取实时K线 get_cur_kline 和 CurKlineHandlerBase

    def test1(self):
        quote_ctx = OpenQuoteContext(host='127.0.0.1',port=11111)
        quote_ctx.start()
        # 设置异步数据监听
        handler = CurKlineTest()
        quote_ctx.set_handler(handler)
        #待测数据
        codes = ['HK.00939', 'US.AAPL', 'SH.601318', 'SZ.000001']    #'HK.00700', 'US.AAPL', 'SH.601318', 'SZ.000001'
        kTypes = [SubType.K_1M,SubType.K_DAY,SubType.K_15M,SubType.K_60M,SubType.K_WEEK,SubType.K_MON]  #,SubType.K_15M,SubType.K_60M,SubType.K_WEEK,SubType.K_MON
        # 订阅股票
        # quote_ctx.subscribe(codes, kTypes)
        for code in codes:
            for kType in kTypes:
                # 订阅股票
                quote_ctx.subscribe(code, kType)
                #调用待测接口
                # ret_code,ret_data = quote_ctx.get_cur_kline(code,1000,kType,AuType.QFQ)
                # print(ret_code)
                # print(ret_data)

    def test2(self):
        quote_ctx = OpenQuoteContext(host='127.0.0.1',port=11111)
        quote_ctx.start()
        # 设置异步数据监听
        handler = CurKlineTest()
        quote_ctx.set_handler(handler)
        # codes = get_codes_cvs()[:2]
        print(quote_ctx.subscribe('HK.00857', SubType.K_1M))
        # print(quote_ctx.get_cur_kline('HK.00700', 0, SubType.K_1M, AuType.QFQ))
        # quote_ctx.close()

class CurKlineTest(CurKlineHandlerBase):
    '''获取实时K线 get_cur_kline 和 CurKlineHandlerBase'''
    logger = Logs().getNewLogger(name='CurKlineTest')
    def on_recv_rsp(self, rsp_pb):
        ret_code, ret_data = super(CurKlineTest, self).on_recv_rsp(rsp_pb)
        # 打印,记录日志
        CurKlineTest.logger.info('CurKlineTest')
        CurKlineTest.logger.info(ret_code)
        CurKlineTest.logger.info(ret_data)
        return RET_OK, ret_data

if __name__ == '__main__':
    gck = GetCurKline()
    gck.test1()