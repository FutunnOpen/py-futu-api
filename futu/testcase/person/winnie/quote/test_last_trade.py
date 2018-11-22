from futu import *
import pandas
import logging

class StockQuoteTest(StockQuoteHandlerBase):
    def on_recv_rsp(self, rsp_str):
        # pwd_unlock = '123123'
        # trd_ctx = OpenHKTradeContext(host='127.0.0.1', port=11111)
        # print(trd_ctx.unlock_trade(pwd_unlock))
        # print(trd_ctx.place_order(price=1.0, qty=10, code="HK.01715", trd_side=TrdSide.BUY))
        ret_code, content = super(StockQuoteTest, self).on_recv_rsp(rsp_str)
        if ret_code != RET_OK:
            print("StockQuoteTest: error, msg: %s" % content)
            return RET_ERROR, content
        # 设置显示
        pandas.set_option('max_columns', 100)
        pandas.set_option('display.width', 1000)
        print("StockQuoteTest ", content)  # StockQuoteTest自己的处理逻辑

        return RET_OK, content


def test_get_quote():
    quote_ctx = OpenQuoteContext(host='172.18.10.58', port=11111)
    # 启动异步数据
    quote_ctx.start()
    # 设置监听
    handler = StockQuoteTest()
    quote_ctx.set_handler(handler)
    # 订阅
    # quote_ctx.subscribe(['HK.01810'], SubType.QUOTE)
    quote_ctx.subscribe(['HK.00797'], SubType.QUOTE)
    # quote_ctx.subscribe(['HK.00700'], SubType.QUOTE)

    # 主动获取
    ret_code, ret_data = quote_ctx.get_stock_quote(['HK.00797'])
    print(ret_code)
    print(ret_data)
    # print(ret_data.columns.size)
    # print(ret_data.columns.tolist())


def test_get_market_snapshot():
    quote_ctx = OpenQuoteContext(host='172.18.10.58', port=11111)
    pandas.set_option('max_columns', 100)
    pandas.set_option('display.width', 1000)
    print(quote_ctx.get_market_snapshot('HK.00797'))
    quote_ctx.close()


if __name__ == '__main__':
    # test_get_quote()
    test_get_market_snapshot()

