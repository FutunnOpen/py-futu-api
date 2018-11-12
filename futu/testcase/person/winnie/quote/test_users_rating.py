# -* -coding:utf-8 -*-
from futuquant import *
import pandas
import time


def test_subscribe():
    pandas.set_option('max_columns', 100)
    pandas.set_option('display.width', 1000)
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    ret_code, ret_data = quote_ctx.get_stock_basicinfo(Market.HK, SecurityType.STOCK, [])
    code_list = list(ret_data['code'])
    del code_list[99:]  # 截取股票
    # print(code_list)
    print(quote_ctx.subscribe(code_list,
                             [SubType.TICKER]))
    #
    print(quote_ctx.query_subscription())


def test_get_market_snapshot():
    pandas.set_option('max_columns', 100)
    pandas.set_option('display.width', 1000)
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    ret_code, ret_data = quote_ctx.get_stock_basicinfo(Market.HK, SecurityType.STOCK, [])
    code_list = list(ret_data['code'])
    del code_list[200:]  # 截取股票
    print(len(code_list))
    start = time.time()
    print(start)
    flag = True
    index = 0
    end = 0
    while flag:
        print(index)
        ret_code, ret_data = quote_ctx.get_market_snapshot(code_list)
        print(ret_data)
        index = index + 1
        end = time.time()
        if end - start >= 30:
            flag = False
    print(end)
    time.sleep(1)
    ret_code, ret_data = quote_ctx.get_market_snapshot(code_list)
    print(ret_data)


# 请求次数测试
def test_request_nums():
    # -------30秒的请求次数测试
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    flag = True
    start = time.time()
    print(start)
    index = 0
    end = 0
    while flag:
        print(index)
        ret_code, ret_data, page_key = quote_ctx.request_history_kline(code='HK.00700', start='2018-08-15',
                                                                       end='2018-08-21', ktype=KLType.K_DAY,
                                                                       max_count=1)
        print(ret_data)
        index = index + 1
        end = time.time()
        if end - start >= 30:
            flag = False
    print(end)


# 请求股票支数测试
def test_request_stock_count():
    pandas.set_option('max_columns', 100)
    pandas.set_option('display.width', 1000)
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    ret_code, ret_data = quote_ctx.get_stock_basicinfo(Market.HK, SecurityType.STOCK, [])
    code_list = list(ret_data['code'])
    del code_list[0:1000]  # 截取股票
    del code_list[1200:]
    # print(code_list)
    # print(quote_ctx.request_history_kline(code='US.AAPL180921P235000', start='2018-08-15', end='2018-09-15',
    #                                       ktype=KLType.K_DAY, max_count=40))
    # print(quote_ctx.request_history_kline(code='US.AAPL180921C135000', start='2018-08-15', end='2018-08-23',
    #                                       ktype=KLType.K_DAY,max_count=40))
    # print(quote_ctx.request_history_kline(code='HK.00700', start='2007-08-31', end='2018-08-16',
    #                                       ktype=KLType.K_DAY))
    # ------每次请求的股票只数测试
    page_key = None
    for i in range(400):
        print(i)
        if i != 0 and i % 10 == 0:
            time.sleep(30)
        ret_code, ret_data, page_key = quote_ctx.request_history_kline(code='US.DIS', start='2018-08-01',
                                                                       end='2018-08-07', ktype=KLType.K_WEEK,
                                                                       autype=AuType.NONE, fields=KL_FIELD.ALL_REAL,
                                                                       max_count=1)
        print(ret_data)


if __name__ == '__main__':
    # test_subscribe()
    # test_get_market_snapshot()
    # test_request_stock_count()
    # test_request_nums()

    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    # print(quote_ctx.get_stock_basicinfo(Market.HK, SecurityType.WARRANT))
    print(quote_ctx.get_stock_basicinfo(Market.US, SecurityType.DRVT, ['US.AAPL180921C175000']))
    quote_ctx.close()
