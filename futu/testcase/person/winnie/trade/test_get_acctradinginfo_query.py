from futuquant import *
import pandas


def test_acctradinginfo_query():
    pwd_unlock = '123123'
    trd_ctx = OpenHKTradeContext(host='127.0.0.1', port=11111)
    trd_us = OpenUSTradeContext(host='127.0.0.1', port=11111)
    print(trd_ctx.unlock_trade(pwd_unlock))
    pandas.set_option('max_columns', 100)
    pandas.set_option('display.width', 1000)
    print(trd_ctx.get_acc_list())
    # print(trd_ctx.accinfo_query(acc_id=281756455982434220))  # 0
    # print(trd_ctx.accinfo_query(acc_id=281756457982434020))  # 1
    # print(trd_ctx.accinfo_query(acc_id=281756455982434020))  # 2

    # 港股竞价单
    print(trd_ctx.acctradinginfo_query(order_type=OrderType.AUCTION, code='01918', price=28.02,
                                      order_id=0, adjust_limit=0, acc_id=281756457982434020, trd_env=TrdEnv.REAL))
    # 美股市价单
    # print('US', trd_us.acctradinginfo_query(order_type=OrderType.MARKET, code='US.AAPL', price=2.00,
    #                                         order_id=0, adjust_limit=0, acc_id=281756457982434020,
    #                                         trd_env=TrdEnv.REAL))
    # # 港股限价单
    # print(trd_ctx.acctradinginfo_query(order_type=OrderType.ABSOLUTE_LIMIT, code='01918', price=28.02,
    #                                    order_id=0, adjust_limit=0, acc_id=0, trd_env=TrdEnv.REAL))
    # # 港股竞价限价单
    # print(trd_ctx.acctradinginfo_query(order_type=OrderType.AUCTION_LIMIT, code='01918', price=28.02,
    #                                    order_id=0, adjust_limit=0, acc_id=0, trd_env=TrdEnv.REAL))
    # 港股特别限价
    # print(trd_ctx.acctradinginfo_query(order_type=OrderType.SPECIAL_LIMIT, code='01918', price=28.02,
    #                                    order_id=0, adjust_limit=0, acc_id=0, trd_env=TrdEnv.REAL))
    trd_ctx.close()


if __name__ == '__main__':
    test_acctradinginfo_query()
