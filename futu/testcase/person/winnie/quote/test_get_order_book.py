# -*- coding:utf-8 -*-
from futuquant import *
import unittest
import pandas

f = open('test_new_protocol.txt','a')


class GetOrderBook(unittest.TestCase):
    def common_get_order_book(self, code, fun_name):
        print(fun_name, file=f, flush=True)
        quote_ctx.subscribe(code, SubType.ORDER_BOOK)
        ret_code, ret_data = quote_ctx.get_order_book(code)
        print(ret_data, file=f, flush=True)

    # 有效传参获取港股正股摆盘
    def test_get_order_book_hk_stock_valid(self):
        code = 'HK.00700'
        fun_name = sys._getframe().f_code.co_name
        self.common_get_order_book(code, fun_name)
        # 无法校验

    # 有效传参获取港股涡轮摆盘
    def test_get_order_book_hk_warrant_valid(self):
        code = 'HK.59517'
        fun_name = sys._getframe().f_code.co_name
        self.common_get_order_book(code, fun_name)
        # 无法校验

    # 有效传参获取港股指数摆盘
    def test_get_order_book_hk_idx_valid(self):
        code = 'SH.000001'
        fun_name = sys._getframe().f_code.co_name
        self.common_get_order_book(code, fun_name)
        # 无法校验

    # 有效传参获取行股期货摆盘
    def test_get_order_book_hk_future_valid(self):
        code = 'HK_FUTURE.999010'
        fun_name = sys._getframe().f_code.co_name
        self.common_get_order_book(code, fun_name)
        # 无法校验

    # 有效传参获取美股正股摆盘
    def test_get_order_book_us_stock_valid(self):
        code = 'US.AAPL'
        fun_name = sys._getframe().f_code.co_name
        self.common_get_order_book(code, fun_name)
        # 无法校验

    # 有效传参获取美股指数摆盘
    def test_get_order_book_us_idx_valid(self):
        code = 'US..DJI'
        fun_name = sys._getframe().f_code.co_name
        self.common_get_order_book(code, fun_name)
        # 无法校验

    # 有效传参获取美股ETF摆盘
    def test_get_order_book_us_etf_valid(self):
        code = 'US.UBR'
        fun_name = sys._getframe().f_code.co_name
        self.common_get_order_book(code, fun_name)
        # 无法校验

    # 有效传参获取A股stock摆盘
    def test_get_order_book_ch_stock_valid(self):
        code = 'SH.601989'
        fun_name = sys._getframe().f_code.co_name
        self.common_get_order_book(code, fun_name)
        # 无法校验

    # 有效传参获取A股指数摆盘
    def test_get_order_book_ch_idx_valid(self):
        code = 'SZ.000001'
        fun_name = sys._getframe().f_code.co_name
        self.common_get_order_book(code, fun_name)
        # 无法校验


class AsyncOrderBook(unittest.TestCase):
    '''
    实时摆盘数据推送测试类
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
        handler = OrderBookTest()
        quote_ctx.set_handler(handler)
        #订阅摆盘
        quote_ctx.subscribe(code_list, SubType.ORDER_BOOK)

    def test_asyncOrderBook_hk_stock(self):
        #1、测试点：订阅港股正股实时摆盘
        self.step_base(code_list= ['HK.00700'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncOrderBook_hk_wrrant(self):
        # 1、测试点：订阅港股涡轮实时摆盘

        #获取认沽、认购、牛证、熊证代码
        codes_warrant = 'HK.11875'
        #执行测试步骤
        self.step_base(code_list=codes_warrant, casename=sys._getframe().f_code.co_name )

        # 2、校验
        # 不合适在此处校验，需跑完一整天数据后校验

    def test_asyncOrderBook_hk_future_stock(self):
        #1、测试点：订阅港股期货实时摆盘
        self.step_base(code_list= ['HK_FUTURE.999010'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncOrderBook_hk_idx(self):
        #1、测试点：订阅港股指数实时摆盘
        self.step_base(code_list= ['HK.800000'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncOrderBook_hk_etf(self):
        #1、测试点：订阅港股基金实时摆盘
        self.step_base(code_list= ['HK.02800'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncOrderBook_hk_bond(self):
        #1、测试点：订阅港股债券实时摆盘
        self.step_base(code_list= ['HK.04231'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncOrderBook_us_stock(self):
        #1、测试点：订阅美股正股实时摆盘
        self.step_base(code_list= ['US.AAPL'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncOrderBook_us_idx(self):
        #1、测试点：订阅美股指数实时摆盘
        self.step_base(code_list= ['US..IXIC'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncOrderBook_us_etf(self):
        #1、测试点：订阅美股指数实时摆盘
        self.step_base(code_list= ['US.YINN'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncOrderBook_us_drvt(self):
        #1、测试点：订阅美股期权实时摆盘

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

    def test_asyncOrderBook_cn_stock(self):
        #1、测试点：订阅A股正股实时摆盘
        self.step_base(code_list= ['SZ.000001' ,'SH.601318'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncOrderBook_cn_idx(self):
        #1、测试点：订阅A股指数实时摆盘
        self.step_base(code_list= ['SH.000001' ,'SZ.399001'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncOrderBook_cn_etf(self):
        #1、测试点：订阅A股指基金实时摆盘
        self.step_base(code_list= ['SH.501053' ,'SZ.164824'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验


class OrderBookTest(OrderBookHandlerBase):

    def on_recv_rsp(self, rsp_str):
        '''
        回调
        :param rsp_str:
        :return:
        '''
        ret_code, ret_data = super(OrderBookTest,self).on_recv_rsp(rsp_str) # 基类的on_recv_rsp方法解包返回了摆盘信息
        print(ret_data, file=f, flush=True)

        return RET_OK, ret_data


if __name__ == '__main__':
    quote_ctx = OpenQuoteContext('127.0.0.1',11122)
    unittest.main()
