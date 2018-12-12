from futu import *
import pandas
import sys
import datetime
import unittest
import random
from futu.testcase.person.winnie.quote.compare_data import *

f1 = open('test_rt_ticker1_low.txt','a')
f2 = open('test_rt_ticker2_low.txt','a')

class GetRtTicker(unittest.TestCase):
    '''
    测试类:获取逐笔
    '''

    # 各类型股票获取逐笔的测试步骤和校验
    def step_check_base1(self, casename, code, num = random.randint(0,1000)):
        '''
        各市场各股票获取逐笔并校验是否正确
        :param casename:
        :param code:
        :param num:
        :return:
        '''
        ret_code_sub, ret_data_sub = quote_ctx1.subscribe(code, SubType.TICKER)
        ret_code, ret_data1 = quote_ctx1.get_rt_ticker(code, num)
        print(casename)
        print(num)
        print(num, file=f1, flush=True)
        print(casename,file=f1, flush=True)
        print(ret_data1, file=f1, flush=True)
        print(ret_data1)
        ret_code_sub, ret_data_sub = quote_ctx2.subscribe(code, SubType.TICKER)
        ret_code, ret_data2 = quote_ctx2.get_rt_ticker(code, num)
        print(num, file=f2, flush=True)
        print(casename, file=f2, flush=True)
        print(ret_data2, file=f2, flush=True)
        print(CompareData().compare(ret_data1, ret_data2))
        # print(ret_data)
        '''
        校验点：
        1、请求成功
        2、交易时间len(ret_data)>0
        3、返回的股票与code一致
        4、price >0
        5、volume、turnover>0
        6、sequence无重复项
        '''
        #校验点1、请求成功
        # self.assertEqual(ret_code, RET_OK)
        # #校验点6、sequence无重复项
        # sequence_list = ret_data['sequence'].tolist()
        # sequence_set = set(sequence_list)   #set自动去重
        # self.assertEqual(len(sequence_list), len(sequence_set))

    #港股
    def test_get_rt_ticker_hk_stock(self):
        '''
        测试点：获取某一港股正股的逐笔
        :return:
        '''
        casename = sys._getframe().f_code.co_name
        code = 'HK.01810'
        self.step_check_base1(casename,code)

    def test_get_rt_ticker_hk_wrt(self):
        '''
        测试点：获取某一港股涡轮的逐笔
        :return:
        '''
        casename = sys._getframe().f_code.co_name
        code = 'HK.27187'
        self.step_check_base1(casename,code)

    def test_get_rt_ticker_hk_futrue(self):
        '''
        测试点：获取港股期货的逐笔
        :return:
        '''
        casename = sys._getframe().f_code.co_name
        code = 'HK_FUTURE.999010'
        self.step_check_base1(casename,code)

    #美股
    def test_get_rt_ticker_us_stock(self):
        '''
        测试点：获取某一美股正股的逐笔
        :return:
        '''
        casename = sys._getframe().f_code.co_name
        code = 'US.PDD'
        self.step_check_base1(casename, code)

    def test_get_rt_ticker_us_drvt(self):
        '''
        测试点：获取某一美股期权的逐笔
        :return:
        '''
        casename = sys._getframe().f_code.co_name
        code = 'US.AAPL181221C182500'
        self.step_check_base1(casename,code)

    #A股
    def test_get_rt_ticker_sh_stock(self):
        '''
        测试点：获取某一A股(SH)正股的报价
        :return:
        '''
        casename = sys._getframe().f_code.co_name
        code = 'SH.603131'
        self.step_check_base1(casename, code)

    def test_get_rt_ticker_sz_stock(self):
        '''
        测试点：获取某一A股(SZ)正股的逐笔
        :return:
        '''
        casename = sys._getframe().f_code.co_name
        code = 'SZ.300710'
        self.step_check_base1(casename, code)

    #code是无逐笔的股票，指数无逐笔
    def test_get_rt_ticker_idx(self):
        casename = sys._getframe().f_code.co_name
        code = 'HK.800000'
        num = 100
        ret_code_sub, ret_data_sub = quote_ctx1.subscribe(code, SubType.TICKER)
        ret_code, ret_data1 = quote_ctx1.get_rt_ticker(code, num)
        print(casename)
        print(casename, file=f1, flush=True)
        print(ret_data1, file=f1, flush=True)
        ret_code_sub, ret_data_sub = quote_ctx2.subscribe(code, SubType.TICKER)
        ret_code, ret_data2 = quote_ctx2.get_rt_ticker(code, num)
        print(casename, file=f2, flush=True)
        print(ret_data2, file=f2, flush=True)
        print(CompareData().compare(ret_data1, ret_data2))
        #校验


    #入参错误步骤和校验
    def step_check_base2(self, casename, code, num = random.randint(0,1000)):
        # 执行步骤
        ret_code_sub, ret_data_sub = quote_ctx1.subscribe(code, SubType.TICKER)
        ret_code, ret_data1 = quote_ctx1.get_rt_ticker(code,num)
        print(casename, file=f1, flush=True)
        print(ret_data1, file=f1, flush=True)
        ret_code_sub, ret_data_sub = quote_ctx2.subscribe(code, SubType.TICKER)
        ret_code, ret_data2 = quote_ctx2.get_rt_ticker(code, num)
        print(casename, file=f2, flush=True)
        print(ret_data2, file=f2, flush=True)
        print(CompareData().compare(ret_data1, ret_data2))
        # 校验
        # self.assertEqual(ret_code, RET_ERROR)

    #code入参错误
    def test_get_rt_ticker_err_code(self):
        '''
        测试点：code入参错误
        :return:
        '''
        casename = sys._getframe().f_code.co_name
        code = ['HK.00700']
        self.step_check_base2(casename, code)

    # num入参错误
    def test_get_rt_ticker_err_num(self):
        '''
        测试点：num入参错误
        :return:
        '''
        casename = sys._getframe().f_code.co_name
        code = 'HK.00434'
        num = -2
        self.step_check_base2(casename,code,num)

    #code正确，但未执行订阅
    def test_get_rt_ticker_err_no_sub(self):
        '''
        测试点：未订阅
        :return:
        '''
        casename = sys._getframe().f_code.co_name
        code = 'US.CI'
        #执行步骤
        ret_code, ret_data = quote_ctx1.get_rt_ticker(code)
        print(ret_data, file=f1, flush=True)
        ret_code, ret_data = quote_ctx2.get_rt_ticker(code)
        print(ret_data, file=f2, flush=True)
        #校验
        self.assertEqual(ret_code,RET_ERROR)




