# import time
from futuquant import *
import pandas
import sys
import unittest

f1 = open('test_stock_quote1.txt','a')
f2 = open('test_stock_quote2.txt','a')

class GetStockQuote(unittest.TestCase):
    '''
    测试类:获取报价
    '''

    # 各市场各股票类型的报价测试步骤和校验
    def step_check_base1(self, casename, code_list):
        '''
        测试点：各市场各股票类型的报价
        :param casename:
        :param code_list:
        :return:
        '''
        # 执行步骤
        ret_code_sub, ret_data_sub = quote_ctx1.subscribe(code_list, SubType.QUOTE)#这里没有对应的反订阅。测试类退出前tearDownClass会stop、close行情上下文，此时会自动反订阅。
                                                                                        # 原因是反订阅前得等待60s，如果每个用例都等待60s自动化时间将大大加长，效率低。
        ret_code, ret_data = quote_ctx1.get_stock_quote(code_list)
        print(casename, file=f1,flush=True)
        print(ret_data, file=f1,flush=True)

        ret_code_sub, ret_data_sub = quote_ctx2.subscribe(code_list, SubType.QUOTE)  # 这里没有对应的反订阅。测试类退出前tearDownClass会stop、close行情上下文，此时会自动反订阅。
        # 原因是反订阅前得等待60s，如果每个用例都等待60s自动化时间将大大加长，效率低。
        ret_code, ret_data = quote_ctx2.get_stock_quote(code_list)
        print(casename, file=f2, flush=True)
        print(ret_data, file=f2, flush=True)
        '''校验点：
        1、请求成功，且数据不为空。
        2、返回的股票 == code_list
        3、价格相关值一定大于0，即last_price，open_price，high_price，low_price，prev_close_price，price_spread
        4、若当天是交易日且开盘时间范围内，data_time与当前时间戳相差不超过3秒。
        5、volume成交量和turnover成交额要不同时为0，要不同时大于0.
        '''
        # 校验点1、请求成功，且数据不为空
        # self.assertEqual(ret_code, RET_OK)
        # self.assertTrue(len(ret_data) > 0)
        #校验点2、返回的股票 == code_list
        # ret_code_list = ret_data['code'].tolist()
        # if type(code_list)!= type([]):
        #     code_list = [code_list]
        # self.assertEqual(ret_code_list,code_list)
        #校验点3、价格相关值一定大于0
        # price_key = ['last_price','open_price','high_price','low_price','prev_close_price','price_spread']
        # for key in price_key:
        #     price_list = ret_data[key]
        #     for index in range(len(ret_data)):
        #         self.assertTrue(price_list[index] > 0, 'Error: index = %d' % index)

    # 港股
    def test_get_stock_quote_hk_stock(self):
        '''
        测试点：获取某一港股正股的报价
        :return:
        '''
        casename = sys._getframe().f_code.co_name
        code = 'HK.00434'
        self.step_check_base1(casename,code)

    def test_get_stock_quote_hk_wrt(self):
        '''
        测试点：获取某一港股涡轮的报价
        :return:
        '''
        casename = sys._getframe().f_code.co_name
        code = 'HK.28552'
        self.step_check_base1(casename,code)

    def test_get_stock_quote_hk_idx(self):
        '''
        测试点：获取港股指数的报价
        :return:
        '''
        casename = sys._getframe().f_code.co_name
        code = 'HK.800100'
        self.step_check_base1(casename,code)

    def test_get_stock_quote_hk_futrue(self):
        '''
        测试点：获取港股期货的报价
        :return:
        '''
        casename = sys._getframe().f_code.co_name
        code = 'HK_FUTURE.999010'
        self.step_check_base1(casename,code)

    #美股
    def test_get_stock_quote_us_stock(self):
        '''
        测试点：获取某一美股正股的报价
        :return:
        '''
        casename = sys._getframe().f_code.co_name
        code = 'US.JD'
        self.step_check_base1(casename, code)

    def test_get_stock_quote_us_drvt(self):
        '''
        测试点：获取某一美股期权的报价
        :return:
        '''
        casename = sys._getframe().f_code.co_name
        code = 'US.DIS181123P110000'
        self.step_check_base1(casename,code)

    def test_get_stock_quote_us_idx(self):
        '''
        测试点：获取美股指数的报价
        :return:
        '''
        casename = sys._getframe().f_code.co_name
        code = 'US..IXIC'
        self.step_check_base1(casename,code)

    #A股
    def test_get_stock_quote_sh_stock(self):
        '''
        测试点：获取某一A股(SH)正股的报价
        :return:
        '''
        casename = sys._getframe().f_code.co_name
        code = 'SH.603131'
        self.step_check_base1(casename, code)

    def test_get_stock_quote_sz_stock(self):
        '''
        测试点：获取某一A股(SZ)正股的报价
        :return:
        '''
        casename = sys._getframe().f_code.co_name
        code = 'SZ.300710'
        self.step_check_base1(casename, code)

    def test_get_stock_quote_cn_idx(self):
        '''
        测试点：获取A股指数的报价
        :return:
        '''
        casename = sys._getframe().f_code.co_name
        code = 'SZ.399001'
        self.step_check_base1(casename, code)

    #code_list为多只股票时

    def test_get_stock_quote_hk_codes(self):
        '''
        测试点：code_list为多只港股正股
        :return:
        '''
        casename = sys._getframe().f_code.co_name
        code_list = ['HK.00700','HK.00434','HK.00630','HK.01810']
        self.step_check_base1(casename, code_list)

    def test_get_stock_quote_markets(self):
        '''
        测试点：code_list为3大市场各类型股票的组合
        :return:
        '''
        casename = sys._getframe().f_code.co_name
        code_list = ['HK.00700','US.VIPS','SH.603655','SZ.300545','HK.11364','HK.800000','HK_FUTURE.999010','US.DIS181123P110000']
        self.step_check_base1(casename, code_list)

    # code_list入参错误(订阅失败)
    def test_get_stock_quote_err_cod_list(self):
        '''
        测试点：code_list入参错误
        :return:
        '''
        casename = sys._getframe().f_code.co_name
        code_list = ['HK.00700','sh']
        # 执行步骤
        ret_code_sub, ret_data_sub = quote_ctx1.subscribe(code_list, SubType.QUOTE)
        ret_code, ret_data = quote_ctx1.get_stock_quote(code_list)
        print(casename, file=f1, flush=True)
        print(ret_data, file=f1, flush=True)

        ret_code_sub, ret_data_sub = quote_ctx2.subscribe(code_list, SubType.QUOTE)
        ret_code, ret_data = quote_ctx2.get_stock_quote(code_list)
        print(casename, file=f2, flush=True)
        print(ret_data, file=f2, flush=True)
        #校验

    #code_list正确，但未执行订阅
    def test_get_stock_quote_err_no_sub(self):
        '''
        测试点：未订阅
        :return:
        '''
        casename = sys._getframe().f_code.co_name
        code_list = 'HK.01810'
        #执行步骤
        ret_code, ret_data = quote_ctx1.get_stock_quote(code_list)
        print(casename, file=f1,flush=True)
        print(ret_data, file=f1,flush=True)

        ret_code, ret_data = quote_ctx2.get_stock_quote(code_list)
        print(casename, file=f2, flush=True)
        print(ret_data, file=f2, flush=True)
        #校验


    # 订阅板块和正股，反订阅板块正股是否正常
    def test_get_stock_quote_bk_stock_unsubscribe_bk(self):
        casename = sys._getframe().f_code.co_name
        code_list = ['HK.00700','SH.BK0001']
        quote_ctx1.subscribe(code_list,SubType.QUOTE)
        ret_code, ret_data = quote_ctx1.get_stock_quote(code_list)
        print(casename, file=f1,flush=True)
        print(ret_data, file=f1,flush=True)
        print(ret_data)
        # quote_ctx2.subscribe(code_list, SubType.QUOTE)
        # ret_code, ret_data = quote_ctx2.get_stock_quote(code_list)
        # print(casename, file=f2, flush=True)
        # print(ret_data, file=f2, flush=True)
        time.sleep(60)
        quote_ctx1.unsubscribe('SH.BK0001',SubType.QUOTE)
        ret_code, ret_data = quote_ctx1.get_stock_quote('HK.00700')
        print(ret_data)
        print(ret_data, file=f1,flush=True)
        # quote_ctx2.unsubscribe('SH.BK0001', SubType.QUOTE)
        # ret_code, ret_data = quote_ctx2.get_stock_quote('HK.00700')
        # print(ret_data, file=f2, flush=True)

    # 订阅板块和正股，反订阅板块正股是否正常
    def test_get_stock_quote_bk_stock_unsubscribe_stock(self):
        casename = sys._getframe().f_code.co_name
        code_list = ['HK.00700','SH.BK0001']
        quote_ctx1.subscribe(code_list,SubType.QUOTE)
        ret_code, ret_data = quote_ctx1.get_stock_quote(code_list)
        print(casename, file=f1,flush=True)
        print(ret_data, file=f1,flush=True)
        quote_ctx2.subscribe(code_list, SubType.QUOTE)
        ret_code, ret_data = quote_ctx2.get_stock_quote(code_list)
        print(casename, file=f2, flush=True)
        print(ret_data, file=f2, flush=True)
        time.sleep(60)
        quote_ctx1.unsubscribe('HK.00700',SubType.QUOTE)
        ret_code, ret_data = quote_ctx1.get_stock_quote('SH.BK0001')
        print(ret_data, file=f1,flush=True)
        quote_ctx2.unsubscribe('HK.00700', SubType.QUOTE)
        ret_code, ret_data = quote_ctx2.get_stock_quote('SH.BK0001')
        print(ret_data, file=f2, flush=True)


