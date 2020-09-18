# -*- coding: utf-8 -*-
import talib
import math
import datetime
import logging
import futu as ft


class MACD(object):
    """
    A simple MACD strategy
    """
    # API parameter setting
    api_svr_ip = '127.0.0.1'  # 账户登录的牛牛客户端PC的IP, 本机默认为127.0.0.1
    api_svr_port = 11111  # 富途牛牛端口，默认为11111
    unlock_password = "123456"  # 美股和港股交易解锁密码
    trade_env = ft.TrdEnv.SIMULATE

    def __init__(self, stock, short_period, long_period, smooth_period,
                 observation):
        """
        Constructor
        """
        self.stock = stock
        self.short_period = short_period
        self.long_period = long_period
        self.smooth_period = smooth_period
        self.observation = observation
        self.quote_ctx, self.trade_ctx = self.context_setting()

    def close(self):
        self.quote_ctx.close()
        self.trade_ctx.close()

    def context_setting(self):
        """
        API trading and quote context setting
        :returns: trade context, quote context
        """
        if self.unlock_password == "":
            raise Exception("请先配置交易解锁密码! password: {}".format(
                self.unlock_password))

        quote_ctx = ft.OpenQuoteContext(
            host=self.api_svr_ip, port=self.api_svr_port)

        if 'HK.' in self.stock:
            trade_ctx = ft.OpenHKTradeContext(host=self.api_svr_ip, port=self.api_svr_port)
        elif 'US.' in self.stock:
            trade_ctx = ft.OpenUSTradeContext(host=self.api_svr_ip, port=self.api_svr_port)
        else:
            raise Exception("不支持的stock: {}".format(self.stock))

        if self.trade_env == ft.TrdEnv.REAL:
            ret_code, ret_data = trade_ctx.unlock_trade(
                self.unlock_password)
            if ret_code == ft.RET_OK:
                print('解锁交易成功!')
            else:
                raise Exception("请求交易解锁失败: {}".format(ret_data))
        else:
            print('解锁交易成功!')

        return quote_ctx, trade_ctx

    def handle_data(self):
        """
        handle stock data for trading signal, and make order
        """
        # 读取历史数据，使用sma方式计算均线准确度和数据长度无关，但是在使用ema方式计算均线时建议将历史数据窗口适当放大，结果会更加准确
        today = datetime.datetime.today()
        pre_day = (today - datetime.timedelta(days=self.observation)
                   ).strftime('%Y-%m-%d')
        end_dt = today.strftime('%Y-%m-%d')
        ret_code, prices, page_req_key = self.quote_ctx.request_history_kline(self.stock, start=pre_day, end=end_dt)
        if ret_code != ft.RET_OK:
            print("request_history_kline fail: {}".format(prices))
            return

        # 用talib计算MACD取值，得到三个时间序列数组，分别为 macd, signal 和 hist
        # macd 是长短均线的差值，signal 是 macd 的均线
        # 使用 macd 策略有几种不同的方法，我们这里采用 macd 线突破 signal 线的判断方法
        macd, signal, hist = talib.MACD(prices['close'].values,
                                        self.short_period, self.long_period,
                                        self.smooth_period)

        # 如果macd从上往下跌破macd_signal
        if macd[-1] < signal[-1] and macd[-2] > signal[-2]:
            # 计算现在portfolio中股票的仓位
            ret_code, data = self.trade_ctx.position_list_query(
                trd_env=self.trade_env)

            if ret_code != ft.RET_OK:
                raise Exception('账户信息获取失败: {}'.format(data))
            pos_info = data.set_index('code')

            cur_pos = int(pos_info['qty'][self.stock])
            # 进行清仓
            if cur_pos > 0:
                ret_code, data = self.quote_ctx.get_market_snapshot(
                    [self.stock])
                if ret_code != 0:
                    raise Exception('市场快照数据获取异常 {}'.format(data))
                cur_price = data['last_price'][0]
                ret_code, ret_data = self.trade_ctx.place_order(
                    price=cur_price,
                    qty=cur_pos,
                    code=self.stock,
                    trd_side=ft.TrdSide.SELL,
                    order_type=ft.OrderType.NORMAL,
                    trd_env=self.trade_env)
                if ret_code == ft.RET_OK:
                    print('stop_loss MAKE SELL ORDER\n\tcode = {} price = {} quantity = {}'
                          .format(self.stock, cur_price, cur_pos))
                else:
                    print('stop_loss: MAKE SELL ORDER FAILURE: {}'.format(ret_data))

        # 如果短均线从下往上突破长均线，为入场信号
        if macd[-1] > signal[-1] and macd[-2] < signal[-2]:
            # 满仓入股
            ret_code, acc_info = self.trade_ctx.accinfo_query(
                trd_env=self.trade_env)
            if ret_code != 0:
                raise Exception('账户信息获取失败! 请重试: {}'.format(acc_info))

            ret_code, snapshot = self.quote_ctx.get_market_snapshot(
                [self.stock])
            if ret_code != 0:
                raise Exception('市场快照数据获取异常 {}'.format(snapshot))
            lot_size = snapshot['lot_size'][0]
            cur_price = snapshot['last_price'][0]
            cash = acc_info['power'][0]  # 购买力
            qty = int(math.floor(cash / cur_price))
            qty = qty // lot_size * lot_size

            ret_code, ret_data = self.trade_ctx.place_order(
                price=cur_price,
                qty=qty,
                code=self.stock,
                trd_side=ft.TrdSide.BUY,
                order_type=ft.OrderType.NORMAL,
                trd_env=self.trade_env)
            if not ret_code:
                print(
                    'stop_loss MAKE BUY ORDER\n\tcode = {} price = {} quantity = {}'
                    .format(self.stock, cur_price, qty))
            else:
                print('stop_loss: MAKE BUY ORDER FAILURE: {}'.format(ret_data))


if __name__ == "__main__":
    SHORT_PERIOD = 12
    LONG_PERIOD = 26
    SMOOTH_PERIOD = 9
    OBSERVATION = 100

    STOCK = "HK.00123"

    test = MACD(STOCK, SHORT_PERIOD, LONG_PERIOD, SMOOTH_PERIOD, OBSERVATION)
    test.handle_data()
    test.close()
