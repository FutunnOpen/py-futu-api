#-*-coding:utf-8-*-

from futuquant import *

class GetPlateList(object):
    # 获取板块集合下的子板块列表 get_plate_list

    def test1(self):
        # SysConfig.set_init_rsa_file('E:\\test\\testing\\conn_key.txt') #配置密钥所在路径。
        # SysConfig.enable_proto_encrypt(True) #打开加密配置

        quote_ctx = OpenQuoteContext(host='127.0.0.1',port=11111)
        market = Market.US
        plate_class = Plate.REGION
        ret_code, ret_data = quote_ctx.get_plate_list(market, plate_class)
        quote_ctx.close()

        print(ret_code)
        print(ret_data)

if __name__== '__main__':
    gpl = GetPlateList()
    gpl.test1()