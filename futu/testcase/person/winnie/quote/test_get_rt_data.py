# -*- coding:utf-8 -*-
from futu import *
import pandas
import unittest
from futu.testcase.person.winnie.quote.compare_data import *

f1 = open('test_new_protocol.txt','a')
f2 = open('test_new_protoco2.txt','a')

class GetRtData(unittest.TestCase):
    '''
    测试类:获取分时数据
    '''

    # 各市场各股票类型的分时测试步骤和校验
    def step_check_base1(self, casename, code):
        '''
        测试点：各市场各股票类型的分时
        :param casename:
        :param code:
        :return:
        '''
        ret_code_sub, ret_data_sub = quote_ctx1.subscribe(code, SubType.RT_DATA)
        print(casename)
        print(casename, file=f1, flush=True)
        print(casename, file=f2, flush=True)
        ret_code, ret_data1 = quote_ctx1.get_rt_data(code)
        print(ret_data1, file=f1, flush=True)
        ret_code_sub, ret_data_sub = quote_ctx2.subscribe(code, SubType.RT_DATA)
        ret_code, ret_data2 = quote_ctx2.get_rt_data(code)
        print(ret_data2, file=f2, flush=True)
        print(CompareData().compare(ret_data1, ret_data2))

    #港股
    def test_get_rt_data_hk_stock(self):
        '''
        测试点：获取某一港股正股的分时
        :return:
        '''
        casename = sys._getframe().f_code.co_name
        code = 'HK.00700'
        self.step_check_base1(casename,code)

    def test_get_rt_data_hk_wrt(self):
        '''
        测试点：获取某一港股涡轮的分时
        :return:
        '''
        casename = sys._getframe().f_code.co_name
        code = 'HK.28552'
        self.step_check_base1(casename,code)

    def test_get_rt_data_hk_idx(self):
        '''
        测试点：获取港股指数的分时
        :return:
        '''
        casename = sys._getframe().f_code.co_name
        code = 'HK.800100'
        self.step_check_base1(casename,code)

    def test_get_rt_data_hk_futrue(self):
        '''
        测试点：获取港股期货的分时
        :return:
        '''
        casename = sys._getframe().f_code.co_name
        code = 'HK_FUTURE.999010'
        self.step_check_base1(casename,code)

    #美股
    def test_get_rt_data_us_stock(self):
        '''
        测试点：获取某一美股正股的分时
        :return:
        '''
        casename = sys._getframe().f_code.co_name
        code = 'US.JD'
        self.step_check_base1(casename, code)

    def test_get_rt_data_us_drvt(self):
        '''
        测试点：获取某一美股期权的分时
        :return:
        '''
        casename = sys._getframe().f_code.co_name
        code = 'US.AAPL190104C162500'
        self.step_check_base1(casename,code)

    def test_get_rt_data_us_idx(self):
        '''
        测试点：获取美股指数的分时
        :return:
        '''
        casename = sys._getframe().f_code.co_name
        code = 'US..IXIC'
        self.step_check_base1(casename,code)

    # A股
    def test_get_rt_data_sh_stock(self):
        '''
        测试点：获取某一A股正股的分时
        :return:
        '''
        casename = sys._getframe().f_code.co_name
        code = 'SH.603131'
        self.step_check_base1(casename, code)

    def test_get_rt_data_sz_stock(self):
        '''
        测试点：获取某一A股正股的分时
        :return:
        '''
        casename = sys._getframe().f_code.co_name
        code = 'SZ.300710'
        self.step_check_base1(casename, code)

    def test_get_rt_data_cn_idx(self):
        '''
        测试点：获取A股指数的分时
        :return:
        '''
        casename = sys._getframe().f_code.co_name
        code = 'SZ.399001'
        self.step_check_base1(casename, code)

    # code入参错误
    def test_get_rt_data_err_code_none(self):
        code = None
        casename = sys._getframe().f_code.co_name
        print(casename)
        print(casename, file=f1, flush=True)
        print(casename, file=f2, flush=True)
        ret_code_sub, ret_data_sub = quote_ctx1.subscribe(code, SubType.RT_DATA)
        ret_code, ret_data1 = quote_ctx1.get_rt_data(code)
        print(ret_data1, file=f1, flush=True)

        ret_code_sub, ret_data_sub = quote_ctx2.subscribe(code, SubType.RT_DATA)
        ret_code, ret_data2 = quote_ctx2.get_rt_data(code)
        print(ret_data2, file=f2, flush=True)

        print(CompareData().compare(ret_data1, ret_data2))

    def test_get_rt_data_err_code_fmtErr(self):
        code = ['HK.00700']
        casename = sys._getframe().f_code.co_name
        print(casename)
        ret_code_sub, ret_data_sub = quote_ctx1.subscribe(code, SubType.RT_DATA)
        ret_code, ret_data1 = quote_ctx1.get_rt_data(code)
        ret_code_sub, ret_data_sub = quote_ctx2.subscribe(code, SubType.RT_DATA)
        ret_code, ret_data2 = quote_ctx2.get_rt_data(code)
        print(casename, file=f1, flush=True)
        print(ret_data1, file=f1, flush=True)

        ret_code_sub, ret_data_sub = quote_ctx2.subscribe(code, SubType.RT_DATA)
        ret_code, ret_data2 = quote_ctx2.get_rt_data(code)
        print(casename, file=f2, flush=True)
        print(ret_data2, file=f2, flush=True)
        print(CompareData().compare(ret_data1, ret_data2))

    # 订阅板块和正股，反订阅板块正股是否正常
    def test_get_rt_data_bk_stock_unsubscribe_bk(self):
        casename = sys._getframe().f_code.co_name
        code_list = ['HK.00700','SH.BK0001']
        print(casename)
        print(casename, file=f1, flush=True)
        print(casename, file=f2, flush=True)
        quote_ctx1.subscribe(code_list,SubType.RT_DATA)
        ret_code, ret_data1 = quote_ctx1.get_rt_data(code_list[0])
        print(ret_data1, file=f1, flush=True)
        ret_code, ret_data1 = quote_ctx1.get_rt_data(code_list[1])
        print(ret_data1, file=f1, flush=True)
        quote_ctx2.subscribe(code_list, SubType.RT_DATA)
        ret_code, ret_data2 = quote_ctx2.get_rt_data(code_list[0])
        print(ret_data2, file=f2, flush=True)
        ret_code, ret_data2 = quote_ctx2.get_rt_data(code_list[1])
        print(ret_data2, file=f2, flush=True)
        print(CompareData().compare(ret_data1, ret_data2))
        time.sleep(60)
        quote_ctx1.unsubscribe('SH.BK0001',SubType.RT_DATA)
        ret_code, ret_data1 = quote_ctx1.get_rt_data(code_list[0])
        print(ret_data1, file=f1, flush=True)
        quote_ctx2.unsubscribe('SH.BK0001', SubType.RT_DATA)
        ret_code, ret_data2 = quote_ctx2.get_rt_data(code_list[0])
        print(ret_data2, file=f2, flush=True)
        print(CompareData().compare(ret_data1, ret_data2))


    # 订阅板块和正股，反订阅板块正股是否正常
    def test_get_rt_data_bk_stock_unsubscribe_stock(self):
        casename = sys._getframe().f_code.co_name
        print(casename)
        print(casename, file=f1, flush=True)
        print(casename, file=f2, flush=True)
        code_list = ['HK.00700','SH.BK0001']
        quote_ctx1.subscribe(code_list,SubType.RT_DATA)
        ret_code, ret_data1 = quote_ctx1.get_rt_data(code_list[0])
        print(ret_data1, file=f1, flush=True)
        ret_code, ret_data1 = quote_ctx1.get_rt_data(code_list[1])
        print(ret_data1, file=f1, flush=True)
        quote_ctx2.subscribe(code_list, SubType.RT_DATA)
        ret_code, ret_data2 = quote_ctx2.get_rt_data(code_list[0])
        print(ret_data2, file=f2, flush=True)
        ret_code, ret_data2 = quote_ctx2.get_rt_data(code_list[1])
        print(ret_data2, file=f2, flush=True)
        print(CompareData().compare(ret_data1, ret_data2))
        time.sleep(60)
        quote_ctx1.unsubscribe('HK.00700',SubType.RT_DATA)
        ret_code, ret_data1 = quote_ctx1.get_rt_data(code_list[1])
        print(ret_data1, file=f1, flush=True)
        quote_ctx2.unsubscribe('HK.00700', SubType.RT_DATA)
        ret_code, ret_data2 = quote_ctx2.get_rt_data(code_list[1])
        print(ret_data2, file=f2, flush=True)
        print(CompareData().compare(ret_data1, ret_data2))


