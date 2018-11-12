#-*-coding:utf-8-*-

import futuquant

class GetPlateStock(object):
    # 获取板块集合下的子板块列表 get_plate_list

    def test1(self):
        quote_ctx = futuquant.OpenQuoteContext(host='127.0.0.1',port=11111)
        plate_code = 'HK.BK1102'
        ret_code, ret_data = quote_ctx.get_plate_stock(plate_code)
        quote_ctx.close()

        print(ret_code)
        # print(ret_data)
        for data in ret_data.iterrows():
            print(data)

if __name__ == '__main__':
    gps = GetPlateStock()
    gps.test1()