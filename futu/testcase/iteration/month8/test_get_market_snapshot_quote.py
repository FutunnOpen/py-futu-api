# 8月迭代2--查询美股期权行情

# -*- coding:utf-8 -*-
from futuquant import *
import pandas


def test_get_market_snapshot():
    pandas.set_option('max_columns', 100)
    pandas.set_option('display.width', 1000)
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

    # code_list=['HK.00700', 'HK.00066', 'US.AAPL', 'SZ.000700'] # 港股正股、美股、A股
    # code_list = ['US_OPTION.AAPL180907P160000', 'US_OPTION.AAPL180921C225000'] # 美股期权
    ret_code, ret_data = quote_ctx.get_option_chain('US.AAPL', '2018-09-01', '2018-09-24',
                                                    OptionType.ALL, OptionCondType.ALL)
    code_list = list(ret_data['code'])
    del code_list[200:]  # 200只期权
    print(quote_ctx.get_market_snapshot(code_list))


if __name__ == '__main__':
    test_get_market_snapshot()