# class AsyncRTData(unittest.TestCase):
#     '''
#     实时分时推送测试类
#     '''
#
#     def step_base(self, code_list, casename=sys._getframe().f_code.co_name ):
#         '''
#         基本测试步骤
#         :param code_list:待订阅的股票代码列表
#         :return:
#         '''
#         #打印日志：测试用例名
#         # print(casename, file=f, flush=True)
#         #设置监听
#         handler1 = RTDataTest1()
#         handler2 = RTDataTest2()
#         quote_ctx1.set_handler(handler1)
#         quote_ctx2.set_handler(handler2)
#         #订阅分时
#         quote_ctx1.subscribe(code_list, SubType.RT_DATA)
#         quote_ctx2.subscribe(code_list, SubType.RT_DATA)
#
#     def test_asyncRTData_hk_stock(self):
#         #1、测试点：订阅港股正股实时分时
#         self.step_base(code_list= ['HK.00700'], casename=sys._getframe().f_code.co_name )
#
#         #2、校验
#         #不合适在此处校验，需跑完一整天数据后校验
#
#     def test_asyncRTData_hk_wrrant(self):
#         # 1、测试点：订阅港股涡轮实时分时
#
#         #获取认沽、认购、牛证、熊证代码
#         codes_warrant = 'HK.13322'
#         #执行测试步骤
#         self.step_base(code_list=codes_warrant, casename=sys._getframe().f_code.co_name )
#
#         # 2、校验
#         # 不合适在此处校验，需跑完一整天数据后校验
#
#     def test_asyncRTData_hk_future_stock(self):
#         #1、测试点：订阅港股期货实时分时
#         self.step_base(code_list= ['HK_FUTURE.999010'], casename=sys._getframe().f_code.co_name )
#
#         #2、校验
#         #不合适在此处校验，需跑完一整天数据后校验
#
#     def test_asyncRTData_hk_idx(self):
#         #1、测试点：订阅港股指数实时分时
#         self.step_base(code_list= ['HK.800000'], casename=sys._getframe().f_code.co_name )
#
#         #2、校验
#         #不合适在此处校验，需跑完一整天数据后校验
#
#     def test_asyncRTData_hk_etf(self):
#         #1、测试点：订阅港股基金实时分时
#         self.step_base(code_list= ['HK.02800'], casename=sys._getframe().f_code.co_name )
#
#         #2、校验
#         #不合适在此处校验，需跑完一整天数据后校验
#
#     def test_asyncRTData_hk_bond(self):
#         #1、测试点：订阅港股债券实时分时
#         self.step_base(code_list= ['HK.04231'], casename=sys._getframe().f_code.co_name )
#
#         #2、校验
#         #不合适在此处校验，需跑完一整天数据后校验
#
#     def test_asyncRTData_us_stock(self):
#         #1、测试点：订阅美股正股实时分时
#         self.step_base(code_list= ['US.AAPL'], casename=sys._getframe().f_code.co_name )
#
#         #2、校验
#         #不合适在此处校验，需跑完一整天数据后校验
#
#     def test_asyncRTData_us_idx(self):
#         #1、测试点：订阅美股指数实时分时
#         self.step_base(code_list= ['US..IXIC'], casename=sys._getframe().f_code.co_name )
#
#         #2、校验
#         #不合适在此处校验，需跑完一整天数据后校验
#
#     def test_asyncRTData_us_etf(self):
#         #1、测试点：订阅美股指数实时分时
#         self.step_base(code_list= ['US.YINN'], casename=sys._getframe().f_code.co_name )
#
#         #2、校验
#         #不合适在此处校验，需跑完一整天数据后校验
#
#     def test_asyncRTData_us_drvt(self):
#         #1、测试点：订阅美股期权实时分时
#
#         #获取期权代码
#         codes = []
#         drvt_call_ret_code, drvt_call_ret_data = quote_ctx1.get_option_chain(code='US.GOOG',
#                                                                                  option_type=OptionType.CALL,
#                                                                                  option_cond_type=OptionCondType.ALL)
#         drvt_put_ret_code, drvt_put_ret_data = quote_ctx1.get_option_chain(code='US.GOOG',
#                                                                                  option_type=OptionType.PUT,
#                                                                                  option_cond_type=OptionCondType.ALL)
#         if drvt_put_ret_code==RET_OK and drvt_call_ret_code==RET_OK:
#             codes.append(drvt_call_ret_data['code'].tolist()[0])
#             codes.append(drvt_put_ret_data['code'].tolist()[0])
#         else:
#             codes = ['US.DIS180907P95000', 'US.DIS180907C111000']
#
#         #执行测试步骤
#         self.step_base(code_list= codes, casename=sys._getframe().f_code.co_name )
#
#         #2、校验
#         #不合适在此处校验，需跑完一整天数据后校验
#
#     def test_asyncRTData_cn_stock(self):
#         #1、测试点：订阅A股正股实时分时
#         self.step_base(code_list= ['SZ.000001' ,'SH.601318'], casename=sys._getframe().f_code.co_name )
#
#         #2、校验
#         #不合适在此处校验，需跑完一整天数据后校验
#
#     def test_asyncRTData_cn_idx(self):
#         #1、测试点：订阅A股指数实时分时
#         self.step_base(code_list= ['SH.000001' ,'SZ.399001'], casename=sys._getframe().f_code.co_name )
#
#         #2、校验
#         #不合适在此处校验，需跑完一整天数据后校验
#
#     def test_asyncRTData_cn_etf(self):
#         #1、测试点：订阅A股指基金实时分时
#         self.step_base(code_list= ['SH.501053' ,'SZ.164824'], casename=sys._getframe().f_code.co_name )
#
#         #2、校验
#         #不合适在此处校验，需跑完一整天数据后校验
#
#
# class RTDataTest1(RTDataHandlerBase):
#     def on_recv_rsp(self, rsp_str):
#         '''
#         回调
#         :param rsp_str:
#         :return:
#         '''
#         ret_code, ret_data = super(RTDataTest1, self).on_recv_rsp(rsp_str) # 基类的on_recv_rsp方法解包返回了分时信息
#         print(ret_data, file=f1, flush=True)
#
#         return RET_OK, ret_data
#
# class RTDataTest2(RTDataHandlerBase):
#     def on_recv_rsp(self, rsp_str):
#         '''
#         回调
#         :param rsp_str:
#         :return:
#         '''
#         ret_code, ret_data = super(RTDataTest2, self).on_recv_rsp(rsp_str) # 基类的on_recv_rsp方法解包返回了分时信息
#         print(ret_data, file=f2, flush=True)
#
#         return RET_OK, ret_data

if __name__ == '__main__':
    quote_ctx1 = OpenQuoteContext('127.0.0.1', 11111)
    quote_ctx2 = OpenQuoteContext('127.0.0.1', 11111)
    pandas.set_option('max_columns', 100)
    pandas.set_option('display.width', 1000)
    pandas.set_option('display.max_rows', 1000)
    # unittest.main()
    codes = ['US.JD','US..IXIC','US.AAPL190104C162500']
    for code in codes:
        print(quote_ctx1.subscribe(code, SubType.RT_DATA))
        print(quote_ctx1.get_rt_data(code))
