#-*-coding:utf-8-*-

import futuquant

class GetAutypeList():
    # 获取复权因子get_autype_list

    def test1(self):
        quote_ctx = futuquant.OpenQuoteContext(host='127.0.0.1',port=11111)
        code_list =  ['HK.08413']
        ret_code, ret_data = quote_ctx.get_autype_list(code_list)
        quote_ctx.close()

        print(ret_code)
        # print(ret_data)
        for data in ret_data.iterrows():
            print(data)

if __name__ == '__main__':
    gal = GetAutypeList()
    gal.test1()


