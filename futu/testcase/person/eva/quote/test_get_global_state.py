#-*-coding:utf-8-*-

from futuquant import *
import time
import datetime

class GetGlobalState(object):
    # 获取牛牛程序全局状态 get_global_state

    def test1(self):
        quote_ctx = OpenQuoteContext(host='127.0.0.1',port=11111)
        ret_code,state_dict = quote_ctx.get_global_state()

        print(ret_code)
        print(state_dict)
        quote_ctx.close()

    def test2(self):
        num = 1000
        quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
        start = datetime.datetime.now()
        for index in range(num):
            quote_ctx.get_global_state()
        end = datetime.datetime.now()
        print('get_global_state请求一千次，耗时(秒)：',end - start)

    def test6(self):
        quote_ctx_285706 = OpenQuoteContext('127.0.0.1',11112)
        quote_ctx_5914062 = OpenQuoteContext('127.0.0.1',11115)
        for i in range(1000000):
            print( datetime.datetime.now(),' quote_ctx_285706 ',quote_ctx_285706.get_global_state())
            print( datetime.datetime.now(),' quote_ctx_5914062 ', quote_ctx_285706.get_global_state())
            time.sleep(60)

if __name__ == '__main__':
    ggs = GetGlobalState()
    ggs.test2()