# -*- coding: utf-8 -*-

from collections import namedtuple
import logging
import csv
import functools
from futuquant import *

class StockInfo:
    def __init__(self, code=None, name=None, stock_type=None, turnover=None, volume=None):
        self.code = code
        self.name = name
        self.stock_type = stock_type
        self.turnover = turnover
        self.volume = volume

    def to_tuple(self):
        return (self.code, self.name, self.stock_type, self.turnover, self.volume)

    def from_tuple(self, t):
        self.code, self.name, self.stock_type, self.turnover, self.volume = t
        self.turnover = float(self.turnover)
        self.volume = float(self.volume)

    @classmethod
    def titles(cls):
        return 'code', 'name', 'stock_type', 'turnover', 'volume'

class Worker:
    def __init__(self, market, filter_func):
        self.marker = market
        self.filter_func = filter_func
        self.stock_info_list = [] # (code, turnover)
        self.stock_code_name_map = {}

    def collect(self):
        quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
        quote_ctx.start()
        ret, stock_info_pd = quote_ctx.get_stock_basicinfo(self.marker, SecurityType.STOCK)
        self._filter_stock_list(quote_ctx, stock_info_pd)
        quote_ctx.close()
        return self.stock_info_list

    def _filter_stock_list(self, quote_ctx, stock_pd):
        stock_codes = []

        def handle_stock_codes():
            ret, data = quote_ctx.get_market_snapshot(stock_codes)
            time.sleep(3.5)
            if ret == RET_OK:
                self._filter_stock_snapshot(data)
                return RET_OK
            else:
                print(data)
                return RET_ERROR

        for stock_info in stock_pd.itertuples():
            self.stock_code_name_map[stock_info.code] = stock_info
            stock_codes.append(stock_info.code)
            if len(stock_codes) == 100:
                ret = handle_stock_codes()
                if ret != RET_OK:
                    return
                stock_codes.clear()

        if len(stock_codes) > 0:
            handle_stock_codes()

    def _filter_stock_snapshot(self, stock_snapshot_list):
        for snapshot in stock_snapshot_list.itertuples():
            stock_info = self.stock_code_name_map[snapshot.code]
            if self.filter_func(snapshot, stock_info):
                info = StockInfo(code=snapshot.code,
                                 name=stock_info.name,
                                 stock_type=stock_info.stock_type,
                                 turnover=snapshot.turnover,
                                 volume=snapshot.volume)
                self.stock_info_list.append(info)


def load_stock_code(csv_file):
    code_list = []
    with open(csv_file, 'r', encoding='gb18030') as fo:
        reader = csv.reader(fo)
        # for row in reader:
            # print(row)
        code_list = [row[0] for row in reader]
    return code_list

def get_codes_cvs():
    '''
    获取cvs中的股票代码列表
    :return:
    '''
    # path_csv = os.getcwd() + os.path.sep + 'stock1.csv'
    codes = load_stock_code(r'c:\Users\admin\futu\futuquant1\datas\stock1.csv') #r'D:\FutuCode\api\futuquant_feature_v3.0_test0525\evatest\datas\stock1.csv'
    return codes

def filter_stock(snapshot, stock_info):
    return not snapshot.suspension

def export_stock():
    w = Worker(Market.US, filter_stock)
    stock_info_list = w.collect()
    with open(r'd:\tmp\stock3.csv', 'w', encoding='gb18030', newline='\n') as fo:
        writer = csv.writer(fo)
        writer.writerow(StockInfo.titles())
        for stock_info in stock_info_list:
            writer.writerow(stock_info.to_tuple())

def sort_stock(csv_file, out_csv_file):
    def cmp(lhs, rhs):
        if lhs.volume > rhs.volume:
            return -1
        elif lhs.volume == rhs.volume:
            return 0
        return 1

    stocks = []
    with open(csv_file, 'r', encoding='gb18030', newline='\n') as fo:
        fo.readline()
        reader = csv.reader(fo)
        for row in reader:
            stock_info = StockInfo()
            stock_info.from_tuple(row)
            stocks.append(stock_info)

    stocks = sorted(stocks, key=functools.cmp_to_key(cmp))

    with open(out_csv_file, 'w', encoding='gb18030', newline='\n') as fo:
        writer = csv.writer(fo)
        writer.writerow(StockInfo.titles())
        for stock_info in stocks:
            writer.writerow(stock_info.to_tuple())

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    # path_csv =os.getcwd()+ os.path.sep +'stock1.csv'
    # codes = load_stock_code(r'D:\FutuCode\api\futuquant_feature_v3.0_test0525\evatest\datas\stock1.csv')
    # print(codes[0])
    # print(len(codes))
    # export_stock()
    sort_stock(r'd:\tmp\stock-us.csv', r'd:\tmp\stock-us-vol.csv')