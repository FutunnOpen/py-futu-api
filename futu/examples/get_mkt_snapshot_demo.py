# -*- coding: utf-8 -*-
"""
验证接口：获取某个市场的全部快照数据
"""
import time
import futu as ft


def loop_get_mkt_snapshot(api_svr_ip, api_svr_port, market):
    """
    验证接口：获取某个市场的全部快照数据 get_mkt_snapshot
    :param api_svr_ip: (string)ip
    :param api_svr_port: (int)port
    :param market: market type
    :return:
    """
    # 创建行情api
    quote_ctx = ft.OpenQuoteContext(host=api_svr_ip, port=api_svr_port)
    stock_type = [ft.SecurityType.STOCK, ft.SecurityType.IDX, ft.SecurityType.ETF, ft.SecurityType.WARRANT,
                  ft.SecurityType.BOND]

    stock_codes = []
    # 枚举所有的股票类型，获取股票codes
    for sub_type in stock_type:
        ret_code, ret_data = quote_ctx.get_stock_basicinfo(market, sub_type)
        if ret_code == 0:
            print("get_stock_basicinfo: market={}, sub_type={}, count={}".format(market, sub_type, len(ret_data)))
            for ix, row in ret_data.iterrows():
                stock_codes.append(row['code'])

    if len(stock_codes) == 0:
        quote_ctx.close()
        print("Error market:'{}' can not get stock info".format(market))
        return

    # 按频率限制获取股票快照: 每3秒200支股票
    for i in range(1, len(stock_codes), 200):
        print("from {}, total {}".format(i, len(stock_codes)))
        ret_code, ret_data = quote_ctx.get_market_snapshot(stock_codes[i:i + 200])
        if ret_code == 0:
            print(ret_data)
        time.sleep(3)

    quote_ctx.close()


if __name__ == "__main__":
    ip = '127.0.0.1'
    port = 11111

    for mkt in [ft.Market.HK, ft.Market.US, ft.Market.SZ, ft.Market.SH]:
        loop_get_mkt_snapshot(ip, port, mkt)
