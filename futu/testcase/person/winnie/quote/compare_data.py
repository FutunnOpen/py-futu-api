# -*- coding:utf-8 -*-
from futu import *
import pandas


# example
# quote_ctx = OpenQuoteContext('127.0.0.1',11111)
# code = 'HK.00700'
# quote_ctx.subscribe(code, SubType.QUOTE)
# ret_code, ret_data = quote_ctx.get_stock_quote(code)
# print(ret_data)
# print(list(ret_data['code']))
# df = pandas.DataFrame(ret_data)
# print(df.columns)
# print(list(df.columns))

class CompareData():
    def compareOtherFields(self, data1, data2, field_name):
        data1_field = list(data1[field_name])
        data2_field = list(data2[field_name])
        if data1_field == data2_field:
            return -2
        # 找不相等的行
        i = 0
        for i in range(0,len(data1_field)-1):
            if data1_field[i] != data2_field[i]:
                return i
        return -2

    def comparePrice(self, data1, data2, field_name,is_list=False):
        data1_field = data2_field = []
        if is_list is False:
            data1_field = list(data1[field_name])
            data2_field = list(data2[field_name])
        else:
            data1_field = data1
            data2_field = data2
        if data1_field == data2_field:
            return -2
        # 需要将价格转换精度
        i = 0
        for i in range(0,len(data1_field)-1):
            tmp1 = float('%.3f'%data1_field[i])
            tmp2 = float('%.3f'%data2_field[i])
            if abs(tmp1 - tmp2) < 1e-10:
                continue
            else:
                return i
        return -2

    def compare(self,data1,data2):
        '''
        :param data1:
        :param data2:
        :return:
        '''
        '''
        # 比较步骤
        0、对比data1和data2的数据类型是否一致
        1、获取data1和data2的列名，并比较列名是否相等
        2、比较每个字段对应的数据是否一致<有些数字类型的字段需要将精度统一再比较>
        '''
        if type(data1) != type(data2):
            print('数据类型不一致')
            return -1
        if type(data1) == type('test'):
            if data1 != data2:
                print('数据内容不一致')
                return -1
            else:
                print('数据内容一致')
                return -2
        col1 = col2 = []
        i = 0
        if type(data1) == type(pd.DataFrame(columns=['A'])):
            if len(data1) != len(data2):
                print('数据条数不相等')
                return -1
            if len(data1) == 0:
                print('数据是空')
                return -2
            df1 = pandas.DataFrame(data1)
            col1 = list(df1.columns)
            df2 = pandas.DataFrame(data2)
            col2 = list(df2.columns)
            if col1 != col2:
                print('两者的列不同')
                return -1
        col_list = col1
        for field_name in col_list:
            if 'price' in field_name or 'amplitude' is field_name:
                # 表明是价格相关的字段，需要调整精度
                ret = self.comparePrice(data1, data2, field_name)
                if ret != -2:
                    print(field_name,ret)
                    return ret
                continue
            else:
                ret = self.compareOtherFields(data1, data2, field_name)
                if ret != -2:
                    print(field_name,ret)
                    return ret
                continue
        return -2



if __name__ == '__main__':
    cd = CompareData()
    # cd.compareOtherFields(None,None,None)
