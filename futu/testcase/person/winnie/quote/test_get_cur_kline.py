# -*-coding:utf-8-*-

from futu import *
from futu.common.constant import *
import pandas
import time
import random
import unittest
from futu.testcase.person.winnie.quote.compare_data import *

f1 = open('test_new_protocol.txt','a')
f2 = open('test_new_protoco2.txt','a')

# class GetCurKline(unittest.TestCase):
#     '''
#     测试类:获取实时K线
#     '''
#
#     # 各类型历史K线测试步骤和校验
#     def step_check_base1(self, casename, code, num, ktype, autype):
#         '''
#         测试点：各市场股票各种K线数据
#         :param casename:
#         :param code:
#         :param num:
#         :param ktype:
#         :param autype:
#         :return:
#         '''
#         print(casename)
#         print(casename, file=f1, flush=True)
#         print(casename, file=f2, flush=True)
#         quote_ctx1.subscribe(code, ktype)
#         ret_code, ret_data1 = quote_ctx1.get_cur_kline(code, num, ktype, autype)
#         print(ret_data1, file=f1, flush=True)
#         quote_ctx2.subscribe(code, ktype)
#         ret_code, ret_data2 = quote_ctx2.get_cur_kline(code, num, ktype, autype)
#         print(ret_data2, file=f2, flush=True)
#         print(CompareData().compare(ret_data1, ret_data2))
#
#         '''
#         校验点
#         1、请求成功，且数据不为空。即ret_code == RET_OK, len(ret_data)>0
#         1、请求成功，且数据不为空。即ret_code == RET_OK, len(ret_data)>0---应该和num相等
#         2、返回的股票与入参code一致
#         3、价格相关字段值一定大于0，即open、close、high、low、last_close。
#         4、volume成交量和turnover成交额要不同时为0，要不同时大于0。
#         5、日K、周K、月K的pe_ratio市盈率和turnover_rate换手率不为0。
#         '''
#         # 校验点1、请求成功，且数据不为空
#         # self.assertEqual(ret_code, RET_OK)
#         # self.assertTrue(len(ret_data) > 0)
#         # # 校验点2、返回的股票与入参code一致
#         # code_list = ret_data['code']
#         # for index in range(len(ret_data)):
#         #     self.assertTrue( code_list[index] == code, 'Error: index = %d' % index)
#         # 校验点3、价格相关字段值一定大于0
#         # price_key = ['open', 'close', 'high', 'low', 'last_close']
#         # for k in price_key:
#         #     price_list = ret_data[k]
#         #     for index in range(len(ret_data)):
#         #         self.assertTrue(abs( price_list[index] ) > 0, 'Error: index = %d' % index)
#
#     # 港股正股
#     def test_get_cur_kline_hk_1m(self):
#         '''
#         测试点：港股正股1分K
#         :return:
#         '''
#         casename = sys._getframe().f_code.co_name
#         code = 'HK.01810'
#         num = random.randint(1, 1000)
#         ktype = KLType.K_1M
#         autype = AuType.HFQ
#         self.step_check_base1(casename, code, num, ktype, autype)
#
#     def test_get_cur_kline_hk_idx_3m(self):
#         '''
#         测试点：港股指数3分K
#         :return:
#         '''
#         casename = sys._getframe().f_code.co_name
#         code = 'HK.800000'
#         num = random.randint(1, 1000)
#         ktype = KLType.K_3M
#         autype = AuType.QFQ
#         self.step_check_base1(casename, code, num, ktype, autype)
#
#     def test_get_cur_kline_hk_5m(self):
#         '''
#         测试点：港股正股5分K
#         :return:
#         '''
#         casename = sys._getframe().f_code.co_name
#         code = 'HK.00434'
#         num = random.randint(1,1000)
#         ktype = KLType.K_5M
#         autype = AuType.QFQ
#         self.step_check_base1(casename, code, num, ktype, autype)
#
#     def test_get_cur_kline_hk_15m(self):
#         '''
#         测试点：港股正股15分K
#         :return:
#         '''
#         casename = sys._getframe().f_code.co_name
#         code = 'HK.00700'
#         num = random.randint(1,1000)
#         ktype = KLType.K_15M
#         autype = AuType.NONE
#         self.step_check_base1( casename, code, num, ktype, autype)
#
#     def test_get_cur_kline_hk_30m(self):
#         '''
#         测试点：港股正股30分K
#         :return:
#         '''
#         casename = sys._getframe().f_code.co_name
#         code = 'HK.08299'
#         num = random.randint(1,1000)
#         ktype = KLType.K_30M
#         autype = AuType.QFQ
#         self.step_check_base1(casename, code, num, ktype, autype)
#
#     def test_get_cur_kline_hk_60m(self):
#         '''
#         测试点：港股正股60分K
#         :return:
#         '''
#         casename = sys._getframe().f_code.co_name
#         code = 'HK.01882'
#         num = random.randint(1,1000)
#         ktype = KLType.K_60M
#         autype = AuType.QFQ
#         self.step_check_base1( casename, code, num, ktype, autype)
#
#     def test_get_cur_kline_hk_day(self):
#         '''
#         测试点：港股正股日K
#         :return:
#         '''
#         casename = sys._getframe().f_code.co_name
#         code = 'HK.00260'
#         num = random.randint(1,1000)
#         ktype = KLType.K_DAY
#         autype = AuType.HFQ
#         self.step_check_base1(casename, code, num, ktype, autype)
#
#     def test_get_cur_kline_hk_week(self):
#         '''
#         测试点：港股正股周K
#         :return:
#         '''
#         casename = sys._getframe().f_code.co_name
#         code = 'HK.08507'
#         num = random.randint(1,1000)
#         ktype = KLType.K_WEEK
#         autype = AuType.NONE
#         self.step_check_base1(casename, code, num, ktype, autype)
#
#     def test_get_cur_kline_hk_mon(self):
#         '''
#         测试点：港股正股月K
#         :return:
#         '''
#         casename = sys._getframe().f_code.co_name
#         code = 'HK.08465'
#         num = random.randint(1,1000)
#         ktype = KLType.K_MON
#         autype = AuType.QFQ
#         self.step_check_base1(casename, code, num, ktype, autype)
#
#     # 港股涡轮
#     # @unittest.skip('港股涡轮有可能无数据故跳过')
#     def test_get_cur_kline_hk_wrt_1m(self):
#         '''
#         测试点：港股涡轮1分K
#         :return:
#         '''
#         casename = sys._getframe().f_code.co_name
#         code = 'HK.28579'
#         num = random.randint(1, 1000)
#         ktype = KLType.K_1M
#         autype = AuType.QFQ
#         self.step_check_base1(casename, code, num, ktype, autype)
#
#     # @unittest.skip('港股涡轮有可能无数据故跳过')
#     def test_get_cur_kline_hk_wrt_mon(self):
#         '''
#         测试点：港股涡轮月K
#         :return:
#         '''
#         casename = sys._getframe().f_code.co_name
#         code = 'HK.27141'
#         num = random.randint(1, 1000)
#         ktype = KLType.K_MON
#         autype = AuType.NONE
#         self.step_check_base1(casename, code, num, ktype, autype)
#
#     # 港股指数
#     def test_get_cur_kline_hk_idx_1m(self):
#         '''
#         测试点：港股涡轮1分K
#         :return:
#         '''
#         casename = sys._getframe().f_code.co_name
#         code = 'HK.800000'
#         num = random.randint(1, 1000)
#         ktype = KLType.K_1M
#         autype = AuType.QFQ
#         self.step_check_base1(casename, code, num, ktype, autype)
#
#     # 港股期货
#     def test_get_cur_kline_hk_futrue_1m(self):
#         '''
#         测试点：港股期货1分K
#         :return:
#         '''
#         casename = sys._getframe().f_code.co_name
#         code = 'HK_FUTURE.999010'
#         num = random.randint(1, 1000)
#         ktype = KLType.K_1M
#         autype = AuType.QFQ
#         self.step_check_base1(casename, code, num, ktype, autype)
#
#     # 美股
#     def test_get_cur_kline_us_1m(self):
#         '''
#         测试点：美股正股1分K
#         :return:
#         '''
#         casename = sys._getframe().f_code.co_name
#         code = 'US.AAPL'
#         num = random.randint(1, 1000)
#         ktype = KLType.K_1M
#         autype = AuType.NONE
#         self.step_check_base1(casename, code, num, ktype, autype)
#
#     @unittest.skip('test')
#     def test_get_cur_kline_us_season(self):
#         '''
#         测试点：美股正股季K
#         :return:
#         '''
#         casename = sys._getframe().f_code.co_name
#         code = 'US.JD'
#         num = random.randint(1, 1000)
#         ktype = KLType.K_SEASON
#         autype = AuType.QFQ
#         self.step_check_base1(casename, code, num, ktype, autype)
#
#     def test_get_cur_kline_us_mon(self):
#         '''
#         测试点：美股正股月K
#         :return:
#         '''
#         casename = sys._getframe().f_code.co_name
#         code = 'US.NOK'
#         num = random.randint(1, 1000)
#         ktype = KLType.K_MON
#         autype = AuType.QFQ
#         self.step_check_base1(casename, code, num, ktype, autype)
#
#     @unittest.skip('美股期权有可能无数据故跳过')
#     def test_get_cur_kline_us_drvt_5m(self):
#         '''
#         测试点：美股期权5分K
#         :return:
#         '''
#         casename = sys._getframe().f_code.co_name
#         code = 'US.DIS181123P110000'
#         num = random.randint(1, 1000)
#         ktype = KLType.K_5M
#         autype = AuType.NONE
#         self.step_check_base1(casename, code, num, ktype, autype)
#
#     def test_get_cur_kline_us_idx_30m(self):
#         '''
#         测试点：美股指数30分K
#         :return:
#         '''
#         casename = sys._getframe().f_code.co_name
#         code = 'US..DJI'
#         num = random.randint(1, 1000)
#         ktype = KLType.K_30M
#         autype = AuType.NONE
#         self.step_check_base1(casename, code, num, ktype, autype)
#
#     # A股
#     def test_get_cur_kline_sh_1m(self):
#         '''
#         测试点：A股（SH）正股1分K
#         :return:
#         '''
#         casename = sys._getframe().f_code.co_name
#         code = 'SH.603131'
#         num = random.randint(1, 1000)
#         ktype = KLType.K_1M
#         autype = AuType.NONE
#         self.step_check_base1(casename, code, num, ktype, autype)
#
#     def test_get_cur_kline_sz_1m(self):
#         '''
#         测试点：A股（SZ）正股1分K
#         :return:
#         '''
#         casename = sys._getframe().f_code.co_name
#         code = 'SZ.300710'
#         num = random.randint(1, 1000)
#         ktype = KLType.K_1M
#         autype = AuType.QFQ
#         self.step_check_base1(casename, code, num, ktype, autype)
#
#     @unittest.skip('test')
#     def test_get_cur_kline_sz_season(self):
#         '''
#         测试点：A股（SZ）正股季K
#         :return:
#         '''
#         casename = sys._getframe().f_code.co_name
#         code = 'SZ.300751'
#         num = random.randint(1, 1000)
#         ktype = KLType.K_SEASON
#         autype = AuType.QFQ
#         self.step_check_base1(casename, code, num, ktype, autype)
#
#     def test_get_cur_kline_cn_idx_1m(self):
#         '''
#         测试点：A股指数周K
#         :return:
#         '''
#         casename = sys._getframe().f_code.co_name
#         code = 'SH.000001'
#         num = random.randint(1, 1000)
#         ktype = KLType.K_1M
#         autype = AuType.QFQ
#         # quote_ctx.subscribe(code, ktype)
#         # ret_code, ret_data = quote_ctx.get_cur_kline(code, num, ktype, autype)
#         # print(casename)
#         # print(ret_data)
#         # self.assertEqual(ret_code,RET_OK)
#         self.step_check_base1(casename, code, num, ktype, autype)
#
#     # code, num, ktype, autype入参错误
#     def step_check_base2(self, casename, code, num, ktype, autype):
#         '''
#         测试点：各市场股票各种K线数据
#         :param casename:
#         :param code:
#         :param num:
#         :param ktype:
#         :param autype:
#         :return:
#         '''
#         print(casename)
#         print(casename, file=f1, flush=True)
#         print(casename, file=f2, flush=True)
#         ret_code_sub, ret_data_sub = quote_ctx1.subscribe(code, ktype)
#         ret_code, ret_data1 = quote_ctx1.get_cur_kline(code, num, ktype, autype)
#         print(ret_data1, file=f1, flush=True)
#         ret_code_sub, ret_data_sub = quote_ctx2.subscribe(code, ktype)
#         ret_code, ret_data2 = quote_ctx2.get_cur_kline(code, num, ktype, autype)
#         print(ret_data2, file=f2, flush=True)
#         print(CompareData().compare(ret_data1, ret_data2))
#
#
#     def test_get_cur_kline_err_code(self):
#         '''
#         测试点：股票代码格式错误
#         :return:
#         '''
#         casename = sys._getframe().f_code.co_name
#         code = '000001'     # code格式错误
#         num = random.randint(1, 1000)
#         ktype = KLType.K_1M
#         autype = AuType.QFQ
#         self.step_check_base2(casename, code, num, ktype, autype)
#
#     def test_get_cur_kline_err_num(self):
#         '''
#         测试点：num输入负数
#         :return:
#         '''
#         casename = sys._getframe().f_code.co_name
#         code = 'HK.00700'
#         num = -1  # num输入负数
#         ktype = KLType.K_1M
#         autype = AuType.QFQ
#         self.step_check_base2( casename, code, num, ktype, autype)
#
#     def test_get_cur_kline_err_ktype(self):
#         '''
#         测试点：K线类型错误
#         :return:
#         '''
#         casename = sys._getframe().f_code.co_name
#         code = 'HK.01810'
#         num = random.randint(1, 1000)
#         ktype = '1分K'  # K线类型错误
#         autype = AuType.QFQ
#         self.step_check_base2(casename, code, num, ktype, autype)
#
#     def test_get_cur_kline_err_autype(self):
#         '''
#         测试点：复权值错误
#         :return:
#         '''
#         casename = sys._getframe().f_code.co_name
#         code = 'US.PDD'
#         num = random.randint(1, 1000)
#         ktype = KLType.K_1M
#         autype = '不复权'  # 复权值错误
#         self.step_check_base2(casename, code, num, ktype, autype)
#
#     # 未订阅
#     def test_get_cur_kline_no_sub(self):
#         '''
#         测试点：未订阅，报错
#         :return:
#         '''
#         casename = sys._getframe().f_code.co_name
#         print(casename)
#         print(casename, file=f1, flush=True)
#         print(casename, file=f2, flush=True)
#         code = 'US.VIPS'
#         num = random.randint(1, 1000)
#         ktype = KLType.K_1M
#         autype = AuType.QFQ
#         ret_code, ret_data1 = quote_ctx1.get_cur_kline(code, num, ktype, autype)
#         ret_code, ret_data2 = quote_ctx2.get_cur_kline(code, num, ktype, autype)
#         print(ret_data1, file=f1, flush=True)
#         print(ret_data2, file=f2, flush=True)
#         print(CompareData().compare(ret_data1, ret_data2))
#
#     # 订阅板块和正股，反订阅板块正股是否正常
#     def test_get_cur_kline_bk_stock_unsubscribe_bk(self):
#         casename = sys._getframe().f_code.co_name
#         print(casename)
#         print(casename, file=f1, flush=True)
#         print(casename, file=f2, flush=True)
#         code_list = ['HK.00700','SH.BK0001']
#         quote_ctx1.subscribe(code_list,SubType.K_1M)
#         ret_code, ret_data1 = quote_ctx1.get_cur_kline(code_list[0],10,SubType.K_1M)
#         print(ret_data1, file=f1, flush=True)
#         ret_code, ret_data1 = quote_ctx1.get_cur_kline(code_list[1],10,SubType.K_1M)
#         print(ret_data1, file=f1, flush=True)
#         quote_ctx2.subscribe(code_list, SubType.K_1M)
#         ret_code, ret_data2 = quote_ctx2.get_cur_kline(code_list[0], 10, SubType.K_1M)
#         print(ret_data2, file=f2, flush=True)
#         ret_code, ret_data2 = quote_ctx2.get_cur_kline(code_list[1], 10, SubType.K_1M)
#         print(ret_data2, file=f2, flush=True)
#         print(CompareData().compare(ret_data1, ret_data2))
#         time.sleep(60)
#         quote_ctx1.unsubscribe('SH.BK0001',SubType.K_1M)
#         ret_code, ret_data1 = quote_ctx1.get_cur_kline(code_list[0],10,SubType.K_1M)
#         print(ret_data1, file=f1, flush=True)
#         quote_ctx2.unsubscribe('SH.BK0001', SubType.K_1M)
#         ret_code, ret_data2 = quote_ctx2.get_cur_kline(code_list[0], 10, SubType.K_1M)
#         print(ret_data2, file=f2, flush=True)
#         print(CompareData().compare(ret_data1, ret_data2))
#
#     # 订阅板块和正股，反订阅板块正股是否正常
#     def test_get_cur_kline_bk_stock_unsubscribe_stock(self):
#         casename = sys._getframe().f_code.co_name
#         print(casename)
#         print(casename, file=f1, flush=True)
#         print(casename, file=f2, flush=True)
#         code_list = ['HK.00700','SH.BK0001']
#         quote_ctx1.subscribe(code_list,SubType.K_5M)
#         ret_code, ret_data1 = quote_ctx1.get_cur_kline(code_list[0],10,SubType.K_5M)
#         print(ret_data1, file=f1, flush=True)
#         ret_code, ret_data1 = quote_ctx1.get_cur_kline(code_list[1],10,SubType.K_5M)
#         print(ret_data1, file=f1, flush=True)
#         quote_ctx2.subscribe(code_list, SubType.K_5M)
#         ret_code, ret_data2 = quote_ctx2.get_cur_kline(code_list[0], 10, SubType.K_5M)
#         print(ret_data2, file=f2, flush=True)
#         ret_code, ret_data2 = quote_ctx2.get_cur_kline(code_list[1], 10, SubType.K_5M)
#         print(ret_data2, file=f2, flush=True)
#         print(CompareData().compare(ret_data1, ret_data2))
#         time.sleep(60)
#         quote_ctx1.unsubscribe('HK.00700',SubType.K_5M)
#         ret_code, ret_data1 = quote_ctx1.get_cur_kline(code_list[1],10,SubType.K_5M)
#         print(ret_data1, file=f1, flush=True)
#         quote_ctx2.unsubscribe('HK.00700', SubType.K_5M)
#         ret_code, ret_data2 = quote_ctx2.get_cur_kline(code_list[1], 10, SubType.K_5M)
#         print(ret_data2, file=f2, flush=True)
#         print(CompareData().compare(ret_data1, ret_data2))


