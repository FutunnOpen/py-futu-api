# -*- coding:utf-8 -*-
from futu import *
import unittest
import pandas
from futu.testcase.person.winnie.quote.compare_data import *

f1 = open('test_new_protocol.txt','a')
# f2 = open('test_new_protoco2.txt','a')

# class GetBrokerQueue(unittest.TestCase):
#     # 所有用例的公共模块
#     def common_get_broker_queue(self, code, case_name):
#         quote_ctx1.subscribe(code, SubType.BROKER)
#         quote_ctx2.subscribe(code, SubType.BROKER)
#         print(case_name, file=f1, flush=True)
#         print(case_name, file=f2, flush=True)
#         ret_code, ret_data_big1, ret_data_ask1 = quote_ctx1.get_broker_queue(code)
#         print(ret_data_big1, ret_data_ask1, file=f1,flush=True)
#         ret_code, ret_data_big2, ret_data_ask2 = quote_ctx2.get_broker_queue(code)
#         print(ret_data_big2, ret_data_ask2, file=f2, flush=True)
#         print(CompareData().compare(ret_data_big1, ret_data_big2))
#         print(CompareData().compare(ret_data_ask1, ret_data_ask2))
#
#
#     # 获取港股正股的经纪队列
#     def test_get_broker_queue_hk_stock(self):
#         code = 'HK.00700'
#         case_name = sys._getframe().f_code.co_name
#         self.common_get_broker_queue(code, case_name)
#
#
#     # 获取港股已停牌股票的经纪队列
#     def test_get_broker_queue_hk_stopped_stock(self):
#         code = 'HK.01280'
#         case_name = sys._getframe().f_code.co_name
#         self.common_get_broker_queue(code, case_name)
#
#
#     # 获取港股新股股票的经纪队列
#     # def test_get_broker_queue_hk_new_stock(self):
#     #     # 获取新股的API暂无，所以该用例暂时无法实现
#     #     case_name = sys._getframe().f_code.co_name
#     #     self.assertEqual(0, 0)
#
#     # 获取港股涡轮的经纪队列
#     def test_get_broker_queue_hk_warrant(self):
#         code = 'HK.24493'
#         case_name = sys._getframe().f_code.co_name
#         self.common_get_broker_queue(code, case_name)
#         # 无法自动校验
#         # self.assertEqual(ret_code, RET_OK)
#         # print(len(ret_data_ask))
#         # self.assertEqual(len(ret_data_ask), 0)
#         # self.assertEqual(len(ret_data_big), 0)
#
#     # 获取港股指数的经纪队列
#     def test_get_broker_queue_hk_index(self):
#         code = 'HK.800100'
#         case_name = sys._getframe().f_code.co_name
#         self.common_get_broker_queue(code, case_name)
#         # 无法自动校验，仅能保证返回的数据是空
#         # self.assertEqual(len(ret_data_ask), 0)
#         # self.assertEqual(len(ret_data_big), 0)
#         # self.assertEqual(ret_code, RET_OK)
#
#     # 获取港股期货的经纪队列
#     def test_get_broker_queue_hk_future(self):
#         code = 'HK_FUTURE.999010'
#         case_name = sys._getframe().f_code.co_name
#         self.common_get_broker_queue(code, case_name)
#         # 无法自动校验，仅能保证返回的数据是空
#         # self.assertEqual(len(ret_data_ask), 0)
#         # self.assertEqual(len(ret_data_big), 0)
#         # self.assertEqual(ret_code, RET_OK)
#
#     # 获取美股正股的经纪队列
#     def test_get_broker_queue_us_stock(self):
#         code = 'US.AAPL'
#         case_name = sys._getframe().f_code.co_name
#         self.common_get_broker_queue(code, case_name)
#         # 无法自动校验
#         # self.assertEqual(ret_code, RET_OK)
#         # self.assertEqual(len(ret_data_ask), 0)
#         # self.assertEqual(len(ret_data_big), 0)
#
#     # 获取美股指数的经纪队列
#     def test_get_broker_queue_us_idx(self):
#         code = 'US..DJI'
#         case_name = sys._getframe().f_code.co_name
#         self.common_get_broker_queue(code, case_name)
#         # 无法自动校验，仅能保证返回的数据是空
#         # self.assertEqual(ret_code, RET_OK)
#         # self.assertEqual(len(ret_data_ask), 0)
#         # self.assertEqual(len(ret_data_big), 0)
#
#     # 获取美股ETF的经纪队列
#     def test_get_broker_queue_us_etf(self):
#         code = 'US.BRZU'
#         case_name = sys._getframe().f_code.co_name
#         self.common_get_broker_queue(code, case_name)
#         # 无法自动校验
#         # self.assertEqual(ret_code, RET_OK)
#         # self.assertEqual(len(ret_data_ask), 0)
#         # self.assertEqual(len(ret_data_big), 0)
#
#     # 获取A股正股的经纪队列
#     def test_get_broker_queue_ch_stock(self):
#         code = 'SZ.000001'
#         case_name = sys._getframe().f_code.co_name
#         self.common_get_broker_queue(code, case_name)
#         # 无法自动校验
#         # self.assertEqual(ret_code, RET_OK)
#         # self.assertEqual(len(ret_data_ask), 0)
#         # self.assertEqual(len(ret_data_big), 0)
#
#     # 获取A股指数的经纪队列
#     def test_get_broker_queue_ch_idx(self):
#         code = 'SH.000001'
#         case_name = sys._getframe().f_code.co_name
#         self.common_get_broker_queue(code, case_name)
#
#
#     # 获取已停牌股票的经纪队列
#     def test_get_broker_queue_stopped_invalid1(self):
#         code = 'HK.01280'
#         case_name = sys._getframe().f_code.co_name
#         self.common_get_broker_queue(code, case_name)
#         # 无法自动校验,没有数据
#         # self.assertEqual(len(ret_data_ask), 0)
#         # self.assertEqual(len(ret_data_big), 0)
#         # self.assertEqual(ret_code, RET_OK)
#
#     # 获取美股期权的经纪队列
#     def test_get_broker_queue_us_option_invalid2(self):
#         code = 'US.AAPL181116P230000'
#         case_name = sys._getframe().f_code.co_name
#         self.common_get_broker_queue(code, case_name)
#         # 无法自动校验,没有数据
#         # self.assertEqual(ret_code, RET_OK)
#         # self.assertEqual(len(ret_data_ask), 0)
#         # self.assertEqual(len(ret_data_big), 0)
#
#     # 指定code为空
#     def test_get_broker_queue_non_stock_invalid3(self):
#         code = ''
#         case_name = sys._getframe().f_code.co_name
#         self.common_get_broker_queue(code, case_name)
#         # 校验：ERROR. format of  is wrong. (US.AAPL, HK.00700, SZ.000001)
#         # self.assertEqual(ret_data_big, 'ERROR. format of  is wrong. (US.AAPL, HK.00700, SZ.000001)')
#         # self.assertEqual(ret_code, RET_ERROR)
#
#     # 指定code格式不对
#     def test_get_broker_queue_wrong_stock_invalid4(self):
#         code = 'hk.00700'
#         case_name = sys._getframe().f_code.co_name
#         self.common_get_broker_queue(code, case_name)
#         # 校验：ERROR. format of  is wrong. (US.AAPL, HK.00700, SZ.000001)
#         # self.assertEqual(ret_data_ask, 'ERROR. format of hk.00700 is wrong. (US.AAPL, HK.00700, SZ.000001)')
#         # self.assertEqual(ret_code, RET_ERROR)


