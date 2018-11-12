# 8月迭代2--通过标的股查询期权
# -*- coding:utf-8 -*-
from futuquant import *
import pandas


def test_get_option_chain():
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    # call width
    ret_code, ret_data = quote_ctx.get_option_chain(code='US.AAPL', start_date='2018-08-12', end_date='2018-08-25',
                                                    option_type=OptionType.CALL, option_cond_type=OptionCondType.WITHIN)
    # call output
    ret_code, ret_data = quote_ctx.get_option_chain(code='US.AAPL', start_date='2018-08-12', end_date='2018-08-25',
                                                    option_type=OptionType.CALL, option_cond_type=OptionCondType.OUTSIDE)
    # call all
    ret_code, ret_data = quote_ctx.get_option_chain(code='US.AAPL', start_date='2018-08-12', end_date='2018-08-25',
                                                    option_type=OptionType.CALL,
                                                    option_cond_type=OptionCondType.ALL)
    # all all
    ret_code, ret_data = quote_ctx.get_option_chain(code='US.AAPL', start_date='2018-08-12', end_date='2018-08-25',
                                                    option_type=OptionType.ALL,
                                                    option_cond_type=OptionCondType.ALL)
    # put all
    ret_code, ret_data = quote_ctx.get_option_chain(code='US.AAPL', start_date='2018-08-12', end_date='2018-08-25',
                                                    option_type=OptionType.PUT,
                                                    option_cond_type=OptionCondType.ALL)
    # others others
    ret_code, ret_data = quote_ctx.get_option_chain(code='US.AAPL', start_date='2018-08-12', end_date='2018-08-25',
                                                    option_type='put',
                                                    option_cond_type='all')
    # 日期跨度30天以上
    ret_code, ret_data = quote_ctx.get_option_chain(code='US.AAPL', start_date='2018-08-12', end_date='2018-09-25',
                                                    option_type=OptionType.PUT,
                                                    option_cond_type=OptionCondType.ALL)
    # 无期权
    ret_code, ret_data = quote_ctx.get_option_chain(code='US.BRK.A', start_date='2018-08-12', end_date='2018-08-25',
                                                    option_type=OptionType.PUT,
                                                    option_cond_type=OptionCondType.ALL)
    print(ret_data)


if __name__ == '__main__':
    pandas.set_option('max_columns', 100)
    pandas.set_option('display.width', 1000)
    test_get_option_chain()
