#-*-coding:utf-8-*-

from futuquant import *
import pandas

class GetMarketSnapshot(object):
    # 获取市场快照 get_market_snapshot

    def __init__(self):
        pandas.set_option('display.width', 1000)
        pandas.set_option('max_columns', 1000)

    def test1(self):
        quote_ctx = OpenQuoteContext(host='127.0.0.1',port=11113)
        ret_code, ret_data = quote_ctx.get_stock_basicinfo(market=Market.HK, stock_type=SecurityType.STOCK,code_list=None)
        codes = ret_data['code'].tolist()

        for i in range(2):
            flag = True
            t = time.time() #控制while循环执行的时长:30s
            times = 0   #30秒内成功请求次数
            while flag:
                print(times)
                ret_code ,ret_data = quote_ctx.get_market_snapshot(code_list = codes[:300])
                print(ret_data)
                if ret_code is RET_OK:
                    times += 1
                if time.time() > (t+30):
                    flag = False
            print('get_market_snapshot 第%d个30秒请求成功的次数：%d'%(i,times))
            time.sleep(30)
        quote_ctx.close()

        # for data in ret_data.iterrows():
        #     print(data)

    def test2(self):
        quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

        ret_code, ret_data = quote_ctx.get_market_snapshot(
            code_list=['US.AAPL181026C240000','HK.28100','HK.00700', 'US.AAPL', 'SZ.000700', 'HK.13597']) #, 'US.DIS180824C111000'
        quote_ctx.close()
        print(ret_code)
        print(ret_data)

if __name__ == '__main__':
    gms = GetMarketSnapshot()
    gms.test2()