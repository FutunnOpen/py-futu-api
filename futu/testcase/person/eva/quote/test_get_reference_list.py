#-*-coding:utf-8-*-

from futuquant import *
import pandas

class GetReferenceList(object):

    def test1(self):
        SysConfig.set_all_thread_daemon(False)
        quote_ctx = OpenQuoteContext(host='127.0.0.1',port=11111)

        ret_code, ret_data = quote_ctx.get_referencestock_list(code = 'HK.00700', reference_type = SecurityReferenceType.WARRANT)
        pandas.set_option('max_columns', 100)
        pandas.set_option('display.width', 1000)
        put_df = ret_data[ret_data['wrt_type'] == WrtType.PUT]
        codelist_put = put_df['code'].tolist()
        print(type(codelist_put))
        print(codelist_put)

        # print(ret_code)
        # print(ret_data)
        # print(ret_data.columns)
        # i = 0
        # for data in ret_data.values:
        #     print(i,data)
        #     i+=1

if __name__ == '__main__':

    grl = GetReferenceList()
    grl.test1()