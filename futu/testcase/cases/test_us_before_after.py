# -*- coding:utf-8 -*-
from futu import *
from futu.testcase.winnieUtils.logs import MyLogger
import pandas
import time
import random

pandas.set_option('max_columns', 100)
pandas.set_option('max_rows', 5000)
pandas.set_option('display.width', 1200)

host = "127.0.0.1"
port = 11111


class TickerTest(TickerHandlerBase):
    '''获取逐笔 get_rt_ticker 和 TickerHandlerBase'''

    def on_recv_rsp(self, rsp_pb):
        ret_code, ret_data = super(TickerTest, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            print("TickerTest: error, msg: %s" % ret_data)
            return RET_ERROR, ret_data
        print(ret_data)
        # print(ret_data)
        return RET_OK, ret_data

class RTDataTest1(RTDataHandlerBase):
    global __logger

    def set_logger(self, logger):
        '''
        设置记录日志
        :param logger: 记录日志实例
        :return:
        '''
        global __logger
        __logger = logger
    def on_recv_rsp(self, rsp_str):
        global __logger
        ret_code, data = super(RTDataTest1, self).on_recv_rsp(rsp_str)
        if ret_code != RET_OK:
            print("RTDataTest: error, msg: %s" % data)
            return RET_ERROR, data
        __logger.info(data) # RTDataTest自己的处理逻辑
        return RET_OK, data

class CurKlineTest1(CurKlineHandlerBase):
    global __logger
    def set_logger(self, logger):
        '''
        设置记录日志
        :param logger: 记录日志实例
        :return:
        '''
        global __logger
        __logger = logger
    def on_recv_rsp(self, rsp_str):
        global __logger
        ret_code, data = super(CurKlineTest1,self).on_recv_rsp(rsp_str)
        if ret_code != RET_OK:
            print("CurKlineTest: error, msg: %s" % data)
            return RET_ERROR, data
        __logger.info(data) # CurKlineTest自己的处理逻辑
        return RET_OK, data

class RTDataTest2(RTDataHandlerBase):
    global __logger

    def set_logger(self, logger):
        '''
        设置记录日志
        :param logger: 记录日志实例
        :return:
        '''
        global __logger
        __logger = logger
    def on_recv_rsp(self, rsp_str):
        global __logger
        ret_code, data = super(RTDataTest2, self).on_recv_rsp(rsp_str)
        if ret_code != RET_OK:
            print("RTDataTest: error, msg: %s" % data)
            return RET_ERROR, data
        __logger.info(data) # RTDataTest自己的处理逻辑
        return RET_OK, data

class CurKlineTest2(CurKlineHandlerBase):
    global __logger
    def set_logger(self, logger):
        '''
        设置记录日志
        :param logger: 记录日志实例
        :return:
        '''
        global __logger
        __logger = logger

    def on_recv_rsp(self, rsp_str):
        global __logger
        ret_code, data = super(CurKlineTest2,self).on_recv_rsp(rsp_str)
        if ret_code != RET_OK:
            print("CurKlineTest: error, msg: %s" % data)
            return RET_ERROR, data
        __logger.info(data) # CurKlineTest自己的处理逻辑
        return RET_OK, data


class TestUsBeforeAfter():
    """
    美股盘前盘后数据
    """
    log_kline = MyLogger().geLogger("kline1.txt")
    log_rt_data = MyLogger().geLogger("rtdata1.txt")
    log_ticker = MyLogger().geLogger("ticker1.txt")
    # log_push_rt_data_no = MyLogger().geLogger("push_rt_data_no1.txt")
    # log_push_rt_data = MyLogger().geLogger("push_rt_data1.txt")
    # log_push_kline_no = MyLogger().geLogger("log_push_kline_no1.txt")
    # log_push_kline = MyLogger().geLogger("log_push_kline1.txt")
    def test_get_ticker_rtdata_kline(self):
        """
        测试逐笔、分时、k线
        :return:
        """
        dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.log_rt_data.info("现在时间是：{}".format(dt))
        self.log_kline.info("现在时间是：{}".format(dt))
        subtype = [SubType.RT_DATA,SubType.K_1M,SubType.K_15M,SubType.K_DAY,SubType.TICKER]
        quote_ctx = OpenQuoteContext(host, port)
        code_list = ["HK.00700","US.AAPL","SZ.000001"]
        # 不订阅盘前盘后
        ret_code, ret_data = quote_ctx.subscribe(code_list,subtype,extended_time=False)
        if ret_code == RET_ERROR:
            print(ret_data)
            return
        for c in code_list:
            self.log_rt_data.info("不订阅盘前盘后,分时数据：\n{}".format(quote_ctx.get_rt_data(c)[1]))
            self.log_kline.info("不订阅盘前盘后,1分K线数据：\n{}".format(quote_ctx.get_cur_kline(c, 10, ktype=SubType.K_1M)[1]))
            self.log_kline.info("不订阅盘前盘后,15分K线数据：\n{}".format(quote_ctx.get_cur_kline(c, 100, ktype=SubType.K_15M)[1]))
            self.log_kline.info("不订阅盘前盘后,日K线数据：\n{}".format(quote_ctx.get_cur_kline(c, 200, ktype=SubType.K_DAY)[1]))
            # self.log_ticker.info("不订阅盘前盘后,逐笔数据：\n{}".format(quote_ctx.get_rt_ticker(c, 1000)[1]))

        # 订阅盘前盘后
        ret_code, ret_data = quote_ctx.subscribe(code_list, subtype,extended_time=True)
        if ret_code == RET_ERROR:
            print(ret_data)
            return
        for c in code_list:
            self.log_rt_data.info("订阅盘前盘后,分时数据：\n{}".format(quote_ctx.get_rt_data(c)[1]))
            self.log_kline.info("订阅盘前盘后,1分K线数据：\n{}".format(quote_ctx.get_cur_kline(c, 10, ktype=SubType.K_1M)[1]))
            self.log_kline.info("订阅盘前盘后,15分K线数据：\n{}".format(quote_ctx.get_cur_kline(c, 100, ktype=SubType.K_15M)[1]))
            self.log_kline.info("订阅盘前盘后,日K线数据：\n{}".format(quote_ctx.get_cur_kline(c, 200, ktype=SubType.K_DAY)[1]))
            # self.log_ticker.info("订阅盘前盘后,逐笔数据：\n{}".format(quote_ctx.get_rt_ticker(c, 1000)[1]))

    def test_push_ticker_data_kline(self):
        """
        测试推送逐笔、分时、K线
        :return:
        """
        subtype = [SubType.RT_DATA, SubType.K_1M, SubType.K_15M, SubType.K_DAY, SubType.TICKER]
        quote_ctx1 = OpenQuoteContext(host, port)
        quote_ctx2 = OpenQuoteContext(host, port)
        code_list = ["HK.00700", "US.PDD", "US.AAPL", "SZ.000001"]
        handler1 = RTDataTest1()
        handler1.set_logger(self.log_push_rt_data)
        quote_ctx1.set_handler(handler1)
        handler2 = CurKlineTest1()
        handler2.set_logger(self.log_push_kline)
        quote_ctx1.set_handler(handler2)
        quote_ctx1.subscribe(code_list, subtype,extended_time=True)
        handler3 = RTDataTest2()
        handler3.set_logger(self.log_push_rt_data_no)
        quote_ctx2.set_handler(handler3)
        handler4 = CurKlineTest2()
        handler4.set_logger(self.log_push_kline_no)
        quote_ctx2.set_handler(handler4)
        quote_ctx2.subscribe(code_list, subtype, extended_time=False)


if __name__ == '__main__':
    tba = TestUsBeforeAfter()
    tba.test_get_ticker_rtdata_kline()
    # tba.test_push_ticker_data_kline()
    # while 1:
    #     dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #     if dt == "2020-09-18 00:00:00":
    #         tba.test_get_ticker_rtdata_kline()
    #
    #     if dt == "2020-09-18 07:00:00":
    #         tba.test_get_ticker_rtdata_kline()
    #
    #     if dt == "2020-09-18 10:00:00":
    #         tba.test_get_ticker_rtdata_kline()



