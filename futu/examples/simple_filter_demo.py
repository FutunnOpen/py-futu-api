# -*- coding: utf-8 -*-

"""演示如何使用股票筛选功能"""

from futu import *
quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
simple_filter = SimpleFilter()
simple_filter.filter_min = 2
simple_filter.filter_max = 1000
simple_filter.stock_field = StockField.CUR_PRICE
simple_filter.is_no_filter = False
# simple_filter.sort = SortDir.ASCEND
financial_filter = FinancialFilter()
financial_filter.filter_min = 0.5
financial_filter.filter_max = 50
financial_filter.stock_field = StockField.CURRENT_RATIO
financial_filter.is_no_filter = False
financial_filter.sort = SortDir.ASCEND
financial_filter.quarter = FinancialQuarter.ANNUAL
ret, ls = quote_ctx.get_stock_filter(market=Market.HK, filter_list=[simple_filter, financial_filter])  # 对香港市场的股票做简单和财务筛选
if ret == RET_OK:
    last_page, all_count, ret_list = ls
    print(len(ret_list), all_count, ret_list)
    for item in ret_list:
        print(item.stock_code)  # 取股票代码
        print(item.stock_name)  # 取股票名称
        print(item[simple_filter])   # 取 simple_filter 对应的变量值
        print(item.cur_price)   # 效果同上，也是取 simple_filter 对应的变量值
        print(item[financial_filter])   # 取 financial_filter 对应的变量值
else:
    print('error: ', ls)
quote_ctx.close()  # 结束后记得关闭当条连接，防止连接条数用尽