if __name__ == '__main__':
    # SysConfig.set_all_thread_daemon(True)
    # 新订阅协议
    quote_ctx1 = OpenQuoteContext('127.0.0.1',11111)
    # 旧协议
    quote_ctx2 = OpenQuoteContext('127.0.0.1', 11111)
    pandas.set_option('max_columns', 100)
    pandas.set_option('display.width', 1000)
    pandas.set_option('display.max_rows', 1000)
    grt = GetRtTicker()
    grt.test_get_rt_ticker_us_drvt()
    # while True:
    # unittest.main()

    # 高频接口
    # 设置监听
    # handler = TickerTest()
    # quote_ctx1.set_handler(handler)
    # quote_ctx2.set_handler(handler)
    # code_list=['HK.00700','HK.28070','HK_FUTURE.999010','HK.800000','HK.02800','HK.04231','US.AAPL','US..IXIC','US.YINN','US.DIS181207P113000', 'US.DIS181207C121000',
    #            'SZ.000001', 'SH.601318','SH.000001' ,'SZ.399001','SH.501053' ,'SZ.164824']
    # # 订阅逐笔
    # quote_ctx1.subscribe(code_list, SubType.TICKER)
    # quote_ctx2.subscribe(code_list, SubType.TICKER)



# f = open('get_rt_triker2.txt','a')

# class TickerTest(TickerHandlerBase):
#     def on_recv_rsp(self, rsp_str):
#         ret_code, data = super(TickerTest, self).on_recv_rsp(rsp_str)
#         if ret_code != RET_OK:
#             print("TickerTest: error, msg: %s" % data)
#             return RET_ERROR, data
#         # print(datetime.datetime.now().strftime('%c'), file=f, flush=True)
#         # print(data, file=f, flush=True)
#         print(data)
#         return RET_OK, data
#
#
# class SysNotifyTest(SysNotifyHandlerBase):
#     def on_recv_rsp(self, rsp_pb):
#         ret_code, content = super(SysNotifyTest, self).on_recv_rsp(rsp_pb)
#         notify_type, sub_type, msg = content
#         if ret_code != RET_OK:
#             logger.debug("SysNotifyTest: error, msg: %s" % msg)
#             return RET_ERROR, content
#
#         now = datetime.datetime.now()
#         now.strftime('%c')
#         # print(now, file=f, flush=True)
#         # print(msg, file=f, flush=True)
#         print(now)
#         print(msg)
#         return ret_code, content
#
#
# if __name__ == '__main__':
#     # output = sys.stdout
#     # outputfile = open('get_rt_triker1.txt', 'a')
#     # sys.stdout = outputfile
#     pandas.set_option('max_columns', 100)
#     pandas.set_option('display.width', 1000)
#     quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11112)
#     ret_code, ret_data = quote_ctx.get_stock_basicinfo(Market.HK, SecurityType.STOCK)
#     code_list = list(ret_data['code'])
#     del code_list[800:]  # 截取股票
#     quote_ctx.set_handler(TickerTest())
#     quote_ctx.set_handler(SysNotifyTest())
#     print(quote_ctx.subscribe(code_list, SubType.TICKER))  # SH.600119
#     quote_ctx.start()






