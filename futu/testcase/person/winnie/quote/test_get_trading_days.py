# -*- coding:utf-8 -*-
from futuquant import *
import time

def test_get_trading_days():
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    # ret_code, ret_data = quote_ctx.get_trading_days(market='HK', start='1970-01-01',
    #                                                 end=time.strftime('%Y-%m-%d', time.localtime(time.time())))

    ret_code, ret_data = quote_ctx.get_trading_days(market='HK', start='2018-01-01',
                                                    end='2018-13-02')
    print(ret_code)
    print(ret_data)
    # ret_code, ret_data = quote_ctx.get_global_state()
    # print(ret_data)


if __name__ == '__main__':
    test_get_trading_days()