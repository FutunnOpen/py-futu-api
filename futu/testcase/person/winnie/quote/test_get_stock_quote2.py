# import time
from futu import *
import pandas
import sys
import unittest

# f1 = open('test_stock_quote1.txt','a')
f2 = open('test_stock_quote2.txt','a')

class AsyncStockQuote(unittest.TestCase):
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
        print(casename, file=f2, flush=True)
        #设置监听
        handler = StockQuoteTest()
        quote_ctx2.set_handler(handler)
        #订阅报价
        quote_ctx2.subscribe(code_list, SubType.QUOTE)

    def test_asyncStockQuote_hk_stock(self):
        #1、测试点：订阅港股正股实时报价
        self.step_base(code_list= ['HK.00700'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncStockQuote_hk_wrrant(self):
        # 1、测试点：订阅港股涡轮实时报价

        #获取认沽、认购、牛证、熊证代码
        codes_warrant = 'HK.13322'
        #执行测试步骤
        self.step_base(code_list=codes_warrant, casename=sys._getframe().f_code.co_name )

        # 2、校验
        # 不合适在此处校验，需跑完一整天数据后校验

    def test_asyncStockQuote_hk_future_stock(self):
        #1、测试点：订阅港股期货实时报价
        self.step_base(code_list= ['HK_FUTURE.999010'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncStockQuote_hk_idx(self):
        #1、测试点：订阅港股指数实时报价
        self.step_base(code_list= ['HK.800000'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncStockQuote_hk_etf(self):
        #1、测试点：订阅港股基金实时报价
        self.step_base(code_list= ['HK.02800'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncStockQuote_hk_bond(self):
        #1、测试点：订阅港股债券实时报价
        self.step_base(code_list= ['HK.04231'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncStockQuote_us_stock(self):
        #1、测试点：订阅美股正股实时报价
        self.step_base(code_list= ['US.AAPL'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncStockQuote_us_idx(self):
        #1、测试点：订阅美股指数实时报价
        self.step_base(code_list= ['US..IXIC'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncStockQuote_us_etf(self):
        #1、测试点：订阅美股指数实时报价
        self.step_base(code_list= ['US.YINN'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncStockQuote_us_drvt(self):
        #1、测试点：订阅美股期权实时报价

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

    def test_asyncStockQuote_cn_stock(self):
        #1、测试点：订阅A股正股实时报价
        self.step_base(code_list= ['SZ.000001' ,'SH.601318'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncStockQuote_cn_idx(self):
        #1、测试点：订阅A股指数实时报价
        self.step_base(code_list= ['SH.000001' ,'SZ.399001'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncStockQuote_cn_etf(self):
        #1、测试点：订阅A股指基金实时报价
        self.step_base(code_list= ['SH.501053' ,'SZ.164824'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验


class StockQuoteTest(StockQuoteHandlerBase):
    def on_recv_rsp(self, rsp_str):
        '''
        回调
        :param rsp_str:
        :return:
        '''
        ret_code, data = super(StockQuoteTest,self).on_recv_rsp(rsp_str) # 基类的on_recv_rsp方法解包返回了报价信息

        print(data, file=f2,flush=True)

        return RET_OK, data


if __name__ == '__main__':
    # quote_ctx1 = OpenQuoteContext('127.0.0.1', 11111)
    quote_ctx2 = OpenQuoteContext('127.0.0.1',11121)
    pandas.set_option('max_columns', 100)
    pandas.set_option('display.width', 1000)
    # a =  AsyncStockQuote()
    # a.test_asyncStockQuote_hk_stock()
    unittest.main()
    # tq = TestQuote()
    # tq.test1()
