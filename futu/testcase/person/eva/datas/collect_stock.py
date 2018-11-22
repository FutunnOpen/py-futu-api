# -*- coding: utf-8 -*-

from collections import namedtuple
import logging
import csv
from futu import *

class StockInfo:
    def __init__(self, code=None, name=None, stock_type=None, turnover=None):
        self.code = code
        self.name = name
        self.stock_type = stock_type
        self.turnover = turnover

class Worker:
    def __init__(self, market=Market.HK):
        self.marker = market
        self.stock_info_list = [] # (code, turnover)

    def collect(self):
        quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
        quote_ctx.start()
        ret, plate_list = quote_ctx.get_plate_list(self.marker, Plate.ALL)
        stock_info_map = {}
        for plate in plate_list.itertuples():
            stock_info_map.update(self._get_plate_stocks(quote_ctx, plate.code))

        self._fill_stock_turnover(quote_ctx, stock_info_map)
        for stock_code, stock_info in stock_info_map.items():
            print(stock_code, stock_info.turnover)

        self.stock_info_list.extend(stock_info_map.values())
        return self.stock_info_list

    def _get_plate_stocks(self, quote_ctx, plate):
        result = {}
        ret, data = quote_ctx.get_plate_stock(plate)
        if ret == RET_OK:
            for row in data.itertuples():
                item = StockInfo(code=row.code,
                                 name=row.stock_name,
                                 stock_type=row.stock_type,
                                 turnover=0)
                result[item.code] = item
        return result

    def _fill_stock_turnover(self, quote_ctx, stock_info_map):
        group = []
        for stock_code, stock_info in stock_info_map.items():
            group.append(stock_info)
            if len(group) == 20:
                ret, data = quote_ctx.get_market_snapshot([stock.code for stock in group])
                if ret == RET_OK:
                    for snapshot in data.itertuples():
                        stock_info_map[snapshot.code].turnover = snapshot.turnover
                else:
                    logging.warning('get_market_snapshot err: {0}'.format(data))
                    return
                group.clear()


        if len(group) > 0:
            ret, data = quote_ctx.get_market_snapshot([stock.code for stock in group])
            if ret == RET_OK:
                for snapshot in data.itertuples():
                    stock_info_map[snapshot.code].turnover = snapshot.turnover
            else:
                logging.warning('get_market_snapshot err: {0}'.format(data))
                return


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
    path_csv = r'D:\\FutuCode\\api\\FutuOpenAPI\\futu\\testcase\\person\\eva\\datas\\stock1.csv'#os.path.dirname(os.path.dirname(os.getcwd())) + os.path.sep +'datas'+ os.path.sep +'stock1.csv'
    codes = load_stock_code(path_csv) # r'D:\FutuCode\api\FutuOpenAPI\futu\testcase\person\eva\datas\\stock1.csv'
    return codes

def export_stock():
    w = Worker(Market.HK)
    stock_info_list = w.collect()
    with open(r'd:\tmp\stock1.csv', 'w', encoding='gb18030', newline='\n') as fo:
        writer = csv.writer(fo)
        for stock_info in stock_info_list:
            writer.writerow([stock_info.code, stock_info.name, stock_info.turnover])

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    # path_csv =os.getcwd()+ os.path.sep +'stock1.csv'
    codes = load_stock_code(r'D:\FutuCode\api\futu_feature_v3.0_test0525\evatest\datas\stock1.csv')
    print(codes[0])
    print(len(codes))