# class AsyncStockQuote(unittest.TestCase):
#     '''
#     实时报价推送测试类
#     '''
#
#     def step_base(self, code_list, casename=sys._getframe().f_code.co_name ):
#         '''
#         基本测试步骤
#         :param code_list:待订阅的股票代码列表
#         :return:
#         '''
#         #打印日志：测试用例名
#         print(casename, file=f1, flush=True)
#         #设置监听
#         handler = StockQuoteTest()
#         quote_ctx1.set_handler(handler)
#         #订阅报价
#         quote_ctx1.subscribe(code_list, SubType.QUOTE)
#
#     def test_asyncStockQuote_hk_stock(self):
#         #1、测试点：订阅港股正股实时报价
#         self.step_base(code_list= ['HK.00700'], casename=sys._getframe().f_code.co_name )
#
#         #2、校验
#         #不合适在此处校验，需跑完一整天数据后校验
#
#     def test_asyncStockQuote_hk_wrrant(self):
#         # 1、测试点：订阅港股涡轮实时报价
#
#         #获取认沽、认购、牛证、熊证代码
#         codes_warrant = 'HK.13322'
#         #执行测试步骤
#         self.step_base(code_list=codes_warrant, casename=sys._getframe().f_code.co_name )
#
#         # 2、校验
#         # 不合适在此处校验，需跑完一整天数据后校验
#
#     def test_asyncStockQuote_hk_future_stock(self):
#         #1、测试点：订阅港股期货实时报价
#         self.step_base(code_list= ['HK_FUTURE.999010'], casename=sys._getframe().f_code.co_name )
#
#         #2、校验
#         #不合适在此处校验，需跑完一整天数据后校验
#
#     def test_asyncStockQuote_hk_idx(self):
#         #1、测试点：订阅港股指数实时报价
#         self.step_base(code_list= ['HK.800000'], casename=sys._getframe().f_code.co_name )
#
#         #2、校验
#         #不合适在此处校验，需跑完一整天数据后校验
#
#     def test_asyncStockQuote_hk_etf(self):
#         #1、测试点：订阅港股基金实时报价
#         self.step_base(code_list= ['HK.02800'], casename=sys._getframe().f_code.co_name )
#
#         #2、校验
#         #不合适在此处校验，需跑完一整天数据后校验
#
#     def test_asyncStockQuote_hk_bond(self):
#         #1、测试点：订阅港股债券实时报价
#         self.step_base(code_list= ['HK.04231'], casename=sys._getframe().f_code.co_name )
#
#         #2、校验
#         #不合适在此处校验，需跑完一整天数据后校验
#
#     def test_asyncStockQuote_us_stock(self):
#         #1、测试点：订阅美股正股实时报价
#         self.step_base(code_list= ['US.AAPL'], casename=sys._getframe().f_code.co_name )
#
#         #2、校验
#         #不合适在此处校验，需跑完一整天数据后校验
#
#     def test_asyncStockQuote_us_idx(self):
#         #1、测试点：订阅美股指数实时报价
#         self.step_base(code_list= ['US..IXIC'], casename=sys._getframe().f_code.co_name )
#
#         #2、校验
#         #不合适在此处校验，需跑完一整天数据后校验
#
#     def test_asyncStockQuote_us_etf(self):
#         #1、测试点：订阅美股指数实时报价
#         self.step_base(code_list= ['US.YINN'], casename=sys._getframe().f_code.co_name )
#
#         #2、校验
#         #不合适在此处校验，需跑完一整天数据后校验
#
#     def test_asyncStockQuote_us_drvt(self):
#         #1、测试点：订阅美股期权实时报价
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
#     def test_asyncStockQuote_cn_stock(self):
#         #1、测试点：订阅A股正股实时报价
#         self.step_base(code_list= ['SZ.000001' ,'SH.601318'], casename=sys._getframe().f_code.co_name )
#
#         #2、校验
#         #不合适在此处校验，需跑完一整天数据后校验
#
#     def test_asyncStockQuote_cn_idx(self):
#         #1、测试点：订阅A股指数实时报价
#         self.step_base(code_list= ['SH.000001' ,'SZ.399001'], casename=sys._getframe().f_code.co_name )
#
#         #2、校验
#         #不合适在此处校验，需跑完一整天数据后校验
#
#     def test_asyncStockQuote_cn_etf(self):
#         #1、测试点：订阅A股指基金实时报价
#         self.step_base(code_list= ['SH.501053' ,'SZ.164824'], casename=sys._getframe().f_code.co_name )
#
#         #2、校验
#         #不合适在此处校验，需跑完一整天数据后校验
#
#
# class StockQuoteTest(StockQuoteHandlerBase):
#     def on_recv_rsp(self, rsp_str):
#         '''
#         回调
#         :param rsp_str:
#         :return:
#         '''
#         ret_code, data = super(StockQuoteTest,self).on_recv_rsp(rsp_str) # 基类的on_recv_rsp方法解包返回了报价信息
#
#         print(data, file=f1,flush=True)
#
#         return RET_OK, data


if __name__ == '__main__':
    quote_ctx1 = OpenQuoteContext('127.0.0.1', 11111)
    # quote_ctx2 = OpenQuoteContext('127.0.0.1',11121)
    pandas.set_option('max_columns', 100)
    pandas.set_option('display.width', 1000)
    # tmp = GetStockQuote()
    # tmp.test_get_stock_quote_bk_stock_unsubscribe_bk()
    print(quote_ctx1.subscribe('HK.00700', SubType.ORDER_BOOK))
    print(quote_ctx1.get_order_book('HK.00700'))
    # unittest.main()
    # tq = TestQuote()
    # tq.test1()



