# -*- coding:utf-8 -*-
from futuquant import *
import pandas
import time

f = open('request_data.txt','a')
class TestMuchLanguage():
    # 行情：使用正式环境二级用户900019测试
    # 交易：使用测试环境账户100068测试
    def __init__(self):
        pandas.set_option('max_columns', 100)
        pandas.set_option('display.width', 1000)
        self.quote_ctx = OpenQuoteContext('127.0.0.1',11115)
        # self.quote_ctx2 = OpenQuoteContext('127.0.0.1', 11122)
        # self.quote_ctx3 = OpenQuoteContext('127.0.0.1', 11123)
        self.trade_ctx_hk = OpenHKTradeContext('127.0.0.1',11115)
        # self.trade_ctx_us = OpenUSTradeContext('127.0.0.1',11111)

    # def test(self):
    #     ret_code, ret_data = self.quote_ctx1.get_stock_basicinfo(Market.HK, SecurityType.STOCK)
    #     code_list = list(ret_data['code'])
    #     code_list1 = code_list[100:1300]
    #     code_list2 = code_list[1302:1700]
    #     code_list3 = code_list[1702:1900]
    #     print(len(code_list1),code_list1)
    #     print(len(code_list2),code_list2)
    #     print(len(code_list3),code_list3)
        # print('LV1:',file=f,flush=True)
        # for i in range(len(code_list1)):
        #     if i != 0 and i % 10 == 0:
        #         time.sleep(30)
        #     ret_code, result, page = self.quote_ctx1.request_history_kline(code_list1[i],max_count=1)
        #     print(i)
        #     print(result)
        #     print(i,file=f,flush=True)
        #     print(result,file=f,flush=True)
        #     if ret_code is RET_ERROR:
        #         print(result, file=f, flush=True)
        #         break
        # print('LV2:', file=f, flush=True)
        # i = 0
        # for i in range(len(code_list2)):
        #     if i != 0 and i % 10 == 0:
        #         time.sleep(30)
        #     ret_code, result, page = self.quote_ctx2.request_history_kline(code_list2[i],max_count=1)
        #     print(i)
        #     print(result)
        #     # print(i, file=f, flush=True)
        #     # print(result, file=f, flush=True)
        #     if ret_code is RET_ERROR:
        #         print(result)
        #         break
        # print('LV3:', file=f, flush=True)
        # i = 0
        # for i in range(len(code_list3)):
        #     if i != 0 and i % 10 == 0:
        #         time.sleep(30)
        #     ret_code, result, page = self.quote_ctx3.request_history_kline(code_list3[i],max_count=1)
        #     print(i)
        #     print(result)
        #     # print(i, file=f, flush=True)
        #     # print(result, file=f, flush=True)
        #     if ret_code is RET_ERROR:
        #         print(result, file=f, flush=True)
        #         break

    def test_quote(self):
        print(self.quote_ctx.request_history_kline('HK.00700', max_count=1))
        # 1、订阅不足1分钟
        self.quote_ctx.subscribe('HK.00700',SubType.ORDER_BOOK)
        print(self.quote_ctx.unsubscribe('HK.00700',SubType.ORDER_BOOK))
        # 2、未订阅该行情
        print(self.quote_ctx.get_rt_ticker('HK.00700',100))
        # 3、未知的股票
        print(self.quote_ctx.subscribe('HK.00', SubType.BROKER))
        self.quote_ctx.get_broker_queue('HK.00')
        # 4、请求股票个数超过限制get_owner_plate
        ret_code, ret_data = self.quote_ctx.get_stock_basicinfo(Market.HK, SecurityType.STOCK)
        code_list = list(ret_data['code'])
        code_list = code_list[311:520]
        print(len(code_list))
        self.quote_ctx.subscribe(code_list,SubType.K_1M)
        print(self.quote_ctx.get_owner_plate(code_list))
        # 5、本地数据库不存在
        print(self.quote_ctx.get_history_kline('HK.00700',start='2017-06-20',end='2017-07-12'))
        # 6、未知的K线类型
        print(self.quote_ctx.subscribe('HK.00700','1M'))
        # 7、时间字符串格式错误
        print(self.quote_ctx.get_trading_days(Market.HK, start='2018/02/01',end='2018/02/12'))
        # 8、时间段超过限制
        print(self.quote_ctx.get_option_chain('US.AAPL',start='2019-01-05',end='2019-06-14'))
        # 9、订阅额度不足
        ret_code, ret_data = self.quote_ctx.get_stock_basicinfo(Market.HK, SecurityType.STOCK)
        code_list = list(ret_data['code'])
        # del code_list[0:310]
        # del code_list[630:]
        code_list = code_list[311:630]
        print(code_list)
        print(len(code_list))
        print(self.quote_ctx.subscribe(code_list, SubType.ORDER_BOOK))
        # # 10、分页请求key错误
        print(self.quote_ctx.request_history_kline('HK.00700',page_req_key=16))
        # 11、历史下载额度不足
        for i in range(len(code_list)):
            if i != 0 and i % 10 == 0:
                time.sleep(30)
            ret_code, result, page = self.quote_ctx.request_history_kline(code_list[i],max_count=1)
            print(i)
            print(result)
            if ret_code is RET_ERROR:
                print(result)
                break
        # 12、缺少必要参数
        # print(self.quote_ctx.subscribe())
        # 13、未知的股票类型
        print(self.quote_ctx.get_stock_basicinfo(Market.HK, "warr"))
        # 14、


    def test_trade(self):
        pwd = '321321'
        # 1、未解锁
        self.trade_ctx_hk.unlock_trade(is_unlock=False)
        print(self.trade_ctx_hk.accinfo_query())
        # 2、已经是锁定状态
        print(self.trade_ctx_hk.unlock_trade(is_unlock=False))
        print(self.trade_ctx_hk.unlock_trade(is_unlock=False))
        # 3、已经是解锁状态
        print(self.trade_ctx_hk.unlock_trade(password='3d186804534370c3c817db0563f0e461', password_md5='3d186804534370c3c817db0563f0e461'))
        print(self.trade_ctx_hk.unlock_trade(password=pwd, password_md5='3d186804534370c3c817db0563f0e461'))
        # 4、数量不合法
        print(self.trade_ctx_hk.place_order(200,0.1, 'HK.00700',trd_side=TrdSide.BUY))
        # 5、交易方向只能是买或卖
        print(self.trade_ctx_hk.place_order(200,1,'HK.00700',trd_side=TrdSide.BUY_BACK))
        # 6、模拟交易不支持A股通市场
        trade_ctx_hkcc = OpenHKCCTradeContext('127.0.0.1',11111)
        print(trade_ctx_hkcc.place_order(4.61,200,'SH.600287',trd_side=TrdSide.BUY,trd_env=TrdEnv.SIMULATE))
        # 7、模拟交易不支持修改所有的订单
        # self.trade_ctx_hk.place_order()
        # 8、订单号不存在
        print(self.trade_ctx_hk.modify_order(ModifyOrderOp.NORMAL,'12345',1,1))
        # 9、业务账号不存在
        print(self.trade_ctx_hk.position_list_query(acc_id=12345))
        # 10、不支持的订单类型
        print(self.trade_ctx_hk.place_order(200,100, 'HK.00700',order_type=OrderType.MARKET,trd_side=TrdSide.BUY))
        # 11、模拟交易不支持成交数据
        print(self.trade_ctx_hk.deal_list_query(trd_env=TrdEnv.SIMULATE))


if __name__ == '__main__':
    tml = TestMuchLanguage()
    # tml.test()
    # tml.test_quote()
    tml.test_trade()

