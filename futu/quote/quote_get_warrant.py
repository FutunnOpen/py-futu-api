# -*- coding: utf-8 -*-
"""
    Market quote and trade context setting
"""
from futu import *
from futu.common.conn_mng import *
from futu.common.utils import *

class Request(object):

    def __init__(self):
        self.begin = 0  # 数据起始点
        self.num = 200  # 请求数据个数，最大200
        self.sort_field = SortField.CODE  # 根据哪个字段排序
        self.ascend = True  # 升序ture, 降序false
        self.stock_owner = None  # 所属正股
        self.type_list = list()   # Qot_Common.WarrantType, 窝轮类型过滤列表 WrtType
        self.issuer_list = list()  # Qot_Common.Issuer, 发行人过滤列表
        self.maturity_time_min = None # 到期日, 到期日范围的开始时间戳
        self.maturity_time_max = None # 到期日范围的结束时间戳
        self.ipo_period = None  # 上市日
        self.price_type = None  # Qot_Common.PriceType, 价内 / 价外
        self.status = None  # Qot_Common.WarrantStatus, 窝轮状态
        self.cur_price_min = None  # 最新价过滤起点
        self.cur_price_max = None  # 最新价过滤终点
        self.strike_price_min = None  # 行使价过滤起点
        self.strike_price_max = None  # 行使价过滤终点
        self.street_min = None  # 街货占比 % 过滤起点
        self.street_max = None  # 街货占比 % 过滤终点
        self.conversion_min = None  # 换股比率过滤起点
        self.conversion_max = None  # 换股比率过滤终点
        self.vol_min = None  # 成交量过滤起点
        self.vol_max = None  # 成交量过滤终点
        self.premium_min = None  # 溢价 % 过滤起点
        self.premium_max = None  # 溢价 % 过滤终点
        self.leverage_ratio_min = None  # 杠杆比率过滤起点
        self.leverage_ratio_max = None  # 杠杆比率过滤终点
        self.delta_min = None   # 对冲值过滤起点, 仅认购认沽支持该字段过滤
        self.delta_max = None  # 对冲值过滤终点, 仅认购认沽支持该字段过滤
        self.implied_min = None  # 引伸波幅过滤起点, 仅认购认沽支持该字段过滤
        self.implied_max = None  # 引伸波幅过滤终点, 仅认购认沽支持该字段过滤
        self.recovery_price_min = None  # 回收价过滤起点, 仅牛熊证支持该字段过滤
        self.recovery_price_max = None  # 回收价过滤终点, 仅牛熊证支持该字段过滤
        self.price_recovery_ratio_min = None  # 正股距回收价 % 过滤起点, 仅牛熊证支持该字段过滤
        self.price_recovery_ratio_max = None  # 正股距回收价 % 过滤终点, 仅牛熊证支持该字段过滤

    def fill_request_pb(self):
        from futu.common.pb.Qot_GetWarrant_pb2 import Request as GetWarrantPBRequest
        pb = GetWarrantPBRequest()
        pb.c2s.begin = self.begin
        pb.c2s.num = self.num

        r, v = SortField.to_number(self.sort_field)
        if not r:
            return RET_ERROR, 'sort_field is wrong. must be SortField'
        pb.c2s.sortField = v

        if type(self.ascend) != bool:
            return RET_ERROR, 'ascend is wrong. must be bool'

        pb.c2s.ascend = self.ascend
        if self.stock_owner is not None and len(self.stock_owner) != 0:
            """所属正股"""
            ret, content = split_stock_str(self.stock_owner)
            if ret == RET_ERROR:
                error_str = content
                return RET_ERROR, error_str
            market_code, stock_code = content
            pb.c2s.owner.market = market_code
            pb.c2s.owner.code = stock_code

        if self.type_list is not None and not isinstance(self.type_list, list):
            # 1120400921001028867
            self.type_list = [self.type_list]
        if self.issuer_list is not None and not isinstance(self.issuer_list, list):
            # 1120400921001028867
            self.issuer_list = [self.issuer_list]

        if self.type_list is not None and len(self.type_list) != 0:
            """Qot_Common.WarrantType,窝轮类型过滤列表"""
            for t in self.type_list:
                r, v = WrtType.to_number(t)
                if not r:
                    return RET_ERROR, 'type_list is wrong. must be [WrtType]'
                pb.c2s.typeList.append(v)
        if self.issuer_list is not None and len(self.issuer_list) != 0:
            """Qot_Common.Issuer,发行人过滤列表"""
            for t in self.issuer_list:
                r, v = Issuer.to_number(t)
                if not r:
                    return RET_ERROR, 'issuer_list is wrong. must be [Issuer]'
                pb.c2s.issuerList.append(v)

        if self.maturity_time_min is not None:
            """到期日, 到期日范围的开始时间戳"""
            if not isinstance(self.maturity_time_min, str) or len(self.maturity_time_min) == 0:
                return RET_ERROR, 'maturity_time_min is wrong. must be str. eg:2018-02-05'
            pb.c2s.maturityTimeMin = self.maturity_time_min

        if self.maturity_time_max is not None and len(self.maturity_time_max) != 0:
            """到期日范围的结束时间戳"""
            if not isinstance(self.maturity_time_max, str) or len(self.maturity_time_max) == 0:
                return RET_ERROR, 'maturity_time_max is wrong. must be str. eg:2018-02-10'
            pb.c2s.maturityTimeMax = self.maturity_time_max

        if self.ipo_period is not None:
            """上市日"""
            r, v = IpoPeriod.to_number(self.ipo_period)
            if not r:
                return RET_ERROR, 'ipo_period is wrong. must be IpoPeriod'
            pb.c2s.ipoPeriod = v
        if self.price_type is not None:
            """价内/价外"""
            r, v = PriceType.to_number(self.price_type)
            if not r:
                return RET_ERROR, 'price_type is wrong. must be PriceType'
            pb.c2s.priceType = v
        if self.status is not None:
            """窝轮状态"""
            r, v = WarrantStatus.to_number(self.status)
            if not r:
                return RET_ERROR, 'status is wrong. must be WarrantStatus'
            pb.c2s.status = v
        if self.cur_price_min is not None:
            """最新价过滤起点"""
            pb.c2s.curPriceMin = self.cur_price_min
        if self.cur_price_max is not None:
            """最新价过滤终点"""
            pb.c2s.curPriceMax = self.cur_price_max
        if self.strike_price_min is not None:
            """行使价过滤起点"""
            pb.c2s.strikePriceMin = self.strike_price_min
        if self.strike_price_max is not None:
            """行使价过滤终点 """
            pb.c2s.strikePriceMax = self.strike_price_max
        if self.street_min is not None:
            """街货占比%过滤起点"""
            pb.c2s.streetMin = self.street_min
        if self.street_max is not None:
            """街货占比%过滤终点"""
            pb.c2s.streetMax = self.street_max
        if self.conversion_min is not None:
            """换股比率过滤起点"""
            pb.c2s.conversionMin = self.conversion_min
        if self.conversion_max is not None:
            """换股比率过滤终点"""
            pb.c2s.conversionMax = self.conversion_max
        if self.vol_min is not None and self.vol_min != -1:
            """成交量过滤起点"""
            pb.c2s.volMin = self.vol_min
        if self.vol_max is not None and self.vol_max != -1:
            """成交量过滤终点"""
            pb.c2s.volMax = self.vol_max
        if self.premium_min is not None:
            """溢价 % 过滤起点"""
            pb.c2s.premiumMin = self.premium_min
        if self.premium_max is not None:
            """溢价 % 过滤终点"""
            pb.c2s.premiumMax = self.premium_max
        if self.leverage_ratio_min is not None:
            """杠杆比率过滤起点"""
            pb.c2s.leverageRatioMin = self.leverage_ratio_min
        if self.leverage_ratio_max is not None:
            """杠杆比率过滤终点"""
            pb.c2s.leverageRatioMax = self.leverage_ratio_max
        if self.delta_min is not None:
            """对冲值过滤起点, 仅认购认沽支持该字段过滤"""
            pb.c2s.deltaMin = self.delta_min
        if self.delta_max is not None:
            """对冲值过滤起点, 仅认购认沽支持该字段过滤"""
            pb.c2s.deltaMax = self.delta_max
        if self.implied_min is not None:
            """引伸波幅过滤起点,仅认购认沽支持该字段过滤"""
            pb.c2s.impliedMin = self.implied_min
        if self.implied_max is not None:
            """引伸波幅过滤终点,仅认购认沽支持该字段过滤"""
            pb.c2s.impliedMax = self.implied_max
        if self.recovery_price_min is not None:
            """回收价过滤起点,仅牛熊证支持该字段过滤"""
            pb.c2s.recoveryPriceMin = self.recovery_price_min
        if self.recovery_price_max is not None:
            """回收价过滤终点,仅牛熊证支持该字段过滤"""
            pb.c2s.recoveryPriceMax = self.recovery_price_max
        if self.price_recovery_ratio_min is not None:
            """正股距回收价%过滤起点,仅牛熊证支持该字段过滤"""
            pb.c2s.priceRecoveryRatioMin = self.price_recovery_ratio_min
        if self.price_recovery_ratio_max is not None:
            """正股距回收价%过滤终点,仅牛熊证支持该字段过滤"""
            pb.c2s.priceRecoveryRatioMax = self.price_recovery_ratio_max

        return RET_OK, pb


