from futu import *


def test_unlock():
    pwd_unlock = '123123'
    pwd_md5 = '13955235245b2497'
    trd_ctx = OpenHKTradeContext(host='127.0.0.1', port=11111)
    print(trd_ctx.unlock_trade(password='111', password_md5=pwd_md5))
    # print(trd_ctx.unlock_trade(pwd_unlock))
    # print(trd_ctx.place_order(price=700.0, qty=1, code="HK.00700", trd_side=TrdSide.SELL))
    trd_ctx.close()


if __name__ == '__main__':
    test_unlock()
