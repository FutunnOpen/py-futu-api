# -*- coding:utf-8 -*-
from futuquant import *
import pandas
import unittest

f = open('test_new_protocol.txt','a')

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
        ret_code_sub, ret_data_sub = quote_ctx.subscribe(code, SubType.RT_DATA)
        ret_code, ret_data = quote_ctx.get_rt_data(code)
        print(ret_data, file=f, flush=True)
        #校验点1、请求成功，且数据不为空
        self.assertEqual(ret_code, RET_OK)
        self.assertTrue(len(ret_data) >0)
        #校验点2、返回的股票与入参code一致
        code_list = ret_data['code']
        for index in range(len(ret_data)):
            self.assertTrue( code_list[index] == code, 'Error: index = %d' % index)

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
        code = 'US.DIS181123P110000'
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
        ret_code_sub, ret_data_sub = quote_ctx.subscribe(code, SubType.RT_DATA)
        ret_code, ret_data = quote_ctx.get_rt_data(code)
        print(casename, file=f, flush=True)
        print(ret_data, file=f, flush=True)
        #校验
        self.assertEqual(ret_code, RET_ERROR)

    def test_get_rt_data_err_code_fmtErr(self):
        code = ['HK.00700']
        casename = sys._getframe().f_code.co_name
        ret_code_sub, ret_data_sub = quote_ctx.subscribe(code, SubType.RT_DATA)
        ret_code, ret_data = quote_ctx.get_rt_data(code)
        print(casename, file=f, flush=True)
        print(ret_data, file=f, flush=True)
        #校验
        self.assertEqual(ret_code, RET_ERROR)

    # 订阅板块和正股，反订阅板块正股是否正常
    def test_get_rt_data_bk_stock_unsubscribe_bk(self):
        casename = sys._getframe().f_code.co_name
        code_list = ['HK.00700','SH.BK0001']
        quote_ctx.subscribe(code_list,SubType.RT_DATA)
        ret_code, ret_data = quote_ctx.get_rt_data(code_list[0])
        print(casename, file=f, flush=True)
        print(ret_data, file=f, flush=True)
        ret_code, ret_data = quote_ctx.get_rt_data(code_list[1])
        print(ret_data, file=f, flush=True)
        time.sleep(60)
        quote_ctx.unsubscribe('SH.BK0001',SubType.RT_DATA)
        ret_code, ret_data = quote_ctx.get_rt_data(code_list[0])
        print(ret_data, file=f, flush=True)

    # 订阅板块和正股，反订阅板块正股是否正常
    def test_get_rt_data_bk_stock_unsubscribe_stock(self):
        casename = sys._getframe().f_code.co_name
        code_list = ['HK.00700','SH.BK0001']
        quote_ctx.subscribe(code_list,SubType.RT_DATA)
        ret_code, ret_data = quote_ctx.get_rt_data(code_list[0])
        print(casename, file=f, flush=True)
        print(ret_data, file=f, flush=True)
        ret_code, ret_data = quote_ctx.get_rt_data(code_list[1])
        print(ret_data, file=f, flush=True)
        time.sleep(60)
        quote_ctx.unsubscribe('HK.00700',SubType.RT_DATA)
        ret_code, ret_data = quote_ctx.get_rt_data(code_list[1])
        print(ret_data, file=f, flush=True)


class AsyncRTData(unittest.TestCase):
    '''
    实时分时推送测试类
    '''

    def step_base(self, code_list, casename=sys._getframe().f_code.co_name ):
        '''
        基本测试步骤
        :param code_list:待订阅的股票代码列表
        :return:
        '''
        #打印日志：测试用例名
        print(casename, file=f, flush=True)
        #设置监听
        handler = RTDataTest()
        quote_ctx.set_handler(handler)
        #订阅分时
        quote_ctx.subscribe(code_list, SubType.RT_DATA)

    def test_asyncRTData_hk_stock(self):
        #1、测试点：订阅港股正股实时分时
        self.step_base(code_list= ['HK.00700'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncRTData_hk_wrrant(self):
        # 1、测试点：订阅港股涡轮实时分时

        #获取认沽、认购、牛证、熊证代码
        codes_warrant = 'HK.13322'
        #执行测试步骤
        self.step_base(code_list=codes_warrant, casename=sys._getframe().f_code.co_name )

        # 2、校验
        # 不合适在此处校验，需跑完一整天数据后校验

    def test_asyncRTData_hk_future_stock(self):
        #1、测试点：订阅港股期货实时分时
        self.step_base(code_list= ['HK_FUTURE.999010'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncRTData_hk_idx(self):
        #1、测试点：订阅港股指数实时分时
        self.step_base(code_list= ['HK.800000'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncRTData_hk_etf(self):
        #1、测试点：订阅港股基金实时分时
        self.step_base(code_list= ['HK.02800'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncRTData_hk_bond(self):
        #1、测试点：订阅港股债券实时分时
        self.step_base(code_list= ['HK.04231'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncRTData_us_stock(self):
        #1、测试点：订阅美股正股实时分时
        self.step_base(code_list= ['US.AAPL'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncRTData_us_idx(self):
        #1、测试点：订阅美股指数实时分时
        self.step_base(code_list= ['US..IXIC'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncRTData_us_etf(self):
        #1、测试点：订阅美股指数实时分时
        self.step_base(code_list= ['US.YINN'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncRTData_us_drvt(self):
        #1、测试点：订阅美股期权实时分时

        #获取期权代码
        codes = []
        drvt_call_ret_code, drvt_call_ret_data = quote_ctx.get_option_chain(code='US.GOOG',
                                                                                 option_type=OptionType.CALL,
                                                                                 option_cond_type=OptionCondType.ALL)
        drvt_put_ret_code, drvt_put_ret_data = quote_ctx.get_option_chain(code='US.GOOG',
                                                                                 option_type=OptionType.PUT,
                                                                                 option_cond_type=OptionCondType.ALL)
        if drvt_put_ret_code==RET_OK and drvt_call_ret_code==RET_OK:
            codes.append(drvt_call_ret_data['code'].tolist()[0])
            codes.append(drvt_put_ret_data['code'].tolist()[0])
        else:
            codes = ['US.DIS180907P95000', 'US.DIS180907C111000']

        #执行测试步骤
        self.step_base(code_list= codes, casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncRTData_cn_stock(self):
        #1、测试点：订阅A股正股实时分时
        self.step_base(code_list= ['SZ.000001' ,'SH.601318'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncRTData_cn_idx(self):
        #1、测试点：订阅A股指数实时分时
        self.step_base(code_list= ['SH.000001' ,'SZ.399001'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncRTData_cn_etf(self):
        #1、测试点：订阅A股指基金实时分时
        self.step_base(code_list= ['SH.501053' ,'SZ.164824'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验


class RTDataTest(RTDataHandlerBase):
    def on_recv_rsp(self, rsp_str):
        '''
        回调
        :param rsp_str:
        :return:
        '''
        ret_code, ret_data = super(RTDataTest, self).on_recv_rsp(rsp_str) # 基类的on_recv_rsp方法解包返回了分时信息
        print(ret_data, file=f, flush=True)

        return RET_OK, ret_data


if __name__ == '__main__':
    quote_ctx = OpenQuoteContext('127.0.0.1',11122)
    pandas.set_option('max_columns', 100)
    pandas.set_option('display.width', 1000)
    unittest.main()