class Response(object):

    @staticmethod
    def unpack_response_pb(resp):
        from futu.common.pb.Qot_GetWarrant_pb2 import Response as GetWarrantPBResponse
        if resp is None or not isinstance(resp, GetWarrantPBResponse):
            return RET_ERROR, "unpack_response_pb error", None
        if resp.retType != RET_OK:
            return RET_ERROR, resp.retMsg, None

        warrant_data_list = list()

        for item in resp.s2c.warrantDataList:
            warrant = dict()
            warrant["stock"] = merge_qot_mkt_stock_str(
                int(item.stock.market), item.stock.code)  # 股票
            warrant["stock_owner"] = merge_qot_mkt_stock_str(
                int(item.owner.market), item.owner.code)  # 所属正股
            warrant["type"] = WrtType.to_string2(item.type)  # 窝轮类型
            warrant["issuer"] = Issuer.to_string2(item.issuer)  # 发行人
            warrant["maturity_time"] = item.maturityTime  # 到期日
            if item.HasField("maturityTimestamp"):
                """到期日时间戳"""
                warrant["maturity_timestamp"] = item.maturityTimestamp
            if item.HasField("listTime"):
                """上市时间"""
                warrant["list_time"] = item.listTime
            if item.HasField("listTimestamp"):
                """上市时间戳"""
                warrant["list_timestamp"] = item.listTimestamp
            if item.HasField("lastTradeTime"):
                """最后交易日"""
                warrant["last_trade_time"] = item.lastTradeTime
            if item.HasField("lastTradeTimestamp"):
                """最后交易日时间戳"""
                warrant["last_trade_timestamp"] = item.lastTradeTimestamp
            if item.HasField("recoveryPrice"):
                """回收价,仅牛熊证支持该字段"""
                warrant["recovery_price"] = item.recoveryPrice
            if item.HasField("conversionRatio"):
                """换股比率"""
                warrant["conversion_ratio"] = item.conversionRatio
            if item.HasField("lotSize"):
                """每手数量"""
                warrant["lot_size"] = item.lotSize
            if item.HasField("strikePrice"):
                """行使价"""
                warrant["strike_price"] = item.strikePrice
            if item.HasField("lastClosePrice"):
                """昨收价"""
                warrant["last_close_price"] = item.lastClosePrice
            if item.HasField("curPrice"):
                """当前价"""
                warrant["cur_price"] = item.curPrice
            if item.HasField("priceChangeVal"):
                """涨跌额"""
                warrant["price_change_val"] = item.priceChangeVal
            if item.HasField("changeRate"):
                """涨跌幅%"""
                warrant["change_rate"] = item.changeRate
            if item.HasField("status"):
                """窝轮状态"""
                warrant["status"] = WarrantStatus.to_string2(item.status)
            if item.HasField("bidPrice"):
                """买入价"""
                warrant["bid_price"] = item.bidPrice
            if item.HasField("askPrice"):
                """卖出价"""
                warrant["ask_price"] = item.askPrice
            if item.HasField("bidVol"):
                """买量"""
                warrant["bid_vol"] = item.bidVol
            if item.HasField("askVol"):
                """卖量"""
                warrant["ask_vol"] = item.askVol
            if item.HasField("volume"):
                """成交量"""
                warrant["volume"] = item.volume
            if item.HasField("turnover"):
                """成交额"""
                warrant["turnover"] = item.turnover
            if item.HasField("score"):
                """综合评分"""
                warrant["score"] = item.score
            if item.HasField("premium"):
                """溢价%"""
                warrant["premium"] = item.premium
            if item.HasField("breakEvenPoint"):
                """打和点"""
                warrant["break_even_point"] = item.breakEvenPoint
            if item.HasField("leverage"):
                """杠杠比率"""
                warrant["leverage"] = item.leverage
            if item.HasField("ipop"):
                """价内/价外%"""
                warrant["ipop"] = item.ipop
            if item.HasField("priceRecoveryRatio"):
                """正股距回收价%，仅牛熊证支持该字段"""
                warrant["price_recovery_ratio"] = item.priceRecoveryRatio
            if item.HasField("conversionPrice"):
                """换股价"""
                warrant["conversion_price"] = item.conversionPrice
            if item.HasField("streetRate"):
                """街货占比"""
                warrant["street_rate"] = item.streetRate
            if item.HasField("streetVol"):
                """街货量"""
                warrant["street_vol"] = item.streetVol
            if item.HasField("amplitude"):
                """振幅%"""
                warrant["amplitude"] = item.amplitude
            if item.HasField("name"):
                """name"""
                warrant["name"] = item.name
            if item.HasField("issueSize"):
                """发行量"""
                warrant["issue_size"] = item.issueSize
            if item.HasField("highPrice"):
                """最高价"""
                warrant["high_price"] = item.highPrice
            if item.HasField("lowPrice"):
                """最低价"""
                warrant["low_price"] = item.lowPrice
            if item.HasField("impliedVolatility"):
                """引申波幅,仅认购认沽支持该字段"""
                warrant["implied_volatility"] = item.impliedVolatility
            if item.HasField("delta"):
                """对冲值,仅认购认沽支持该字段"""
                warrant["delta"] = item.delta
            if item.HasField("effectiveLeverage"):
                """有效杠杆"""
                warrant["effective_leverage"] = item.effectiveLeverage
            if item.HasField("upperStrikePrice"):
                """上限价，仅界内证支持该字段"""
                warrant["upper_strike_price"] = item.upperStrikePrice
            if item.HasField("lowerStrikePrice"):
                """下限价，仅界内证支持该字段"""
                warrant["lower_strike_price"] = item.lowerStrikePrice
            if item.HasField("inLinePriceStatus"):
                """界内界外，仅界内证支持该字段"""
                warrant["inline_price_status"] = PriceType.to_string2(
                    item.inLinePriceStatus)
            warrant_data_list.append(warrant)
        return RET_OK, "", (warrant_data_list, resp.s2c.lastPage, resp.s2c.allCount)


if __name__ == "__main__":
    req = Request()
    req.type_list.append(WrtType.BUY)
    req.fill_request_pb()
