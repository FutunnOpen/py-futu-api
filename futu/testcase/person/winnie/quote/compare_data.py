# -*- coding:utf-8 -*-
from futuquant import *
import pandas


# example
# quote_ctx = OpenQuoteContext('127.0.0.1',11111)
# code = 'HK.00700'
# quote_ctx.subscribe(code, SubType.QUOTE)
# ret_code, ret_data = quote_ctx.get_stock_quote(code)
# print(ret_data)
# df = pandas.DataFrame(ret_data)
# print(df.columns)
# print(list(df.columns))

class CompareData():
    def compare(self,data1,data2):
        '''
        :param data1:
        :param data2:
        :return:
        '''
        '''
        # 比较步骤
        0、对比data1和data2的数据类型是否一致
        1、获取data1和data2的列名，并比较列名是否相等;
        2、比较每个字段对应的数据是否一致<有些数字类型的字段需要将精度统一再比较>
        '''
        if type(data1) != type(data2):
            print('数据类型不一致')
            return -1
        if type(data1) == 'str':
            if data1 != data2:
                print('数据内容不一致')
                return -1
            else:
                print('数据内容一致')
                return 0

        if type(data1) == 'DataFrame':
            df1 = pandas.DataFrame(data1)
            col1 = list(df1.columns)
            df2 = pandas.DataFrame(data1)
            col2 = list(df2.columns)
            if col1 != col2:
                print('两者的列不同')
                return -1
            


        pass


if __name__ == '__main__':
    cd = CompareData()
    cd.compare(None,None)