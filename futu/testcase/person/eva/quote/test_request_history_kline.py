#-*-coding=utf-8-*-

import pandas
from futu import *
from futu.testcase.person.eva.datas.collect_stock import *

class RequestHstyKl(object):
    #请求历史K线

    def __init__(self):
        pandas.set_option('display.width', 1000)
        pandas.set_option('max_columns', 1000)

    def test1(self):
        host = '172.18.6.144'   #mac 172.18.6.144
        port = 11112
        req_sleep = 4
        quote_ctx = OpenQuoteContext(host,port)
        # s = time.time()
        # print(s)
        req_key = None
        ret_code,ret_data = quote_ctx.get_stock_basicinfo(market = Market.HK, stock_type=SecurityType.STOCK, code_list=None)
        codes = ret_data['code'].tolist()
        for i in range(1001):
            print(i,'code = ',codes[i])
            print(quote_ctx.request_history_kline(codes[i],
                              start='2018-8-21',
                              end='2018-8-21',
                              ktype=KLType.K_DAY,
                              autype=AuType.QFQ,
                              fields=[KL_FIELD.ALL],
                              max_count=1,
                              page_req_key=None))
            time.sleep(req_sleep)

        # e = time.time()
        # print(s)
        # print('时延（秒）：',e - s)

    def test2(self):
        host = '127.0.0.1'  # mac 172.18.6.144
        port = 11111
        quote_ctx = OpenQuoteContext(host, port)
        print(quote_ctx.request_history_kline(code = 'HK.00700',
                              start=None,
                              end=None,
                              ktype=KLType.K_DAY,
                              autype=AuType.QFQ,
                              fields=[KL_FIELD.ALL],
                              max_count=1000,
                              page_req_key=None))

    def test3(self):
        host = '127.0.0.1'  # mac 172.18.6.144
        port = 11112
        quote_ctx = OpenQuoteContext(host, port)
        req_key = None
        for i in range(20):
            print(i)
            ret_code, ret_data ,req_key = quote_ctx.request_history_kline(code = 'HK.00700',
                              start='2018-8-1',
                              end='2018-8-16',
                              ktype=KLType.K_1M,
                              autype=AuType.QFQ,
                              fields=[KL_FIELD.ALL],
                              max_count=331,
                              page_req_key=req_key)
            print(ret_data)


if __name__ == '__main__':
    rhk = RequestHstyKl()
    rhk.test2()