class AsyncBroker(unittest.TestCase):
    '''
    实时经济队列推送测试类
    '''

    def step_base(self, code_list, casename=sys._getframe().f_code.co_name ):
        '''
        基本测试步骤
        :param code_list:待订阅的股票代码列表
        :return:
        '''
        #打印日志：测试用例名
        print(casename, file=f1, flush=True)
        #设置监听
        handler = BrokerTest()
        quote_ctx1.set_handler(handler)
        #订阅经济队列
        quote_ctx1.subscribe(code_list, SubType.BROKER)

    def test_asyncBroker_hk_stock(self):
        #1、测试点：订阅港股正股实时经济队列
        self.step_base(code_list= ['HK.00700'], casename=sys._getframe().f_code.co_name )

        # 2、校验
        # 不合适在此处校验，需跑完一整天数据后校验

    def test_asyncBroker_hk_wrrant(self):
        # 1、测试点：订阅港股涡轮实时经济队列

        #获取涡轮代码
        codes_warrant = 'HK.27141'
        #执行测试步骤
        self.step_base(code_list=codes_warrant, casename=sys._getframe().f_code.co_name )

        # 2、校验
        # 不合适在此处校验，需跑完一整天数据后校验

    def test_asyncBroker_hk_future_stock(self):
        #1、测试点：订阅港股期货实时经济队列
        self.step_base(code_list= ['HK_FUTURE.999010'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncBroker_hk_idx(self):
        #1、测试点：订阅港股指数实时经济队列
        self.step_base(code_list= ['HK.800000'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncBroker_hk_etf(self):
        #1、测试点：订阅港股基金实时经济队列
        self.step_base(code_list= ['HK.02800'], casename=sys._getframe().f_code.co_name)

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncBroker_hk_bond(self):
        #1、测试点：订阅港股债券实时经济队列
        self.step_base(code_list= ['HK.04231'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncBroker_us_stock(self):
        #1、测试点：订阅美股正股实时经济队列
        self.step_base(code_list= ['US.AAPL'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncBroker_us_idx(self):
        #1、测试点：订阅美股指数实时经济队列
        self.step_base(code_list= ['US..IXIC'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncBroker_us_etf(self):
        #1、测试点：订阅美股指数实时经济队列
        self.step_base(code_list= ['US.YINN'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncBroker_us_drvt(self):
        #1、测试点：订阅美股期权实时经济队列

        #获取期权代码
        codes = []
        drvt_call_ret_code, drvt_call_ret_data = quote_ctx1.get_option_chain(code='US.GOOG',
                                                                                 option_type=OptionType.CALL,
                                                                                 option_cond_type=OptionCondType.ALL)
        drvt_put_ret_code, drvt_put_ret_data = quote_ctx1.get_option_chain(code='US.GOOG',
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

    def test_asyncBroker_cn_stock(self):
        #1、测试点：订阅A股正股实时经济队列
        self.step_base(code_list= ['SZ.000001' ,'SH.601318'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncBroker_cn_idx(self):
        #1、测试点：订阅A股指数实时经济队列
        self.step_base(code_list= ['SH.000001' ,'SZ.399001'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验

    def test_asyncBroker_cn_etf(self):
        #1、测试点：订阅A股指基金实时经济队列
        self.step_base(code_list= ['SH.501053' ,'SZ.164824'], casename=sys._getframe().f_code.co_name )

        #2、校验
        #不合适在此处校验，需跑完一整天数据后校验


class BrokerTest(BrokerHandlerBase):
    # 监听实时经济队列推送
    def on_recv_rsp(self, rsp_str):
        '''
        回调
        :param rsp_str:
        :return:
        '''
        ret_code, err_or_stock_code, data = super(BrokerTest, self).on_recv_rsp(rsp_str) # 基类的on_recv_rsp方法解包返回了经济队列信息
        #打印,记录日志
        print(data, file=f1, flush=True)

        return RET_OK, data


if __name__ == '__main__':
    quote_ctx1 = OpenQuoteContext(host='127.0.0.1', port=11111)
    quote_ctx2 = OpenQuoteContext(host='127.0.0.1', port=11121)
    pandas.set_option('max_columns', 100)
    pandas.set_option('display.width', 1000)
    pandas.set_option('display.max_rows', 1000)
    unittest.main()
    # gbq = AsyncBroker()
    # gbq.test_asyncBroker_hk_future_stock()
    # gbq.test_asyncBroker_hk_stock()
    # gbq.test_asyncBroker_hk_wrrant()
    # gbq.test_asyncBroker_hk_idx()
    # gbq.test_asyncBroker_hk_etf()
    # gbq.test_asyncBroker_hk_bond()
    # gbq.test_asyncBroker_us_stock()
    # gbq.test_asyncBroker_us_idx()
    # gbq.test_asyncBroker_us_etf()
    # gbq.test_asyncBroker_us_drvt()
    # gbq.test_asyncBroker_cn_stock()
    # gbq.test_asyncBroker_cn_idx()
    # gbq.test_asyncBroker_cn_etf()
    # unittest.main()
    # case_path = os.path.join(os.getcwd(),"winnie","quote")
    # discover = unittest.defaultTestLoader.discover(case_path, pattern="test_*.py",top_level_dir=None)
    # print(discover)
    # gbq = GetBrokerQueue()
    # gbq.test_get_broker_queue_hk_stock()
