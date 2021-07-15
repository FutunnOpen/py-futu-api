# -*- coding: utf-8 -*-

"""演示如何使用股票筛选功能"""

import futu as ft

def simple_financial_filter(api_svr_ip, api_svr_port):
    """
    验证接口：条件选股功能 get_stock_filter
    这里只设置了“简单属性”和“财务属性”作为筛选条件，。
    :param api_svr_ip: (string)ip
    :param api_svr_port: (int)port
    :return:
    """
    # 创建行情api
    quote_ctx = ft.OpenQuoteContext(host=api_svr_ip, port=api_svr_port)

    # 简单属性
    simple_filter = ft.SimpleFilter()
    simple_filter.filter_min = 2
    simple_filter.filter_max = 1000
    simple_filter.stock_field = ft.StockField.CUR_PRICE
    simple_filter.is_no_filter = False
    # simple_filter.sort = SortDir.ASCEND

    # 财务属性
    financial_filter = ft.FinancialFilter()
    financial_filter.filter_min = 0.5
    financial_filter.filter_max = 50
    financial_filter.stock_field = ft.StockField.CURRENT_RATIO
    financial_filter.is_no_filter = False
    financial_filter.sort = ft.SortDir.ASCEND # 多个筛选条件，只能有一个排序方向。
    financial_filter.quarter = ft.FinancialQuarter.ANNUAL

    # 对香港市场的股票做简单和财务筛选
    ret, ls = quote_ctx.get_stock_filter(market=ft.Market.HK,
                                         filter_list=[simple_filter, financial_filter])
    if ret == ft.RET_OK:
        last_page, all_count, ret_list = ls
        print(len(ret_list), all_count, ret_list)
        for item in ret_list:
            print(item.stock_code)  # 取股票代码
            print(item.stock_name)  # 取股票名称
            print(item[simple_filter])  # 取 simple_filter 对应的变量值
            print(item.cur_price)  # 效果同上，也是取 simple_filter 对应的变量值
            print(item[financial_filter])  # 取 financial_filter 对应的变量值
    else:
        print('error: ', ls)

    quote_ctx.close()  # 结束后记得关闭当条连接，防止连接条数用尽

if __name__ == "__main__":
    ip = '127.0.0.1'
    port = 11111

    simple_financial_filter(ip, port)
