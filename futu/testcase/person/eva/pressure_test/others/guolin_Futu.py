
import os
import futu as ft
import pandas as pd
import time

quote_ctx = ft.OpenQuoteContext(host='lim.app', port=11113)


def get_sh_stock_list():
    xs, ret_data = quote_ctx.get_stock_basicinfo(market='SH', stock_type='STOCK')
    ret_data = ret_data[~ret_data.name.str.contains('ST')]
    ret_data = ret_data[ret_data.code.str.startswith('SH.60')]
    ret_data.drop(['lot_size', 'stock_type', 'stock_child_type', 'stock_owner', 'listing_date', 'stock_id'], axis=1, inplace=True)
    # return list(ret_data['code'])
    return ret_data


def get_sz_stock_list():
    xs, ret_data = quote_ctx.get_stock_basicinfo(market='SZ', stock_type='STOCK')
    ret_data = ret_data[~ret_data.name.str.contains('ST')]
    ret_data = ret_data[ret_data.code.str.startswith('SZ.00') | ret_data.code.str.startswith('SZ.30')]
    ret_data.drop(['lot_size', 'stock_type', 'stock_child_type', 'stock_owner', 'listing_date', 'stock_id'], axis=1, inplace=True)
    # return list(ret_data['code'])
    return ret_data


def get_monitor_list(stock_list):
    filename = time.strftime("%Y-%m-%d", time.localtime()) + '.csv'

    if os.path.exists(filename):
        stocks_info = pd.read_csv(filename)
    else:
        stocks_count = stock_list.iloc[:, 0].size
        stocks_info = pd.DataFrame()

        for xx in range(0, stocks_count, 200):
            print("From {}, total {}".format(xx, stocks_count))
            ret_code, info = quote_ctx.get_market_snapshot(list(stock_list[xx:xx + 200]['code']))
            stocks_info = stocks_info.append(info, ignore_index=True)
            time.sleep(3)

        stocks_info = pd.merge(stocks_info, stock_list, on=['code'])
        stocks_info.drop(['open_price', 'high_price', 'low_price', 'turnover', 'turnover_rate',
                          'volume', 'listing_date', 'wrt_valid', 'wrt_conversion_ratio', 'wrt_type', 'wrt_strike_price',
                          'ey_ratio', 'issued_shares', 'net_asset'], axis=1, inplace=True)
        stocks_info = stocks_info[(stocks_info['prev_close_price'] < 50) &
                                  (stocks_info['total_market_val'] < 20000000000) &
                                  (~stocks_info['suspension']) &
                                  (stocks_info['earning_per_share'] > 0.05)]

        print(stocks_info)
        stocks_info.to_csv(filename)
    return stocks_info


def main():
    # 将沪深两市的股票代码存储到本地的csv， 每次从文件读取，比从接口读快！
    if os.path.exists('all_codes.csv'):
        all_stocks = pd.read_csv('all_codes.csv')
    else:    # 如果不存在股票代码文件，则从接口获取， 并保存到 all_codes.csv ,  问题：新股数据会没有
        sh_stocks = get_sh_stock_list()
        sz_stocks = get_sz_stock_list()
        all_stocks = sh_stocks.append(sz_stocks)
        all_stocks.to_csv('all_codes.csv')

    # print(all_stocks)

    monitor_list = get_monitor_list(all_stocks)
    print(monitor_list.iloc[:, 0].size)

    sh_mo = monitor_list[monitor_list.code.str.startswith('SH.60')]
    print('ShangHai:', sh_mo.iloc[:, 0].size)
    sc_mo = monitor_list[monitor_list.code.str.startswith('SZ.00')]
    print('Shenzhen:', sc_mo.iloc[:, 0].size)
    sz_mo = monitor_list[monitor_list.code.str.startswith('SZ.30')]
    print('Chuangye:', sz_mo.iloc[:, 0].size)

    quote_ctx.close()


if __name__ == "__main__":
    main()
