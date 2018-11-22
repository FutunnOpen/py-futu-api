# -*- coding:utf-8 -*-
from futu import *
import unittest
import time
import datetime
import logging
import pandas


# 以下用例请求太频繁会出现请求频繁错误
class RequestHistoryKline(unittest.TestCase):

    def common_request_history_kline_process(self, case_name, code, start, end, ktype, autype=AuType.QFQ, fields=KL_FIELD.ALL):
        '''
        请求历史K线数据-执行过程
        :param case_name:
        :param code:
        :param start:
        :param end:
        :param ktype:
        :return:
        '''
        logger.info('【testcase】' + case_name)
        page_req_key = None
        ret,data,page_req_key = quote_ctx.request_history_kline(code, start,end,ktype,autype,fields,page_req_key)
        logger.info(data)
        return ret,data

    def common_request_history_kline_check_success(self, code, ret, data):
        '''
        校验点-执行成功的情况
        :param code:
        :param ret:
        :param data:
        :return:
        '''
        '''
        校验点：
        0、返回的状态码：RET_OK
        1、返回的数据code列和code一样
        '''
        self.assertEqual(ret, RET_OK)
        # data数据一定不为空
        self.assertEqual(len(data)>0, True)
        code_list = list(set(data['code']))
        # codes = set(code_list)
        self.assertEqual(len(code_list), 1)
        get_code = code_list[0]
        self.assertEqual(get_code, code)

    # 获取港股正股昨日1分k数据
    def test_request_history_kline_1min_yesterday(self):
        case_name = sys._getframe().f_code.co_name
        code = 'HK.00700'
        start = '2018-11-12'
        end = start
        ktype = KLType.K_1M
        ret, data = self.common_request_history_kline_process(case_name, code, start, end, ktype)
        # 校验：
        self.common_request_history_kline_check_success(code, ret, data)

    # 获取港股涡轮昨日5分k数据
    def test_request_history_kline_5min_yesterday(self):
        case_name = sys._getframe().f_code.co_name
        code = 'HK.13320'
        start = '2018-11-12'
        end = start
        ktype = KLType.K_5M
        ret, data = self.common_request_history_kline_process(case_name, code, start, end, ktype)
        # 校验：如果是交易日，则有66条数据，code显示都是'HK.22803',time的前半部分都是start,end；否则0条数据
        self.assertEqual(len(data), 66)
        self.common_request_history_kline_check_success(code, ret, data)

    # 获取港股牛熊近1年3分k数据
    # def test_request_history_kline_15min_1year(self):
    #     case_name = sys._getframe().f_code.co_name
    #     code = 'HK.66950'
    #     end = '2018-11-12'
    #     start = '2017-11-12'
    #     ktype = KLType.K_3M
    #     ret, data = self.common_request_history_kline_process(case_name, code, start, end, ktype)
    #     # 校验：数据大于5000条，code显示都是'HK.69426'
    #     self.common_request_history_kline_check_success(code, ret, data)

    # 获取港股正股近1年15分k数据
    def test_request_history_kline_15min_1years(self):
        case_name = sys._getframe().f_code.co_name
        code = 'HK.01810'
        end = '2018-11-12'
        start = '2017-11-12'
        ktype = KLType.K_15M
        ret, data = self.common_request_history_kline_process(case_name, code, start, end, ktype)
        # 校验：
        self.common_request_history_kline_check_success(code, ret, data)

    # 获取港股指数近1年30分k数据
    def test_request_history_kline_30min_1years(self):
        case_name = sys._getframe().f_code.co_name
        code = 'HK.800000'
        end = '2018-11-12'
        start = '2017-11-12'
        ktype = KLType.K_30M
        ret, data = self.common_request_history_kline_process(case_name, code, start, end, ktype)
        # 校验：
        self.common_request_history_kline_check_success(code, ret, data)

    # 获取港股期货60分k数据
    def test_request_history_kline_60min_all(self):
        case_name = sys._getframe().f_code.co_name
        code = 'HK_FUTURE.999010'
        end = '2018-11-12'
        start = '2018-10-12'
        ktype = KLType.K_60M
        autype = AuType.QFQ
        fields = [KL_FIELD.DATE_TIME, KL_FIELD.OPEN, KL_FIELD.CLOSE, KL_FIELD.LAST_CLOSE]
        ret, data = self.common_request_history_kline_process(case_name, code, start, end, ktype, autype, fields)
        # 校验：
        self.common_request_history_kline_check_success(code, ret, data)

    # 获取港股板块当天日k数据
    def test_request_history_kline_day_today(self):
        case_name = sys._getframe().f_code.co_name
        code = 'HK.BK1148'
        start = datetime.now()
        end = start
        ktype = KLType.K_DAY
        ret, data = self.common_request_history_kline_process(case_name, code, start, end, ktype)
        # 校验：当下时间，如果是盘中，有一条数据；盘前没有数据
        self.assertEqual(ret, RET_OK)
        # state = self.getMarketOfState('market_hk')
        # if state is not MarketState.PRE_MARKET_BEGIN:
        #     self.assertEqual(len(data), 1)

    # 美股正股获取昨日日k
    def test_request_history_kline_us_stock_yesterday(self):
        case_name = sys._getframe().f_code.co_name
        code = 'US.VIPS'
        start = '2018-11-12'
        end = start
        ktype = KLType.K_DAY
        ret, data = self.common_request_history_kline_process(case_name, code, start, end, ktype)
        # print(start, end)
        # print(len(data))
        # 校验：有一条数据
        self.common_request_history_kline_check_success(code, ret, data)

    # 美股指数获取近1年日k
    def test_request_history_kline_us_idx_1year(self):
        case_name = sys._getframe().f_code.co_name
        code = 'US..DJI'
        end = '2018-11-12'
        start = '2017-11-12'
        ktype = KLType.K_DAY
        ret, data = self.common_request_history_kline_process(case_name, code, start, end, ktype)
        # 校验：252条数据，code部分是'US..DJI'
        self.common_request_history_kline_check_success(code, ret, data)

    # 美股指数获取近1年季k
    # def test_request_history_kline_us_idx_1year_season(self):
    #     case_name = sys._getframe().f_code.co_name
    #     code = 'US..DJI'
    #     end = '2018-11-12'
    #     start = '2017-11-12'
    #     ktype = KLType.K_SEASON
    #     ret, data = self.common_request_history_kline_process(case_name, code, start, end, ktype)
    #     # 校验：252条数据，code部分是'US..DJI'
    #     self.common_request_history_kline_check_success(code, ret, data)

    # 美股ETF获取近1年日k
    def test_request_history_kline_us_etf_1years(self):
        case_name = sys._getframe().f_code.co_name
        code = 'US.DGP'
        end = '2018-11-12'
        start = '2017-11-12'
        ktype = KLType.K_DAY
        autype = AuType.HFQ
        ret, data = self.common_request_history_kline_process(case_name, code, start, end, ktype, autype)
        # 校验：252条数据，code部分是'US.DGP'
        self.common_request_history_kline_check_success(code, ret, data)

    # A股正股获取近1年日k
    def test_request_history_kline_ch_stock_2years(self):
        case_name = sys._getframe().f_code.co_name
        code = 'SH.600837'
        end = '2018-11-12'
        start = '2017-11-12'
        ktype = KLType.K_DAY
        ret, data = self.common_request_history_kline_process(case_name, code, start, end, ktype)
        # 校验：第一条数据的日期和当今在10年，code部分是'SZ.000001'
        self.common_request_history_kline_check_success(code, ret, data)

    # A股指数获取1年日k
    def test_request_history_kline_ch_idx_allyears(self):
        case_name = sys._getframe().f_code.co_name
        code = 'SH.000001'
        end = '2018-11-12'
        start = '2017-11-12'
        ktype = KLType.K_DAY
        ret, data = self.common_request_history_kline_process(case_name, code, start, end, ktype)
        # 校验：第一条数据的日期和当今在10年，code部分是'SH.000001'
        self.common_request_history_kline_check_success(code, ret, data)

    # 获取港股正股今日周k数据
    def test_request_history_kline_hk_stock_week_today(self):
        case_name = sys._getframe().f_code.co_name
        code = 'HK.00434'
        start = '2018-11-14'
        end = start
        ktype = KLType.K_WEEK
        ret, data = self.common_request_history_kline_process(case_name, code, start, end, ktype)
        # 校验：如果当日是周1，会有一条数据，否则没有数据


    # 获取港股涡轮昨日月k数据
    def test_request_history_kline_hk_warrant_month_yesterday(self):
        time.sleep(30)
        case_name = sys._getframe().f_code.co_name
        code = 'HK.14452'
        start = '2018-11-15'
        end = start
        ktype = KLType.K_MON
        ret, data = self.common_request_history_kline_process(case_name, code, start, end, ktype)
        # 校验：如果当日是每月1号，会有一条数据，否则没有数据


    # 获取港股牛熊近1年周k数据
    def test_request_history_kline_hk_warrant_week_1year(self):
        case_name = sys._getframe().f_code.co_name
        code = 'HK.69426'
        end = '2018-11-15'
        start = '2018-11-8'
        ktype = KLType.K_WEEK
        ret, data = self.common_request_history_kline_process(case_name, code, start, end, ktype)
        # 校验：大约52条数据，code都是'HK.69426'，第一个数据和最后一个都是周1
        self.common_request_history_kline_check_success(code, ret, data)

    # 获取美股正股近1年月k数据
    def test_request_history_kline_us_stock_month_2years(self):
        case_name = sys._getframe().f_code.co_name
        code = 'US.VIPS'
        end = '2018-11-12'
        start = '2017-11-12'
        ktype = KLType.K_MON
        autype = AuType.NONE
        ret, data = self.common_request_history_kline_process(case_name, code, start, end, ktype, autype)
        # 校验：第一个数据和最后一个都是1号，code显示都是'US.AAPL'
        self.common_request_history_kline_check_success(code, ret, data)
        # 需验证日期都是1号

    # 获取A股正股近1年年k数据
    # def test_request_history_kline_ch_stock_year_2years(self):
    #     case_name = sys._getframe().f_code.co_name
    #     code = 'SZ.300431'
    #     end = '2018-11-12'
    #     start = '2017-11-12'
    #     ktype = KLType.K_YEAR
    #     autype = AuType.NONE
    #     ret, data = self.common_request_history_kline_process(case_name, code, start, end, ktype, autype)
    #     # 校验：
    #     self.common_request_history_kline_check_success(code, ret, data)

    # 美股指数获取近1年周k
    def test_request_history_kline_us_idx_week_1years(self):
        case_name = sys._getframe().f_code.co_name
        code = 'US..DJI'
        end = '2018-11-12'
        start = '2017-11-12'
        ktype = KLType.K_WEEK
        autype = AuType.HFQ
        ret, data = self.common_request_history_kline_process(case_name, code, start, end, ktype)
        # 校验：第一条数据的日期和当今在10年，code部分是'US..DJI'，都是周1
        self.common_request_history_kline_check_success(code, ret, data)

    # 美股期权获取1年月k
    def test_request_history_kline_us_option_month_allyears(self):
        case_name = sys._getframe().f_code.co_name
        code = 'US.AAPL181214C182500'
        end = '2018-11-12'
        start = '2017-11-12'
        ktype = KLType.K_DAY
        ret, data = self.common_request_history_kline_process(case_name, code, start, end, ktype)
        # 校验：空
        self.common_request_history_kline_check_success(code, ret, data)

    # 入参错误
    def test_request_history_kline_wrong_code(self):
        # code错误
        case_name = sys._getframe().f_code.co_name
        code = 'HK.0070'
        start = '2018-11-12'
        end = start
        ktype = KLType.K_DAY
        logger.info('【testcase】'+case_name)
        ret, data = quote_ctx.request_history_kline(code,start,end,ktype)
        logger.info(data)
        self.assertEqual(ret, False)

    def test_request_history_kline_wrong_date(self):
        # start格式错误
        case_name = sys._getframe().f_code.co_name
        code = 'HK.00700'
        start = '2018/11/12'
        end = start
        ktype = KLType.K_DAY
        logger.info('【testcase】'+case_name)
        ret, data = quote_ctx.request_history_kline(code,start,end,ktype)
        logger.info(data)
        self.assertEqual(ret, False)

    def test_request_history_kline_wrong_ktype(self):
        # ktype错误
        case_name = sys._getframe().f_code.co_name
        code = 'HK.00700'
        start = '2018-11-12'
        end = start
        ktype = '3分K'
        logger.info('【testcase】'+case_name)
        ret, data = quote_ctx.request_history_kline(code,start,end,ktype)
        logger.info(data)
        self.assertEqual(ret, False)

    def test_request_history_kline_wrong_autype(self):
        # autype错误
        case_name = sys._getframe().f_code.co_name
        code = 'HK.00700'
        start = '2018-11-12'
        end = start
        ktype = KLType.K_DAY
        autype = '复权值'
        logger.info('【testcase】'+case_name)
        ret, data = quote_ctx.request_history_kline(code,start,end,ktype,autype)
        logger.info(data)
        self.assertEqual(ret, False)


if __name__ == '__main__':
    quote_ctx = OpenQuoteContext('127.0.0.1',11111)
    logger = logging.getLogger('mylogger')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('request_history_kline.log')
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)

    pandas.set_option('max_columns', 100)
    pandas.set_option('display.width', 1000)

    unittest.main()

