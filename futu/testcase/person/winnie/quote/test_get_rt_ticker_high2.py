from futu import *
import pandas
import sys
import datetime
import unittest
import random
from futu.testcase.person.winnie.quote.compare_data import *


f2 = open('test_new_protoco2.txt','a')


class AsyncTicker(unittest.TestCase):
    '''
    实时逐笔推送测试类
    '''

    def step_base(self, code_list, casename=sys._getframe().f_code.co_name ):
        '''
        基本测试步骤
        :param code_list:待订阅的股票代码列表
        :return:
        '''
        #打印日志：测试用例名
        print(casename, file=f2, flush=True)
        #设置监听
        handler2 = TickerTest2()
        quote_ctx2.set_handler(handler2)
        #订阅逐笔
        quote_ctx2.subscribe(code_list, SubType.TICKER)

    def test_asyncTicker_hk_stock(self):
        #1、测试点：订阅港股正股实时逐笔
        self.step_base(code_list= ['HK.00700'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncTicker_hk_wrrant(self):
        # 1、测试点：订阅港股涡轮实时逐笔

        #获取涡轮代码
        codes_warrant = 'HK.28070'
        #执行测试步骤
        self.step_base(code_list=codes_warrant, casename=sys._getframe().f_code.co_name )

        # 2、校验
        # 不合适在此处校验，需跑完一整天数据后校验

    def test_asyncTicker_hk_future_stock(self):
        #1、测试点：订阅港股期货实时逐笔
        self.step_base(code_list= ['HK_FUTURE.999010'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncTicker_hk_idx(self):
        #1、测试点：订阅港股指数实时逐笔
        self.step_base(code_list= ['HK.800000'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncTicker_hk_etf(self):
        #1、测试点：订阅港股基金实时逐笔
        self.step_base(code_list= ['HK.02800'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncTicker_hk_bond(self):
        #1、测试点：订阅港股债券实时逐笔
        self.step_base(code_list= ['HK.04231'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncTicker_us_stock(self):
        #1、测试点：订阅美股正股实时逐笔
        self.step_base(code_list= ['US.AAPL'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncTicker_us_idx(self):
        #1、测试点：订阅美股指数实时逐笔
        self.step_base(code_list= ['US..IXIC'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncTicker_us_etf(self):
        #1、测试点：订阅美股指数实时逐笔
        self.step_base(code_list= ['US.YINN'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncTicker_us_drvt(self):
        #1、测试点：订阅美股期权实时逐笔

        #获取期权代码
        codes = []
        drvt_call_ret_code, drvt_call_ret_data = quote_ctx2.get_option_chain(code='US.GOOG',
                                                                             option_type=OptionType.CALL,
                                                                             option_cond_type=OptionCondType.ALL)
        drvt_put_ret_code, drvt_put_ret_data = quote_ctx2.get_option_chain(code='US.GOOG',
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

    def test_asyncTicker_cn_stock(self):
        #1、测试点：订阅A股正股实时逐笔
        self.step_base(code_list= ['SZ.000001' ,'SH.601318'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncTicker_cn_idx(self):
        #1、测试点：订阅A股指数实时逐笔
        self.step_base(code_list= ['SH.000001' ,'SZ.399001'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncTicker_cn_etf(self):
        #1、测试点：订阅A股指基金实时逐笔
        self.step_base(code_list= ['SH.501053' ,'SZ.164824'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验


class TickerTest2(TickerHandlerBase):

    def on_recv_rsp(self, rsp_str):
        '''
        回调
        :param rsp_str:
        :return:
        '''
        ret_code, ret_data = super(TickerTest2, self).on_recv_rsp(rsp_str) # 基类的on_recv_rsp方法解包返回了逐笔信息
        print(ret_data, file=f2, flush=True)

        return RET_OK, ret_data


if __name__ == '__main__':
    # SysConfig.set_all_thread_daemon(True)
    # 旧协议
    quote_ctx2 = OpenQuoteContext('127.0.0.1', 11121)
    pandas.set_option('max_columns', 100)
    pandas.set_option('display.width', 1000)
    # grt = GetRtTicker()
    # grt.test_get_rt_ticker_us_drvt()
    unittest.main()
