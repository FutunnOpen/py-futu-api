# -*- coding: utf-8 -*-
"""
    实例: 股票卖出函数
"""
from time import sleep
import futu as ft
import sys

def simple_sell(quote_ctx, trade_ctx, stock_code, trade_price, volume, trade_env, order_type=ft.OrderType.NORMAL):
    """简单卖出函数。取到股票每手的股数后，就下单卖出"""
    lot_size = 0  # 每手多少股
    while True:
        sleep(1)
        if lot_size == 0:
            ret, data = quote_ctx.get_market_snapshot(stock_code)
            lot_size = data.iloc[0]['lot_size'] if ret == ft.RET_OK else 0
            if ret != ft.RET_OK:
                print("can't get lot size, retrying: {}".format(data))
                continue
            elif lot_size <= 0:
                raise Exception('lot size error {}:{}'.format(lot_size, stock_code))

        qty = int(volume // lot_size) * lot_size  # 将数量调整为整手的股数
        ret, data = trade_ctx.place_order(price=trade_price, qty=qty, code=stock_code,
                                          trd_side=ft.TrdSide.SELL, trd_env=trade_env, order_type=order_type)
        if ret != ft.RET_OK:
            print('simple_sell 下单失败:{}'.format(data))
            return None
        else:
            print('simple_sell 下单成功')
            return data


def smart_sell(quote_ctx, trade_ctx, stock_code, volume, trade_env, order_type=ft.OrderType.NORMAL):
    """智能卖出函数。取到股票每手的股数，以及摆盘数据后，就以买一价下单卖出"""
    lot_size = 0  # 每手多少股
    while True:
        if lot_size == 0:
            ret, data = quote_ctx.get_market_snapshot(stock_code)
            lot_size = data.iloc[0]['lot_size'] if ret == ft.RET_OK else 0
            if ret != ft.RET_OK:
                print("can't get lot size, retrying:".format(data))
                continue
            elif lot_size <= 0:
                raise Exception('lot size error {}:{}'.format(lot_size, stock_code))

        qty = int(volume / lot_size) * lot_size  # 将数量调整为整手的股数
        ret, data = quote_ctx.get_order_book(stock_code)  # 获取摆盘
        if ret != ft.RET_OK:
            print("can't get orderbook, retrying:{}".format(data))
            continue

        price = data['Bid'][0][0]  # 取得买一价
        print('smart_sell bid price is {}'.format(price))

        # 以买一价下单卖出
        ret, data = trade_ctx.place_order(price=price, qty=qty, code=stock_code,
                                          trd_side=ft.TrdSide.SELL, trd_env=trade_env, order_type=order_type)
        if ret != ft.RET_OK:
            print('smart_sell 下单失败:{}'.format(data))
            return None
        else:
            print('smart_sell 下单成功')
            print(data)
            return data


if __name__ =="__main__":
    ip = '127.0.0.1'
    port = 11111
    code = 'HK.00700'      # 要卖出的股票
    unlock_pwd = '123456'  # 解锁交易密码
    trd_env = ft.TrdEnv.SIMULATE  # 模拟交易
    order_type = ft.OrderType.NORMAL  # 订单类型

    quote_ctx = ft.OpenQuoteContext(ip, port)
    trd_ctx = ft.OpenHKTradeContext(ip, port)

    quote_ctx.subscribe(code, ft.SubType.ORDER_BOOK)  # 订阅摆盘，这样后面才能调用get_order_book
    ret, data = trd_ctx.unlock_trade(unlock_pwd)
    if ret == ft.RET_OK:
        print("* unlock_trade success")
        simple_sell(quote_ctx, trd_ctx, code, 280.0, 100, trd_env, order_type)
        smart_sell(quote_ctx, trd_ctx, code, 100, trd_env, order_type)
    else:
        print("* unlock_trade fail: ", data)

    quote_ctx.close()
    trd_ctx.close()

