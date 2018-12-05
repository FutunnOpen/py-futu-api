# -*- coding: utf-8 -*-
"""
    实例: 股票卖出函数
"""
from time import sleep
import futu as ft


def simple_sell(quote_ctx, trade_ctx, stock_code, trade_price, volume, trade_env, order_type=ft.OrderType.NORMAL):
    """简单卖出函数"""
    lot_size = 0
    while True:
        sleep(0.1)
        if lot_size == 0:
            ret, data = quote_ctx.get_market_snapshot(stock_code)
            lot_size = data.iloc[0]['lot_size'] if ret == ft.RET_OK else 0
            if ret != ft.RET_OK:
                print("can't get lot size, retrying: {}".format(data))
                continue
            elif lot_size <= 0:
                raise Exception('lot size error {}:{}'.format(lot_size, stock_code))

        qty = int(volume // lot_size) * lot_size
        ret, data = trade_ctx.place_order(price=trade_price, qty=qty, code=stock_code,
                                          trd_side=ft.TrdSide.SELL, trd_env=trade_env, order_type=order_type)
        if ret != ft.RET_OK:
            print('simple_sell 下单失败:{}'.format(data))
            return None
        else:
            print('simple_sell 下单成功')
            return data


def smart_sell(quote_ctx, trade_ctx, stock_code, volume, trade_env, order_type=ft.OrderType.NORMAL):
    """智能卖出函数"""
    lot_size = 0
    while True:
        if lot_size == 0:
            ret, data = quote_ctx.get_market_snapshot(stock_code)
            lot_size = data.iloc[0]['lot_size'] if ret == ft.RET_OK else 0
            if ret != ft.RET_OK:
                print("can't get lot size, retrying:".format(data))
                continue
            elif lot_size <= 0:
                raise Exception('lot size error {}:{}'.format(lot_size, stock_code))

        qty = int(volume / lot_size) * lot_size
        ret, data = quote_ctx.get_order_book(stock_code)
        if ret != ft.RET_OK:
            print("can't get orderbook, retrying:{}".format(data))
            continue

        price = data['Bid'][0][0]
        print('smart_sell bid price is {}'.format(price))

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

    code = 'HK.00700'
    unlock_pwd = '123456'
    trd_env = ft.TrdEnv.SIMULATE
    order_type = ft.OrderType.NORMAL

    quote_ctx = ft.OpenQuoteContext(ip, port)
    trd_ctx = ft.OpenHKTradeContext(ip, port)

    quote_ctx.subscribe(code, ft.SubType.ORDER_BOOK)
    print("* unlock_trade:{}".format(trd_ctx.unlock_trade(unlock_pwd)))

    simple_sell(quote_ctx, trd_ctx, code, 280.0, 100, trd_env, order_type)
    smart_sell(quote_ctx, trd_ctx, code, 100, trd_env, order_type)

    quote_ctx.close()
    trd_ctx.close()