class AsyncCurKline(unittest.TestCase):
    '''
    实时报价推送测试类
    '''

    def step_base(self, code_list, casename=sys._getframe().f_code.co_name ):
        '''
        基本测试步骤
        :param code_list:待订阅的股票代码列表
        :return:
        '''
        #打印日志：测试用例名
        # print(casename, file=f1, flush=True)
        #设置监听
        handler1 = CureKlineTest1()
        handler2 = CureKlineTest2()
        quote_ctx1.set_handler(handler1)
        quote_ctx2.set_handler(handler2)
        #订阅所有类型的K线
        subtypes = [SubType.K_1M, SubType.K_5M, SubType.K_15M, SubType.K_60M, SubType.K_DAY, SubType.K_WEEK, SubType.K_MON]
        quote_ctx1.subscribe(code_list, subtypes)
        quote_ctx2.subscribe(code_list, subtypes)

    def test_asyncCurKline_hk_stock(self):
        #1、测试点：订阅港股正股实时报价
        self.step_base(code_list= ['HK.00700'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncCurKline_hk_wrrant(self):
        # 1、测试点：订阅港股涡轮实时K线

        #获取某一涡轮代码
        codes_warrant = 'HK.27141'
        #执行测试步骤
        self.step_base(code_list=codes_warrant, casename=sys._getframe().f_code.co_name )

        # 2、校验
        # 不合适在此处校验，需跑完一整天数据后校验

    def test_asyncCurKline_hk_future_stock(self):
        #1、测试点：订阅港股期货实时K线
        self.step_base(code_list= ['HK_FUTURE.999010'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncCurKline_hk_idx(self):
        #1、测试点：订阅港股指数实时K线
        self.step_base(code_list= ['HK.800000'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncCurKline_hk_etf(self):
        #1、测试点：订阅港股基金实时K线
        self.step_base(code_list= ['HK.02800'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncCurKline_hk_bond(self):
        #1、测试点：订阅港股债券实时K线
        self.step_base(code_list= ['HK.04231'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncCurKline_us_stock(self):
        #1、测试点：订阅美股正股实时K线
        self.step_base(code_list= ['US.AAPL'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncCurKline_us_idx(self):
        #1、测试点：订阅美股指数实时K线
        self.step_base(code_list= ['US..IXIC'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncCurKline_us_etf(self):
        #1、测试点：订阅美股指数实时K线
        self.step_base(code_list= ['US.YINN'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncCurKline_us_drvt(self):
        #1、测试点：订阅美股期权实时K线

        #获取期权代码
        codes = []
        drvt_call_ret_code, drvt_call_ret_data = quote_ctx1.get_option_chain(code='US.GOOG',
                                                                                 option_type=OptionType.CALL,
                                                                                 option_cond_type=OptionCondType.ALL)

        if drvt_call_ret_code==RET_OK:
            codes.append(drvt_call_ret_data['code'].tolist()[0])
        else:
            codes = ['US.DIS180907P95000']

        #执行测试步骤
        self.step_base(code_list= codes, casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncCurKline_cn_stock(self):
        #1、测试点：订阅A股正股实时K线
        self.step_base(code_list= ['SZ.000001' ,'SH.601318'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncCurKline_cn_idx(self):
        #1、测试点：订阅A股指数实时K线
        self.step_base(code_list= ['SH.000001'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncCurKline_cn_etf(self):
        #1、测试点：订阅A股指基金实时K线
        self.step_base(code_list= ['SH.501053'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验


class CureKlineTest1(CurKlineHandlerBase):
    # 监听实时K线推送
    def on_recv_rsp(self, rsp_str):
        '''
        回调
        :param rsp_str:
        :return:
        '''
        ret_code, ret_data = super(CureKlineTest1, self).on_recv_rsp(rsp_str) # 基类的on_recv_rsp方法解包返回了K线信息
        #打印,记录日志
        print(ret_data, file=f1, flush=True)

        return RET_OK, ret_data

class CureKlineTest2(CurKlineHandlerBase):
    # 监听实时K线推送
    def on_recv_rsp(self, rsp_str):
        '''
        回调
        :param rsp_str:
        :return:
        '''
        ret_code, ret_data = super(CureKlineTest2, self).on_recv_rsp(rsp_str) # 基类的on_recv_rsp方法解包返回了K线信息
        #打印,记录日志
        print(ret_data, file=f2, flush=True)

        return RET_OK, ret_data


if __name__ == '__main__':
    quote_ctx1 = OpenQuoteContext(host='127.0.0.1', port=11111)
    quote_ctx2 = OpenQuoteContext(host='127.0.0.1', port=11121)
    pandas.set_option('max_columns', 100)
    pandas.set_option('display.width', 1000)
    pandas.set_option('display.max_rows', 1000)
    unittest.main()
















# f = open('test_cur_kline.txt', 'a')
# class CurKlineTest(CurKlineHandlerBase):
#     def on_recv_rsp(self, rsp_str):
#         ret_code, data = super(CurKlineTest,self).on_recv_rsp(rsp_str)
#         if ret_code != RET_OK:
#             print("CurKlineTest: error, msg: %s" % data)
#             return RET_ERROR, data
#
#         # print(data, file=f, flush=True)  # CurKlineTest自己的处理逻辑
#         print(data)
#
#         return RET_OK, data

# def test_cur_kline():
#     pandas.set_option('max_columns', 100)
#     pandas.set_option('display.width', 1000)
#     quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
#     quote_ctx.subscribe(['HK.00700'], SubType.K_MON)
#     print(quote_ctx.get_cur_kline('HK.00700', 8, SubType.K_MON , AuType.QFQ))
#     quote_ctx.close()


# if __name__ == '__main__':
#     pandas.set_option('max_columns', 100)
#     pandas.set_option('display.width', 1000)
#     quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11112)
#     quote_ctx.set_handler(CurKlineTest())
#     quote_ctx.subscribe(['HK_FUTURE.999010', 'US.AAPL'], [SubType.K_DAY, SubType.K_5M])# SubType.K_1M,
#     quote_ctx.start()
    # while True:
    #     print(quote_ctx.get_cur_kline('HK.00700', 700, SubType.K_DAY))

