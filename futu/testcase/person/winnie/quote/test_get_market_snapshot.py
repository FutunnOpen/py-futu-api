# -*- coding:utf-8 -*-
from futuquant import *
import pandas


def test_get_market_snapshot():
    pandas.set_option('max_columns', 100)
    pandas.set_option('display.width', 1000)
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    ret_code, ret_data = quote_ctx.get_option_chain('US.AAPL', '2018-09-01', '2018-09-24',
                                                    OptionType.ALL, OptionCondType.ALL)
    code = list(ret_data['code'])
    del code[200:]
    # print(ret_data['code'])
    # code_list = ['HK.00700', 'HK.00066', 'US.AAPL', 'SZ.000700']
    code_list = ['US.AAPL180921P235000', 'US.AAPL180921C135000']  # 'US_OPTION.AAPL180921C225000'
    print(quote_ctx.get_market_snapshot(code_list))


if __name__ == '__main__':
    test_get_market_snapshot()
