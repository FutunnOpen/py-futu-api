# -*- coding: utf-8 -*-
"""
    Quote query
"""

from futu.common.utils import *
from futu.common.pb import Common_pb2
from futu.quote.quote_stockfilter_info import *
from futu.quote.quote_get_warrant import *

# 无数据时的值
NoneDataType = 'N/A'


def get_optional_from_pb(pb, field_name, conv=None):
    if pb.HasField(field_name):
        val = getattr(pb, field_name)
        if conv:
            val = conv(val)
        return val
    return NoneDataType


def set_item_from_pb(item, pb, field_map):
    for python_name, pb_name, is_required, conv in field_map:
        exist_val = item.get(python_name, None)
        if exist_val is not None and exist_val != NoneDataType:
            continue
        if is_required:
            val = getattr(pb, pb_name)
            if conv:
                val = conv(val)
            item[python_name] = val
        else:
            item[python_name] = get_optional_from_pb(pb, pb_name, conv)


def set_item_none(item, field_map):
    for row in field_map:
        exist_val = item.get(row[0], None)
        if exist_val is None or exist_val == NoneDataType:
            item[row[0]] = NoneDataType


def conv_pb_security_to_code(security):
    return merge_qot_mkt_stock_str(security.market, security.code)

def merge_pb_cnipoexdata_winningnumdata(winningnumdata):
    data = ''
    for item in winningnumdata:
        if data == '':
            data = item.winningName + ":" + item.winningInfo
        else:
            data = data + '\n' + item.winningName + ":" + item.winningInfo

    data = data.rstrip()
    return data


# python_name, pb_name, is_required, conv_func
pb_field_map_OptionBasicQotExData = [
    ('strike_price', 'strikePrice', True, None),
    ('contract_size', 'contractSizeFloat', True, None),
    ('open_interest', 'openInterest', True, None),
    ('implied_volatility', 'impliedVolatility', True, None),
    ('premium', 'premium', True, None),
    ('delta', 'delta', True, None),
    ('gamma', 'gamma', True, None),
    ('vega', 'vega', True, None),
    ('theta', 'theta', True, None),
    ('rho', 'rho', True, None),
    ('net_open_interest', 'netOpenInterest', False, None),
    ('expiry_date_distance', 'expiryDateDistance', False, None),
    ('contract_nominal_value', 'contractNominalValue', False, None),
    ('owner_lot_multiplier', 'ownerLotMultiplier', False, None),
    ('option_area_type', 'optionAreaType', False, OptionAreaType.to_string2),
    ('contract_multiplier', 'contractMultiplier', False, None),
    ('index_option_type', 'indexOptionType', False, IndexOptionType.to_string2),
]

pb_field_map_FutureBasicQotExData = [
    ('last_settle_price', 'lastSettlePrice', True, None),
    ('position', 'position', True, None),
    ('position_change', 'positionChange', True, None),
    ('expiry_date_distance', 'expiryDateDistance', False, None),
]

pb_field_map_PreAfterMarketData_pre = [
    ("pre_price", "price", False, None),
    ("pre_high_price", "highPrice", False, None),
    ("pre_low_price", "lowPrice", False, None),
    ("pre_volume", "volume", False, None),
    ("pre_turnover", "turnover", False, None),
    ("pre_change_val", "changeVal", False, None),
    ("pre_change_rate", "changeRate", False, None),
    ("pre_amplitude", "amplitude", False, None),
]

pb_field_map_PreAfterMarketData_after = [
    ("after_price", "price", False, None),
    ("after_high_price", "highPrice", False, None),
    ("after_low_price", "lowPrice", False, None),
    ("after_volume", "volume", False, None),
    ("after_turnover", "turnover", False, None),
    ("after_change_val", "changeVal", False, None),
    ("after_change_rate", "changeRate", False, None),
    ("after_amplitude", "amplitude", False, None),
]

pb_field_map_BasicIpoData = [
    ("code", "security", True, conv_pb_security_to_code),
    ("name", "name", True, None),
    ("list_time", "listTime", False, None),
    ("list_timestamp", "listTimestamp", False, None),
]

pb_field_map_CNIpoExData = [
    ("apply_code", "applyCode", True, None),
    ("issue_size", "issueSize", True, None),
    ("online_issue_size", "onlineIssueSize", True, None),
    ("apply_upper_limit", "applyUpperLimit", True, None),
    ("apply_limit_market_value", "applyLimitMarketValue", True, None),
    ("is_estimate_ipo_price", "isEstimateIpoPrice", True, None),
    ("ipo_price", "ipoPrice", True, None),
    ("industry_pe_rate", "industryPeRate", True, None),
    ("is_estimate_winning_ratio", "isEstimateWinningRatio", True, None),
    ("winning_ratio", "winningRatio", True, None),
    ("issue_pe_rate", "issuePeRate", True, None),
    ("apply_time", "applyTime", False, None),
    ("apply_timestamp", "applyTimestamp", False, None),
    ("winning_time", "winningTime", False, None),
    ("winning_timestamp", "winningTimestamp", False, None),
    ("is_has_won", "isHasWon", True, None),
    ("winning_num_data", "winningNumData", True, merge_pb_cnipoexdata_winningnumdata),
]

pb_field_map_HKIpoExData = [
    ("ipo_price_min", "ipoPriceMin", True, None),
    ("ipo_price_max", "ipoPriceMax", True, None),
    ("list_price", "listPrice", True, None),
    ("lot_size", "lotSize", True, None),
    ("entrance_price", "entrancePrice", True, None),
    ("is_subscribe_status", "isSubscribeStatus", True, None),
    ("apply_end_time", "applyEndTime", False, None),
    ("apply_end_timestamp", "applyEndTimestamp", False, None),
]

pb_field_map_USIpoExData = [
    ("ipo_price_min", "ipoPriceMin", True, None),
    ("ipo_price_max", "ipoPriceMax", True, None),
    ("issue_size", "issueSize", True, None)
]

class InitConnect:
    """
    A InitConnect request must be sent first
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, client_ver, client_id, recv_notify, is_encrypt, push_proto_fmt):

        from futu.common.pb.InitConnect_pb2 import Request
        req = Request()
        req.c2s.clientVer = client_ver
        req.c2s.clientID = client_id
        req.c2s.recvNotify = recv_notify
        req.c2s.pushProtoFmt = push_proto_fmt
        req.c2s.programmingLanguage = 'Python'

        if is_encrypt:
            req.c2s.packetEncAlgo = Common_pb2.PacketEncAlgo_AES_CBC
        else:
            req.c2s.packetEncAlgo = Common_pb2.PacketEncAlgo_None

        return pack_pb_req(req, ProtoId.InitConnect, 0)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        """Unpack the init connect response"""
        ret_type = rsp_pb.retType
        ret_msg = rsp_pb.retMsg

        if ret_type != RET_OK:
            return RET_ERROR, ret_msg, None

        res = {}
        if rsp_pb.HasField('s2c'):
            res['server_version'] = rsp_pb.s2c.serverVer
            res['login_user_id'] = rsp_pb.s2c.loginUserID
            res['conn_id'] = rsp_pb.s2c.connID
            res['conn_key'] = rsp_pb.s2c.connAESKey
            res['conn_iv'] = rsp_pb.s2c.aesCBCiv if rsp_pb.s2c.HasField('aesCBCiv') else None
            res['keep_alive_interval'] = rsp_pb.s2c.keepAliveInterval
        else:
            return RET_ERROR, "rsp_pb error", None

        return RET_OK, "", res


class TradeDayQuery:
    """
    Query Conversion for getting trading days.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, market, conn_id, start_date=None, end_date=None):

        # '''Parameter check'''
        r, mkt = Market.to_number(market)
        if not r:
            error_str = ERROR_STR_PREFIX + " market is %s, which is not valid. (%s)" \
                                           % (market, Market.get_all_keys())
            return RET_ERROR, error_str, None

        if start_date is None:
            today = datetime.today()
            start = today - timedelta(days=365)

            start_date = start.strftime("%Y-%m-%d")
        else:
            ret, msg = normalize_date_format(start_date)
            if ret != RET_OK:
                return ret, msg, None
            start_date = msg

        if end_date is None:
            today = datetime.today()
            end_date = today.strftime("%Y-%m-%d")
        else:
            ret, msg = normalize_date_format(end_date)
            if ret != RET_OK:
                return ret, msg, None
            end_date = msg

        # pack to json
        from futu.common.pb.Qot_GetTradeDate_pb2 import Request
        req = Request()
        req.c2s.market = mkt
        req.c2s.beginTime = start_date
        req.c2s.endTime = end_date

        return pack_pb_req(req, ProtoId.Qot_GetTradeDate, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):

        # response check and unpack response json to objects
        ret_type = rsp_pb.retType
        ret_msg = rsp_pb.retMsg

        if ret_type != RET_OK:
            return RET_ERROR, ret_msg, None

        raw_trading_day_list = rsp_pb.s2c.tradeDateList
        trading_day_list = list()

        for x in raw_trading_day_list:
            if x.time is not None and len(x.time) > 0:
                trading_day_list.append(
                    {"time": x.time, "trade_date_type": TradeDateType.to_string2(x.tradeDateType)})

        return RET_OK, "", trading_day_list

class RequestTradeDayQuery:
    """
    Query Conversion for getting trading days.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, market, conn_id, start_date=None, end_date=None):

        # '''Parameter check'''
        r, v = TradeDateMarket.to_number(market)
        if not r:
            error_str = ERROR_STR_PREFIX + " market is %s, which is not valid." \
                                           % (market)
            return RET_ERROR, error_str, None

        if start_date is None:
            today = datetime.today()
            start = today - timedelta(days=365)

            start_date = start.strftime("%Y-%m-%d")
        else:
            ret, msg = normalize_date_format(start_date)
            if ret != RET_OK:
                return ret, msg, None
            start_date = msg

        if end_date is None:
            today = datetime.today()
            end_date = today.strftime("%Y-%m-%d")
        else:
            ret, msg = normalize_date_format(end_date)
            if ret != RET_OK:
                return ret, msg, None
            end_date = msg

        # pack to json
        from futu.common.pb.Qot_RequestTradeDate_pb2 import Request
        req = Request()
        req.c2s.market = v
        req.c2s.beginTime = start_date
        req.c2s.endTime = end_date

        return pack_pb_req(req, ProtoId.Qot_RequestTradeDate, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):

        # response check and unpack response json to objects
        ret_type = rsp_pb.retType
        ret_msg = rsp_pb.retMsg

        if ret_type != RET_OK:
            return RET_ERROR, ret_msg, None

        raw_trading_day_list = rsp_pb.s2c.tradeDateList
        trading_day_list = list()

        for x in raw_trading_day_list:
            if x.time is not None and len(x.time) > 0:
                trading_day_list.append(
                    {"time": x.time, "trade_date_type": TradeDateType.to_string2(x.tradeDateType)})

        return RET_OK, "", trading_day_list

class StockBasicInfoQuery:
    """
    Query Conversion for getting stock basic information.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, market, conn_id, stock_type='STOCK', code_list=None):
        query_code = code_list is not None and len(code_list) > 0
        if not query_code:
            if not Market.if_has_key(market):
                error_str = ERROR_STR_PREFIX + " market is %s, which is not valid. (%s)" \
                                               % (market, Market.get_all_keys())
                return RET_ERROR, error_str, None

            if not SecurityType.if_has_key(stock_type) and code_list is None:
                error_str = ERROR_STR_PREFIX + " stock_type is %s, which is not valid. (%s)" \
                                               % (stock_type, SecurityType.get_all_keys())
                return RET_ERROR, error_str, None

        from futu.common.pb.Qot_GetStaticInfo_pb2 import Request
        req = Request()
        if query_code:
            req.c2s.market = 0
            req.c2s.secType = 0
            for code in code_list:
                sec = req.c2s.securityList.add()
                ret, data = split_stock_str(code)
                if ret == RET_OK:
                    sec.market, sec.code = data
                else:
                    return RET_ERROR, data, None
        else:
            _, req.c2s.market = Market.to_number(market)
            _, req.c2s.secType = SecurityType.to_number(stock_type)

        return pack_pb_req(req, ProtoId.Qot_GetStaticInfo, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):

        ret_type = rsp_pb.retType
        ret_msg = rsp_pb.retMsg

        if ret_type != RET_OK:
            return RET_ERROR, ret_msg, None

        raw_basic_info_list = rsp_pb.s2c.staticInfoList
        basic_info_list = [{
            "code": merge_qot_mkt_stock_str(record.basic.security.market,
                                            record.basic.security.code),
            "stock_id": record.basic.id,
            "name": record.basic.name,
            "lot_size": record.basic.lotSize,
            "stock_type": SecurityType.to_string2(record.basic.secType),
            "stock_child_type": WrtType.to_string2(record.warrantExData.type),
            "stock_owner":merge_qot_mkt_stock_str(
                record.warrantExData.owner.market,
                record.warrantExData.owner.code) if record.HasField('warrantExData') else (
                merge_qot_mkt_stock_str(
                    record.optionExData.owner.market,
                    record.optionExData.owner.code) if record.HasField('optionExData')
                else ""),
            "listing_date": "N/A" if record.HasField('optionExData') else record.basic.listTime,
            "option_type": OptionType.to_string2(record.optionExData.type) if record.HasField('optionExData') else "",
            "strike_time": record.optionExData.strikeTime,
            "strike_price": record.optionExData.strikePrice if record.HasField('optionExData') else NoneDataType,
            "suspension": record.optionExData.suspend if record.HasField('optionExData') else NoneDataType,
            "delisting": record.basic.delisting if record.basic.HasField('delisting') else NoneDataType,
            "index_option_type": IndexOptionType.to_string2(record.optionExData.indexOptionType) if record.HasField('optionExData') else NoneDataType,
            "main_contract": record.futureExData.isMainContract,
            "last_trade_time": record.futureExData.lastTradeTime,
        } for record in raw_basic_info_list]
        return RET_OK, "", basic_info_list


class MarketSnapshotQuery:
    """
    Query Conversion for getting market snapshot.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, stock_list, conn_id):
        """Convert from user request for trading days to PLS request"""
        stock_tuple_list = []
        failure_tuple_list = []
        for stock_str in stock_list:
            ret_code, content = split_stock_str(stock_str)
            if ret_code != RET_OK:
                error_str = content
                failure_tuple_list.append((ret_code, error_str))
                continue

            market_code, stock_code = content
            stock_tuple_list.append((market_code, stock_code))

        if len(failure_tuple_list) > 0:
            error_str = '\n'.join([x[1] for x in failure_tuple_list])
            return RET_ERROR, error_str, None

        from futu.common.pb.Qot_GetSecuritySnapshot_pb2 import Request
        req = Request()
        for market, code in stock_tuple_list:
            stock_inst = req.c2s.securityList.add()
            stock_inst.market = market
            stock_inst.code = code

        return pack_pb_req(req, ProtoId.Qot_GetSecuritySnapshot, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        """Convert from PLS response to user response"""
        ret_type = rsp_pb.retType
        ret_msg = rsp_pb.retMsg

        if ret_type != RET_OK:
            return RET_ERROR, ret_msg, None

        raw_snapshot_list = rsp_pb.s2c.snapshotList

        snapshot_list = []
        for record in raw_snapshot_list:
            snapshot_tmp = {}
            snapshot_tmp['code'] = merge_qot_mkt_stock_str(
                int(record.basic.security.market), record.basic.security.code)
            snapshot_tmp['update_time'] = record.basic.updateTime
            snapshot_tmp['last_price'] = record.basic.curPrice
            snapshot_tmp['open_price'] = record.basic.openPrice
            snapshot_tmp['high_price'] = record.basic.highPrice
            snapshot_tmp['low_price'] = record.basic.lowPrice
            snapshot_tmp['prev_close_price'] = record.basic.lastClosePrice
            snapshot_tmp['volume'] = record.basic.volume
            snapshot_tmp['turnover'] = record.basic.turnover
            snapshot_tmp['turnover_rate'] = record.basic.turnoverRate
            snapshot_tmp['suspension'] = record.basic.isSuspend
            snapshot_tmp['listing_date'] = "N/A" if record.HasField(
                'optionExData') else record.basic.listTime
            snapshot_tmp['price_spread'] = record.basic.priceSpread
            snapshot_tmp['lot_size'] = record.basic.lotSize
            snapshot_tmp['ask_price'] = record.basic.askPrice if record.basic.HasField('askPrice') else 'N/A'
            snapshot_tmp['bid_price'] = record.basic.bidPrice if record.basic.HasField('bidPrice') else 'N/A'
            snapshot_tmp['ask_vol'] = record.basic.askVol if record.basic.HasField('askVol') else 'N/A'
            snapshot_tmp['bid_vol'] = record.basic.bidVol if record.basic.HasField('bidVol') else 'N/A'

            # 窝轮 统一对枚举类型，初始化
            snapshot_tmp['wrt_type'] = WrtType.to_string2(
                record.warrantExData.warrantType) if record.warrantExData.HasField('warrantType') else 'N/A'
            #  界内界外，仅界内证支持该字段 type=double
            snapshot_tmp["wrt_inline_price_status"] = PriceType.to_string2(
                record.warrantExData.inLinePriceStatus) if record.warrantExData.HasField('inLinePriceStatus') else 'N/A'

            # 期权 统一对枚举类型，初始化
            snapshot_tmp['option_type'] = OptionType.to_string2(
                record.optionExData.type) if record.optionExData.HasField('type') else 'N/A'
            snapshot_tmp['index_option_type'] = IndexOptionType.to_string2(
                record.optionExData.indexOptionType) if record.optionExData.HasField('indexOptionType') else 'N/A'
            snapshot_tmp['option_area_type'] = OptionAreaType.to_string2(
                record.optionExData.optionAreaType) if record.optionExData.HasField('optionAreaType') else 'N/A'

            # 基金 统一对枚举类型，初始化
            snapshot_tmp['trust_assetClass'] = AssetClass.to_string2(record.trustExData.assetClass) if record.trustExData.HasField('assetClass') else 'N/A'

            # 2019.02.25 增加一批数据
            if record.basic.HasField("enableMargin"):
                # 是否可融资，如果为true，后两个字段才有意
                snapshot_tmp['enable_margin'] = record.basic.enableMargin
                if snapshot_tmp['enable_margin'] is True:
                    snapshot_tmp['mortgage_ratio'] = record.basic.mortgageRatio
                    snapshot_tmp['long_margin_initial_ratio'] = record.basic.longMarginInitialRatio
            if record.basic.HasField("enableShortSell"):
                # 是否可卖空，如果为true，后三个字段才有意义
                snapshot_tmp['enable_short_sell'] = record.basic.enableShortSell
                if snapshot_tmp['enable_short_sell'] is True:
                    snapshot_tmp['short_sell_rate'] = record.basic.shortSellRate
                    snapshot_tmp['short_available_volume'] = record.basic.shortAvailableVolume
                    snapshot_tmp['short_margin_initial_ratio'] = record.basic.shortMarginInitialRatio
            # 2019.05.10 增加一批数据================================
            #  振幅（该字段为百分比字段，默认不展示%） type=double
            snapshot_tmp["amplitude"] = record.basic.amplitude
            #  平均价 type=double
            snapshot_tmp["avg_price"] = record.basic.avgPrice
            #  委比（该字段为百分比字段，默认不展示%） type=double
            snapshot_tmp["bid_ask_ratio"] = record.basic.bidAskRatio
            #  量比 type=double
            snapshot_tmp["volume_ratio"] = record.basic.volumeRatio
            #  52周最高价 type=double
            snapshot_tmp["highest52weeks_price"] = record.basic.highest52WeeksPrice
            #  52周最低价 type=double
            snapshot_tmp["lowest52weeks_price"] = record.basic.lowest52WeeksPrice
            #  历史最高价 type=double
            snapshot_tmp["highest_history_price"] = record.basic.highestHistoryPrice
            #  历史最低价 type=double
            snapshot_tmp["lowest_history_price"] = record.basic.lowestHistoryPrice
            #  盘后成交量 type=int64
            snapshot_tmp["after_volume"] = record.basic.afterMarket.volume
            #  盘后成交额 type=double
            snapshot_tmp["after_turnover"] = record.basic.afterMarket.turnover   
            #  股票状态 type=str
            snapshot_tmp["sec_status"] = SecurityStatus.to_string2(record.basic.secStatus) if record.basic.HasField('secStatus') else 'N/A'
            #  5分组收盘价 type=double
            snapshot_tmp["close_price_5min"] = record.basic.closePrice5Minute

            if record.basic.HasField('preMarket'):
                set_item_from_pb(snapshot_tmp, record.basic.preMarket, pb_field_map_PreAfterMarketData_pre)
            else:
                set_item_none(snapshot_tmp, pb_field_map_PreAfterMarketData_pre)

            if record.basic.HasField('afterMarket'):
                set_item_from_pb(snapshot_tmp, record.basic.afterMarket, pb_field_map_PreAfterMarketData_after)
            else:
                set_item_none(snapshot_tmp, pb_field_map_PreAfterMarketData_after)
            # ================================

            snapshot_tmp['equity_valid'] = False
            # equityExData
            if record.HasField('equityExData'):
                snapshot_tmp['equity_valid'] = True
                snapshot_tmp['issued_shares'] = record.equityExData.issuedShares
                snapshot_tmp['total_market_val'] = record.equityExData.issuedMarketVal
                snapshot_tmp['net_asset'] = record.equityExData.netAsset
                snapshot_tmp['net_profit'] = record.equityExData.netProfit
                snapshot_tmp['earning_per_share'] = record.equityExData.earningsPershare
                snapshot_tmp['outstanding_shares'] = record.equityExData.outstandingShares
                snapshot_tmp['circular_market_val'] = record.equityExData.outstandingMarketVal
                snapshot_tmp['net_asset_per_share'] = record.equityExData.netAssetPershare
                snapshot_tmp['ey_ratio'] = record.equityExData.eyRate
                snapshot_tmp['pe_ratio'] = record.equityExData.peRate
                snapshot_tmp['pb_ratio'] = record.equityExData.pbRate
                snapshot_tmp['pe_ttm_ratio'] = record.equityExData.peTTMRate
                snapshot_tmp["dividend_ttm"] = record.equityExData.dividendTTM
                #  股息率TTM（该字段为百分比字段，默认不展示%） type=double
                snapshot_tmp["dividend_ratio_ttm"] = record.equityExData.dividendRatioTTM
                #  股息LFY，上一年度派息 type=double
                snapshot_tmp["dividend_lfy"] = record.equityExData.dividendLFY
                #  股息率LFY（该字段为百分比字段，默认不展示%） type=double
                snapshot_tmp["dividend_lfy_ratio"] = record.equityExData.dividendLFYRatio

            snapshot_tmp['wrt_valid'] = False
            if SecurityType.to_string2(record.basic.type) == SecurityType.WARRANT:
                snapshot_tmp['wrt_valid'] = True
                snapshot_tmp['wrt_conversion_ratio'] = record.warrantExData.conversionRate
                snapshot_tmp['wrt_strike_price'] = record.warrantExData.strikePrice
                snapshot_tmp['wrt_maturity_date'] = record.warrantExData.maturityTime
                snapshot_tmp['wrt_end_trade'] = record.warrantExData.endTradeTime
                snapshot_tmp['stock_owner'] = merge_qot_mkt_stock_str(
                    record.warrantExData.owner.market,
                    record.warrantExData.owner.code)
                snapshot_tmp['wrt_recovery_price'] = record.warrantExData.recoveryPrice
                snapshot_tmp['wrt_street_vol'] = record.warrantExData.streetVolumn
                snapshot_tmp['wrt_issue_vol'] = record.warrantExData.issueVolumn
                snapshot_tmp['wrt_street_ratio'] = record.warrantExData.streetRate
                snapshot_tmp['wrt_delta'] = record.warrantExData.delta
                snapshot_tmp['wrt_implied_volatility'] = record.warrantExData.impliedVolatility
                snapshot_tmp['wrt_premium'] = record.warrantExData.premium
                #  杠杆比率（倍） type=double
                snapshot_tmp["wrt_leverage"] = record.warrantExData.leverage
                #  价内/价外（该字段为百分比字段，默认不展示%） type=double
                snapshot_tmp["wrt_ipop"] = record.warrantExData.ipop
                #  打和点 type=double
                snapshot_tmp["wrt_break_even_point"] = record.warrantExData.breakEvenPoint
                #  换股价 type=double
                snapshot_tmp["wrt_conversion_price"] = record.warrantExData.conversionPrice
                #  距收回价（该字段为百分比字段，默认不展示%） type=double
                snapshot_tmp["wrt_price_recovery_ratio"] = record.warrantExData.priceRecoveryRatio
                #  综合评分 type=double
                snapshot_tmp["wrt_score"] = record.warrantExData.score
                #  上限价，仅界内证支持该字段 type=double
                snapshot_tmp["wrt_upper_strike_price"] = record.warrantExData.upperStrikePrice
                #  下限价，仅界内证支持该字段 type=double
                snapshot_tmp["wrt_lower_strike_price"] = record.warrantExData.lowerStrikePrice
                snapshot_tmp["wrt_issuer_code"] = record.warrantExData.issuerCode

            snapshot_tmp['option_valid'] = False
            if SecurityType.to_string2(record.basic.type) == SecurityType.DRVT:
                snapshot_tmp['option_valid'] = True

                snapshot_tmp['stock_owner'] = merge_qot_mkt_stock_str(
                    record.optionExData.owner.market, record.optionExData.owner.code)
                snapshot_tmp['strike_time'] = record.optionExData.strikeTime
                snapshot_tmp['option_strike_price'] = record.optionExData.strikePrice
                snapshot_tmp['option_contract_size'] = record.optionExData.contractSizeFloat
                snapshot_tmp['option_open_interest'] = record.optionExData.openInterest
                snapshot_tmp['option_implied_volatility'] = record.optionExData.impliedVolatility
                snapshot_tmp['option_premium'] = record.optionExData.premium
                snapshot_tmp['option_delta'] = record.optionExData.delta
                snapshot_tmp['option_gamma'] = record.optionExData.gamma
                snapshot_tmp['option_vega'] = record.optionExData.vega
                snapshot_tmp['option_theta'] = record.optionExData.theta
                snapshot_tmp['option_rho'] = record.optionExData.rho
                snapshot_tmp['option_net_open_interest'] = record.optionExData.netOpenInterest if record.optionExData.HasField('netOpenInterest') else 'N/A'
                snapshot_tmp['option_expiry_date_distance'] = record.optionExData.expiryDateDistance if record.optionExData.HasField('expiryDateDistance') else 'N/A'
                snapshot_tmp['option_contract_nominal_value'] = record.optionExData.contractNominalValue if record.optionExData.HasField('contractNominalValue') else 'N/A'
                snapshot_tmp['option_owner_lot_multiplier'] = record.optionExData.ownerLotMultiplier if record.optionExData.HasField('ownerLotMultiplier') else 'N/A'
                snapshot_tmp['option_contract_multiplier'] = record.optionExData.contractMultiplier if record.optionExData.HasField('contractMultiplier') else 'N/A'

            snapshot_tmp['index_valid'] = False
            if record.HasField('indexExData'):
                snapshot_tmp['index_valid'] = True
                #  指数类型上涨支数 type=int32
                snapshot_tmp["index_raise_count"] = record.indexExData.raiseCount
                #  指数类型下跌支数 type=int32
                snapshot_tmp["index_fall_count"] = record.indexExData.fallCount
                #  指数类型平盘支数 type=int32
                snapshot_tmp["index_equal_count"] = record.indexExData.equalCount

            snapshot_tmp['plate_valid'] = False
            if record.HasField('plateExData'):
                snapshot_tmp['plate_valid'] = True
                #  板块类型上涨支数 type=int32
                snapshot_tmp["plate_raise_count"] = record.plateExData.raiseCount
                #  板块类型下跌支数 type=int32
                snapshot_tmp["plate_fall_count"] = record.plateExData.fallCount
                #  板块类型平盘支数 type=int32
                snapshot_tmp["plate_equal_count"] = record.plateExData.equalCount

            snapshot_tmp['future_valid'] = False
            if SecurityType.to_string2(record.basic.type) == SecurityType.FUTURE:
                snapshot_tmp['future_valid'] = True
                snapshot_tmp['future_last_settle_price'] = record.futureExData.lastSettlePrice
                snapshot_tmp['future_position'] = record.futureExData.position
                snapshot_tmp['future_position_change'] = record.futureExData.positionChange
                snapshot_tmp['future_main_contract'] = record.futureExData.isMainContract
                snapshot_tmp['future_last_trade_time'] = record.futureExData.lastTradeTime

            snapshot_tmp['trust_valid'] = False
            if record.HasField('trustExData'):
                snapshot_tmp['trust_valid'] = True
                snapshot_tmp['trust_dividend_yield'] = record.trustExData.dividendYield
                snapshot_tmp['trust_aum'] = record.trustExData.aum
                snapshot_tmp['trust_outstanding_units'] = record.trustExData.outstandingUnits
                snapshot_tmp['trust_netAssetValue'] = record.trustExData.netAssetValue
                snapshot_tmp['trust_premium'] = record.trustExData.premium

            snapshot_list.append(snapshot_tmp)

        return RET_OK, "", snapshot_list


class RtDataQuery:
    """
    Query Conversion for getting stock real-time data.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, conn_id):

        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            error_str = content
            return RET_ERROR, error_str, None

        market_code, stock_code = content
        from futu.common.pb.Qot_GetRT_pb2 import Request
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code

        return pack_pb_req(req, ProtoId.Qot_GetRT, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):

        ret_type = rsp_pb.retType
        ret_msg = rsp_pb.retMsg

        if ret_type != RET_OK:
            return RET_ERROR, ret_msg, None

        raw_rt_data_list = rsp_pb.s2c.rtList
        rt_list = [
            {
                "code": merge_qot_mkt_stock_str(rsp_pb.s2c.security.market, rsp_pb.s2c.security.code),
                "time": record.time,
                "is_blank":  True if record.isBlank else False,
                "opened_mins": record.minute,
                "cur_price": record.price,
                "last_close": record.lastClosePrice,
                "avg_price": record.avgPrice if record.HasField('avgPrice') else None,
                "turnover": record.turnover,
                "volume": record.volume
            } for record in raw_rt_data_list
        ]
        return RET_OK, "", rt_list


class SubplateQuery:
    """
    Query Conversion for getting sub-plate stock list.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, market, plate_class, conn_id):

        from futu.common.pb.Qot_GetPlateSet_pb2 import Request
        req = Request()
        _, req.c2s.market = Market.to_number(market)
        _, req.c2s.plateSetType = Plate.to_number(plate_class)

        return pack_pb_req(req, ProtoId.Qot_GetPlateSet, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):

        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        raw_plate_list = rsp_pb.s2c.plateInfoList

        plate_list = [{
            "code": merge_qot_mkt_stock_str(record.plate.market, record.plate.code),
            "plate_name":
            record.name,
            "plate_id":
            record.plate.code
        } for record in raw_plate_list]

        return RET_OK, "", plate_list


class PlateStockQuery:
    """
    Query Conversion for getting all the stock list of a given plate.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, plate_code, sort_field, ascend, conn_id):

        ret_code, content = split_stock_str(plate_code)
        if ret_code != RET_OK:
            msg = content
            error_str = ERROR_STR_PREFIX + msg
            return RET_ERROR, error_str, None

        market, code = content
        r, v = SortField.to_number(sort_field)
        from futu.common.pb.Qot_GetPlateSecurity_pb2 import Request
        req = Request()
        req.c2s.plate.market = market
        req.c2s.plate.code = code
        req.c2s.sortField = v
        req.c2s.ascend = ascend
        return pack_pb_req(req, ProtoId.Qot_GetPlateSecurity, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):

        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        raw_stock_list = rsp_pb.s2c.staticInfoList

        stock_list = []
        for record in raw_stock_list:
            stock_tmp = {}
            stock_tmp['stock_id'] = record.basic.id
            stock_tmp['lot_size'] = record.basic.lotSize
            stock_tmp['code'] = merge_qot_mkt_stock_str(
                record.basic.security.market, record.basic.security.code)
            stock_tmp['stock_name'] = record.basic.name
            stock_tmp['list_time'] = record.basic.listTime
            stock_tmp['stock_type'] = SecurityType.to_string2(record.basic.secType)
            stock_tmp['main_contract'] = record.futureExData.isMainContract
            stock_tmp['last_trade_time'] = record.futureExData.lastTradeTime
            stock_list.append(stock_tmp)

        return RET_OK, "", stock_list


class BrokerQueueQuery:
    """
    Query Conversion for getting broker queue information.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, conn_id):

        ret_code, content = split_stock_str(code)
        if ret_code == RET_ERROR:
            error_str = content
            return RET_ERROR, error_str, None

        market, code = content
        from futu.common.pb.Qot_GetBroker_pb2 import Request
        req = Request()
        req.c2s.security.market = market
        req.c2s.security.code = code
        return pack_pb_req(req, ProtoId.Qot_GetBroker, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):

        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        stock_code = merge_qot_mkt_stock_str(rsp_pb.s2c.security.market,
                                             rsp_pb.s2c.security.code)

        raw_broker_bid = rsp_pb.s2c.brokerBidList
        bid_list = []
        if raw_broker_bid is not None:
            bid_list = [{
                "bid_broker_id": record.id,
                "bid_broker_name": record.name,
                "bid_broker_pos": record.pos,
                "code": merge_qot_mkt_stock_str(rsp_pb.s2c.security.market, rsp_pb.s2c.security.code),
                "order_id": record.orderID if record.HasField('orderID') else 'N/A',
                "order_volume": record.volume if record.HasField('volume') else 'N/A'
            } for record in raw_broker_bid]

        raw_broker_ask = rsp_pb.s2c.brokerAskList
        ask_list = []
        if raw_broker_ask is not None:
            ask_list = [{
                "ask_broker_id": record.id,
                "ask_broker_name": record.name,
                "ask_broker_pos": record.pos,
                "code": merge_qot_mkt_stock_str(rsp_pb.s2c.security.market, rsp_pb.s2c.security.code),
                "order_id": record.orderID if record.HasField('orderID') else 'N/A',
                "order_volume": record.volume if record.HasField('volume') else 'N/A'
            } for record in raw_broker_ask]

        return RET_OK, "", (stock_code, bid_list, ask_list)



class RequestHistoryKlineQuery:
    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, start_date, end_date, ktype, autype, fields,
                 max_num, conn_id, next_req_key, extended_time):
        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            error_str = content
            return RET_ERROR, error_str, None

        market_code, stock_code = content

        # check k line type
        if not KLType.if_has_key(ktype):
            error_str = ERROR_STR_PREFIX + "ktype is %s, which is not valid. (%s)" \
                % (ktype, KLType.get_all_keys())
            return RET_ERROR, error_str, None

        if not AuType.if_has_key(autype):
            error_str = ERROR_STR_PREFIX + "autype is %s, which is not valid. (%s)" \
                % (autype, AuType.get_all_keys())
            return RET_ERROR, error_str, None

        from futu.common.pb.Qot_RequestHistoryKL_pb2 import Request

        req = Request()
        _, req.c2s.rehabType = AuType.to_number(autype)
        _, req.c2s.klType = KLType.to_number(ktype)
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code
        if start_date:
            req.c2s.beginTime = start_date
        if end_date:
            req.c2s.endTime = end_date
        req.c2s.maxAckKLNum = max_num
        req.c2s.needKLFieldsFlag = KL_FIELD.kl_fields_to_flag_val(fields)
        if next_req_key is not None:
            req.c2s.nextReqKey = next_req_key
        if extended_time:
            req.c2s.extendedTime = True

        return pack_pb_req(req, ProtoId.Qot_RequestHistoryKL, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        has_next = False
        next_req_key = None
        if rsp_pb.s2c.HasField('nextReqKey'):
            has_next = True
            next_req_key = bytes(rsp_pb.s2c.nextReqKey)

        stock_code = merge_qot_mkt_stock_str(rsp_pb.s2c.security.market,
                                             rsp_pb.s2c.security.code)

        list_ret = []
        dict_data = {}
        raw_kline_list = rsp_pb.s2c.klList
        for record in raw_kline_list:
            dict_data['code'] = stock_code
            dict_data['time_key'] = record.time
            if record.isBlank:
                continue
            if record.HasField('openPrice'):
                dict_data['open'] = record.openPrice
            if record.HasField('highPrice'):
                dict_data['high'] = record.highPrice
            if record.HasField('lowPrice'):
                dict_data['low'] = record.lowPrice
            if record.HasField('closePrice'):
                dict_data['close'] = record.closePrice
            if record.HasField('volume'):
                dict_data['volume'] = record.volume
            if record.HasField('turnover'):
                dict_data['turnover'] = record.turnover
            if record.HasField('pe'):
                dict_data['pe_ratio'] = record.pe
            if record.HasField('turnoverRate'):
                dict_data['turnover_rate'] = record.turnoverRate
            if record.HasField('changeRate'):
                dict_data['change_rate'] = record.changeRate
            if record.HasField('lastClosePrice'):
                dict_data['last_close'] = record.lastClosePrice
            list_ret.append(dict_data.copy())

        return RET_OK, "", (list_ret, has_next, next_req_key)



class SubscriptionQuery:
    """
    Query Conversion for getting user's subscription information.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_sub_or_unsub_req(cls,
                              code_list,
                              subtype_list,
                              is_sub,
                              conn_id,
                              is_first_push,
                              is_detailed_orderbook,
                              extended_time,
                              reg_or_unreg_push,
                              unsub_all=False):

        stock_tuple_list = []

        if code_list is not None:
            for code in code_list:
                ret_code, content = split_stock_str(code)
                if ret_code != RET_OK:
                    return ret_code, content, None
                market_code, stock_code = content
                stock_tuple_list.append((market_code, stock_code))

        from futu.common.pb.Qot_Sub_pb2 import Request
        req = Request()

        if unsub_all is True:
            req.c2s.isUnsubAll = True
            req.c2s.isSubOrUnSub = False
        else:
            for market_code, stock_code in stock_tuple_list:
                stock_inst = req.c2s.securityList.add()
                stock_inst.code = stock_code
                stock_inst.market = market_code
            for subtype in subtype_list:
                r, v = SubType.to_number(subtype)
                req.c2s.subTypeList.append(v)
            req.c2s.isSubOrUnSub = is_sub
            req.c2s.isFirstPush = is_first_push
            req.c2s.isRegOrUnRegPush = reg_or_unreg_push
            req.c2s.isSubOrderBookDetail = is_detailed_orderbook
            req.c2s.extendedTime = extended_time

        return pack_pb_req(req, ProtoId.Qot_Sub, conn_id)

    @classmethod
    def pack_subscribe_req(cls, code_list, subtype_list, conn_id, is_first_push, subscribe_push, is_detailed_orderbook, extended_time):
        return SubscriptionQuery.pack_sub_or_unsub_req(code_list,
                                                       subtype_list,
                                                       True,
                                                       conn_id,
                                                       is_first_push,
                                                       is_detailed_orderbook,
                                                       extended_time,
                                                       subscribe_push)  # True

    @classmethod
    def unpack_subscribe_rsp(cls, rsp_pb):

        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        return RET_OK, "", None

    @classmethod
    def pack_unsubscribe_req(cls, code_list, subtype_list, unsubscribe_all, conn_id):

        return SubscriptionQuery.pack_sub_or_unsub_req(code_list,
                                                       subtype_list,
                                                       False,
                                                       conn_id,
                                                       False,
                                                       False,
                                                       False,
                                                       False,
                                                       unsubscribe_all)

    @classmethod
    def unpack_unsubscribe_rsp(cls, rsp_pb):
        """Unpack the un-subscribed response"""
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        return RET_OK, "", None

    @classmethod
    def pack_subscription_query_req(cls, is_all_conn, conn_id):

        from futu.common.pb.Qot_GetSubInfo_pb2 import Request
        req = Request()
        req.c2s.isReqAllConn = is_all_conn

        return pack_pb_req(req, ProtoId.Qot_GetSubInfo, conn_id)

    @classmethod
    def unpack_subscription_query_rsp(cls, rsp_pb):

        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None
        raw_sub_info = rsp_pb.s2c
        result = {}
        result['total_used'] = raw_sub_info.totalUsedQuota
        result['remain'] = raw_sub_info.remainQuota
        result['conn_sub_list'] = []
        for conn_sub_info in raw_sub_info.connSubInfoList:
            conn_sub_info_tmp = {}
            conn_sub_info_tmp['used'] = conn_sub_info.usedQuota
            conn_sub_info_tmp['is_own_conn'] = conn_sub_info.isOwnConnData
            conn_sub_info_tmp['sub_list'] = []
            for sub_info in conn_sub_info.subInfoList:
                sub_info_tmp = {}
                r, str_sub_type = SubType.to_string(sub_info.subType)
                if not r:
                    logger.error("error subtype:{}".format(sub_info.subType))
                    continue

                sub_info_tmp['subtype'] = str_sub_type
                sub_info_tmp['code_list'] = []
                for stock in sub_info.securityList:
                    sub_info_tmp['code_list'].append(
                        merge_qot_mkt_stock_str(int(stock.market), stock.code),)

                conn_sub_info_tmp['sub_list'].append(sub_info_tmp)

            result['conn_sub_list'].append(conn_sub_info_tmp)

        return RET_OK, "", result

    @classmethod
    def pack_push_or_unpush_req(cls, code_list, subtype_list, is_push, conn_id, is_first_push):
        stock_tuple_list = []
        for code in code_list:
            ret_code, content = split_stock_str(code)
            if ret_code != RET_OK:
                return ret_code, content, None
            market_code, stock_code = content
            stock_tuple_list.append((market_code, stock_code))

        from futu.common.pb.Qot_RegQotPush_pb2 import Request
        req = Request()
        for market_code, stock_code in stock_tuple_list:
            stock_inst = req.c2s.securityList.add()
            stock_inst.code = stock_code
            stock_inst.market = market_code
        for subtype in subtype_list:
            _, v = SubType.to_number(subtype)
            req.c2s.subTypeList.append(v)
        req.c2s.isRegOrUnReg = is_push
        req.c2s.isFirstPush = True if is_first_push else False

        return pack_pb_req(req, ProtoId.Qot_RegQotPush, conn_id)

    @classmethod
    def pack_push_req(cls, code_list, subtype_list, conn_id, is_first_push):

        return SubscriptionQuery.pack_push_or_unpush_req(code_list, subtype_list, True, conn_id, is_first_push)

    @classmethod
    def pack_unpush_req(cls, code_list, subtype_list, conn_id, is_first_push=False):

        return SubscriptionQuery.pack_push_or_unpush_req(code_list, subtype_list, False, conn_id, is_first_push)


def parse_pb_BasicQot(pb):
    item = {
        'code': merge_qot_mkt_stock_str(int(pb.security.market), pb.security.code),
        'data_date':pb.updateTime.split()[0] if len(pb.updateTime) > 0 else '',
        'data_time': pb.updateTime.split()[1] if len(pb.updateTime) > 0 else '',
        'last_price': pb.curPrice,
        'open_price': pb.openPrice,
        'high_price': pb.highPrice,
        'low_price': pb.lowPrice,
        'prev_close_price': pb.lastClosePrice,
        'volume': int(pb.volume),
        'turnover': pb.turnover,
        'turnover_rate': pb.turnoverRate,
        'amplitude': pb.amplitude,
        'suspension': pb.isSuspended,
        'listing_date': "N/A" if pb.HasField('optionExData') else pb.listTime,
        'price_spread': pb.priceSpread,
        'dark_status': DarkStatus.to_string2(pb.darkStatus) if pb.HasField('darkStatus') else 'N/A',
        'sec_status': SecurityStatus.to_string2(pb.secStatus) if pb.HasField(
            'secStatus') else 'N/A',
    }

    if pb.HasField('optionExData'):
        set_item_from_pb(item, pb.optionExData, pb_field_map_OptionBasicQotExData)
    else:
        set_item_none(item, pb_field_map_OptionBasicQotExData) # 这里设置了 'N/A'

    if pb.HasField('futureExData'):
        set_item_from_pb(item, pb.futureExData, pb_field_map_FutureBasicQotExData)
    else:
        set_item_none(item, pb_field_map_FutureBasicQotExData)

    if pb.HasField('preMarket'):
        set_item_from_pb(item, pb.preMarket, pb_field_map_PreAfterMarketData_pre)
    else:
        set_item_none(item, pb_field_map_PreAfterMarketData_pre)

    if pb.HasField('afterMarket'):
        set_item_from_pb(item, pb.afterMarket, pb_field_map_PreAfterMarketData_after)
    else:
        set_item_none(item, pb_field_map_PreAfterMarketData_after)

    return item

class StockQuoteQuery:
    """
    Query Conversion for getting stock quote data.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, stock_list, conn_id):

        stock_tuple_list = []
        failure_tuple_list = []
        for stock_str in stock_list:
            ret_code, content = split_stock_str(stock_str)
            if ret_code != RET_OK:
                msg = content
                error_str = ERROR_STR_PREFIX + msg
                failure_tuple_list.append((ret_code, error_str))
                continue
            market_code, stock_code = content
            stock_tuple_list.append((market_code, stock_code))

        if len(failure_tuple_list) > 0:
            error_str = '\n'.join([x[1] for x in failure_tuple_list])
            return RET_ERROR, error_str, None

        from futu.common.pb.Qot_GetBasicQot_pb2 import Request
        req = Request()
        for market_code, stock_code in stock_tuple_list:
            stock_inst = req.c2s.securityList.add()
            stock_inst.market = market_code
            stock_inst.code = stock_code

        return pack_pb_req(req, ProtoId.Qot_GetBasicQot, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):

        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, []
        raw_quote_list = rsp_pb.s2c.basicQotList

        quote_list = list()
        for record in raw_quote_list:
            item = parse_pb_BasicQot(record)
            if item:
                quote_list.append(item)
        return RET_OK, "", quote_list


class TickerQuery:
    """Stick ticker data query class"""

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, num, conn_id):

        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            error_str = content
            return RET_ERROR, error_str, None

        if isinstance(num, int) is False:
            error_str = ERROR_STR_PREFIX + "num is %s of type %s, and the type shoud be %s" \
                                           % (num, str(type(num)), str(int))
            return RET_ERROR, error_str, None

        if num < 0:
            error_str = ERROR_STR_PREFIX + "num is %s, which is less than 0" % num
            return RET_ERROR, error_str, None

        market_code, stock_code = content
        from futu.common.pb.Qot_GetTicker_pb2 import Request
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code
        req.c2s.maxRetNum = num

        return pack_pb_req(req, ProtoId.Qot_GetTicker, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):

        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        stock_code = merge_qot_mkt_stock_str(rsp_pb.s2c.security.market,
                                             rsp_pb.s2c.security.code)
        raw_ticker_list = rsp_pb.s2c.tickerList
        ticker_list = [{
            "code": stock_code,
            "time": record.time,
            "price": record.price,
            "volume": record.volume,
            "turnover": record.turnover,
            "ticker_direction": TickerDirect.to_string2(record.dir),
            "sequence": record.sequence,
            "recv_timestamp":record.recvTime,
            "type": TickerType.to_string2(record.type),
            "push_data_type": PushDataType.to_string2(record.pushDataType),
        } for record in raw_ticker_list]
        return RET_OK, "", ticker_list


class CurKlineQuery:
    """Stock Kline data query class"""

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, num, ktype, autype, conn_id):

        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            error_str = content
            return RET_ERROR, error_str, None

        market_code, stock_code = content

        if not KLType.if_has_key(ktype):
            error_str = ERROR_STR_PREFIX + "ktype is %s, which is not valid. (%s)" \
                                           % (ktype, KLType.get_all_keys())
            return RET_ERROR, error_str, None

        if not AuType.if_has_key(autype):
            error_str = ERROR_STR_PREFIX + "autype is %s, which is not valid. (%s)" \
                                           % (autype, AuType.get_all_keys())
            return RET_ERROR, error_str, None

        if isinstance(num, int) is False:
            error_str = ERROR_STR_PREFIX + "num is %s of type %s, which type should be %s" \
                                           % (num, str(type(num)), str(int))
            return RET_ERROR, error_str, None

        if num < 0:
            error_str = ERROR_STR_PREFIX + "num is %s, which is less than 0" % num
            return RET_ERROR, error_str, None
        from futu.common.pb.Qot_GetKL_pb2 import Request
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code
        _, req.c2s.rehabType = AuType.to_number(autype)
        req.c2s.reqNum = num
        _, req.c2s.klType = KLType.to_number(ktype)

        return pack_pb_req(req, ProtoId.Qot_GetKL, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):

        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, []

        stock_code = merge_qot_mkt_stock_str(rsp_pb.s2c.security.market,
                                             rsp_pb.s2c.security.code)
        raw_kline_list = rsp_pb.s2c.klList
        kline_list = [{
            "code": stock_code,
            "time_key": record.time,
            "open": record.openPrice,
            "high": record.highPrice,
            "low": record.lowPrice,
            "close": record.closePrice,
            "volume": record.volume,
            "turnover": record.turnover,
            "pe_ratio": record.pe,
            "turnover_rate": record.turnoverRate,
            "last_close": record.lastClosePrice,
        } for record in raw_kline_list]

        return RET_OK, "", kline_list


class CurKlinePush:
    """Stock Kline data push class"""

    def __init__(self):
        pass

    @classmethod
    def unpack_rsp(cls, rsp_pb):

        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, []

        r, kl_type = KLType.to_string(rsp_pb.s2c.klType);
        if not r:
            return RET_ERROR, "kline push error kltype", None

        stock_code = merge_qot_mkt_stock_str(rsp_pb.s2c.security.market,
                                             rsp_pb.s2c.security.code)
        raw_kline_list = rsp_pb.s2c.klList
        kline_list = [{
            "k_type": kl_type,
            "code": stock_code,
            "time_key": record.time,
            "open": record.openPrice,
            "high": record.highPrice,
            "low": record.lowPrice,
            "close": record.closePrice,
            "volume": record.volume,
            "turnover": record.turnover,
            "pe_ratio": record.pe,
            "turnover_rate": record.turnoverRate,
            "last_close": record.lastClosePrice,
        } for record in raw_kline_list]

        return RET_OK, "", kline_list


class OrderBookQuery:
    """
    Query Conversion for getting stock order book data.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, num, conn_id):

        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            error_str = content
            return RET_ERROR, error_str, None

        market_code, stock_code = content
        from futu.common.pb.Qot_GetOrderBook_pb2 import Request
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code
        req.c2s.num = num

        return pack_pb_req(req, ProtoId.Qot_GetOrderBook, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):

        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, []

        raw_order_book_ask = rsp_pb.s2c.orderBookAskList
        raw_order_book_bid = rsp_pb.s2c.orderBookBidList

        order_book = {}
        order_book['code'] = merge_qot_mkt_stock_str(
            rsp_pb.s2c.security.market, rsp_pb.s2c.security.code)
        order_book['svr_recv_time_bid'] = rsp_pb.s2c.svrRecvTimeBid
        order_book['svr_recv_time_ask'] = rsp_pb.s2c.svrRecvTimeAsk
        order_book['Bid'] = []
        order_book['Ask'] = []

        for record in raw_order_book_bid:
            detail = {}
            for info in record.detailList:
                detail[info.orderID] = info.volume
            order_book['Bid'].append((record.price, record.volume,
                                      record.orederCount, detail))
        for record in raw_order_book_ask:
            detail = {}
            for info in record.detailList:
                detail[info.orderID] = info.volume
            order_book['Ask'].append((record.price, record.volume,
                                      record.orederCount, detail))
        return RET_OK, "", order_book


class SuspensionQuery:
    """
    Query SuspensionQuery.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code_list, start, end, conn_id):

        list_req_stock = []
        for stock_str in code_list:
            ret, content = split_stock_str(stock_str)
            if ret == RET_ERROR:
                return RET_ERROR, content, None
            else:
                list_req_stock.append(content)

        from futu.common.pb.Qot_GetSuspend_pb2 import Request
        req = Request()
        if start:
            req.c2s.beginTime = start
        if end:
            req.c2s.endTime = end
        for market, code in list_req_stock:
            stock_inst = req.c2s.securityList.add()
            stock_inst.market = market
            stock_inst.code = code

        return pack_pb_req(req, ProtoId.Qot_GetSuspend, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):

        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        ret_susp_list = []
        for record in rsp_pb.s2c.SecuritySuspendList:
            suspend_info_tmp = {}
            code = merge_qot_mkt_stock_str(
                record.security.market, record.security.code)
            for suspend_info in record.suspendList:
                suspend_info_tmp['code'] = code
                suspend_info_tmp['suspension_dates'] = suspend_info.time
            ret_susp_list.append(suspend_info_tmp)

        return RET_OK, "", ret_susp_list


class GlobalStateQuery:
    """
    Query process "FTNN.exe" global state : market state & logined state
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, user_id, conn_id):

        from futu.common.pb.GetGlobalState_pb2 import Request
        req = Request()
        req.c2s.userID = user_id
        return pack_pb_req(req, ProtoId.GetGlobalState, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):

        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        state = rsp_pb.s2c
        program_status_type = ProgramStatusType.NONE
        program_status_desc = ""
        if state.HasField('programStatus'):
            program_status_type = ProgramStatusType.to_string2(
                state.programStatus.type)
            if state.programStatus.HasField("strExtDesc"):
                program_status_desc = state.programStatus.strExtDesc

        state_dict = {
            'market_sz': MarketState.to_string2(state.marketSZ),
            'market_us': MarketState.to_string2(state.marketUS),
            'market_sh': MarketState.to_string2(state.marketSH),
            'market_hk': MarketState.to_string2(state.marketHK),
            'market_hkfuture': MarketState.to_string2(state.marketHKFuture),
            'market_usfuture': MarketState.to_string2(state.marketUSFuture),
            'server_ver': str(state.serverVer),
            'trd_logined': state.trdLogined,
            'timestamp': str(state.time),
            'qot_logined': state.qotLogined,
            'local_timestamp': state.localTime if state.HasField('localTime') else time.time(),
            'program_status_type': program_status_type,
            'program_status_desc': program_status_desc
        }
        return RET_OK, "", state_dict


class KeepAlive:
    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, conn_id):

        from futu.common.pb.KeepAlive_pb2 import Request
        req = Request()
        req.c2s.time = int(time.time())
        return pack_pb_req(req, ProtoId.KeepAlive, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):

        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        return RET_OK, '', rsp_pb.s2c.time


class SysNotifyPush:
    """ SysNotifyPush """

    def __init__(self):
        pass

    @classmethod
    def unpack_rsp(cls, rsp_pb):

        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg,

        pb_type = rsp_pb.s2c.type
        sub_type = None
        data = None
        notify_type = SysNotifyType.to_string2(pb_type)
        if notify_type == SysNotifyType.GTW_EVENT:
            if rsp_pb.s2c.HasField('event'):
                sub_type = GtwEventType.to_string2(rsp_pb.s2c.event.eventType)
                data = rsp_pb.s2c.event.desc
        elif notify_type == SysNotifyType.PROGRAM_STATUS:
            if rsp_pb.s2c.HasField('programStatus'):
                ret, status_type = ProgramStatusType.to_string(
                    rsp_pb.s2c.programStatus.programStatus.type)
                if not ret:
                    status_type = ProgramStatusType.NONE
                if rsp_pb.s2c.programStatus.programStatus.HasField('strExtDesc'):
                    status_desc = rsp_pb.s2c.programStatus.programStatus.strExtDesc
                else:
                    status_desc = ''
                sub_type = status_type
                data = status_desc
        elif notify_type == SysNotifyType.CONN_STATUS:
            if rsp_pb.s2c.HasField('connectStatus'):
                data = {'qot_logined': rsp_pb.s2c.connectStatus.qotLogined,
                        'trd_logined': rsp_pb.s2c.connectStatus.trdLogined}
        elif notify_type == SysNotifyType.QOT_RIGHT:
            if rsp_pb.s2c.HasField('qotRight'):
                qot_right = rsp_pb.s2c.qotRight
                data = {'hk_qot_right': QotRight.to_string2(qot_right.hkQotRight),
                        'hk_option_qot_right': QotRight.to_string2(qot_right.hkOptionQotRight) if qot_right.HasField('hkOptionQotRight') else 'N/A',
                        'hk_future_qot_right': QotRight.to_string2(qot_right.hkFutureQotRight) if qot_right.HasField('hkFutureQotRight') else 'N/A',
                        'us_qot_right': QotRight.to_string2(qot_right.usQotRight),
                        'us_option_qot_right': QotRight.to_string2(qot_right.usOptionQotRight) if qot_right.HasField('usOptionQotRight') else 'N/A',
                        'us_future_qot_right': QotRight.to_string2(qot_right.usFutureQotRight) if qot_right.HasField('usFutureQotRight') else 'N/A',
                        'cn_qot_right': QotRight.to_string2(qot_right.cnQotRight)}
        elif notify_type == SysNotifyType.API_LEVEL:
            if rsp_pb.s2c.HasField('apiLevel'):
                data = {'api_level': rsp_pb.s2c.apiLevel.apiLevel}

        if data is None:
            logger.warning(
                "SysNotifyPush data is None: notify_type={}".format(notify_type))

        return RET_OK, (notify_type, sub_type, data)



class StockReferenceList:
    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, ref_type, conn_id):
        from futu.common.pb.Qot_GetReference_pb2 import Request

        ret, content = split_stock_str(code)
        if ret != RET_OK:
            return ret, content, None

        req = Request()
        req.c2s.security.market = content[0]
        req.c2s.security.code = content[1]
        _, req.c2s.referenceType = SecurityReferenceType.to_number(ref_type)

        return pack_pb_req(req, ProtoId.Qot_GetReference, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        if not rsp_pb.HasField('s2c'):
            return RET_OK, '', None

        data_list = []
        for info in rsp_pb.s2c.staticInfoList:
            data = {}
            data['code'] = merge_qot_mkt_stock_str(
                info.basic.security.market, info.basic.security.code)
            # item['stock_id'] = info.basic.id
            data['lot_size'] = info.basic.lotSize
            data['stock_type'] = SecurityType.to_string2(info.basic.secType)
            data['stock_name'] = info.basic.name
            data['list_time'] = info.basic.listTime
            if info.HasField('warrantExData'):
                data['wrt_valid'] = True
                data['wrt_type'] = WrtType.to_string2(info.warrantExData.type)
                data['wrt_code'] = merge_qot_mkt_stock_str(info.warrantExData.owner.market,
                                                           info.warrantExData.owner.code)
            else:
                data['wrt_valid'] = False

            if info.HasField('futureExData'):
                data['future_valid'] = True
                data['future_main_contract'] = info.futureExData.isMainContract
                data['future_last_trade_time'] = info.futureExData.lastTradeTime
            else:
                data['future_valid'] = False

            data_list.append(data)

        return RET_OK, '', data_list


class OwnerPlateQuery:
    """
    Query Conversion for getting owner plate information.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code_list, conn_id):

        stock_tuple_list = []
        failure_tuple_list = []
        for stock_str in code_list:
            ret_code, content = split_stock_str(stock_str)
            if ret_code != RET_OK:
                error_str = content
                failure_tuple_list.append((ret_code, error_str))
                continue
            market_code, stock_code = content
            stock_tuple_list.append((market_code, stock_code))

        if len(failure_tuple_list) > 0:
            error_str = '\n'.join([x[1] for x in failure_tuple_list])
            return RET_ERROR, error_str, None

        from futu.common.pb.Qot_GetOwnerPlate_pb2 import Request
        req = Request()
        for market_code, stock_code in stock_tuple_list:
            stock_inst = req.c2s.securityList.add()
            stock_inst.market = market_code
            stock_inst.code = stock_code

        return pack_pb_req(req, ProtoId.Qot_GetOwnerPlate, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, []
        raw_quote_list = rsp_pb.s2c.ownerPlateList

        data_list = []
        for record in raw_quote_list:
            plate_info_list = record.plateInfoList
            for plate_info in plate_info_list:
                quote_list = {
                    'code': merge_qot_mkt_stock_str(record.security.market, record.security.code),
                    'plate_code': merge_qot_mkt_stock_str(plate_info.plate.market, plate_info.plate.code),
                    'plate_name': str(plate_info.name),
                    'plate_type': Plate.to_string2(plate_info.plateType)
                }
                data_list.append(quote_list)

        return RET_OK, "", data_list


class HoldingChangeList:
    """
    Query Conversion for getting holding change list.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, holder_type, conn_id, start_date, end_date=None):

        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            error_str = content
            return RET_ERROR, error_str, None

        market_code, stock_code = content

        if start_date is None:
            msg = "The start date is none."
            return RET_ERROR, msg, None
        else:
            ret, msg = normalize_date_format(start_date)
            if ret != RET_OK:
                return ret, msg, None
            start_date = msg

        if end_date is None:
            today = datetime.today()
            end_date = today.strftime("%Y-%m-%d")
        else:
            ret, msg = normalize_date_format(end_date)
            if ret != RET_OK:
                return ret, msg, None
            end_date = msg

        from futu.common.pb.Qot_GetHoldingChangeList_pb2 import Request
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code
        req.c2s.holderCategory = holder_type
        req.c2s.beginTime = start_date
        if end_date:
            req.c2s.endTime = end_date

        return pack_pb_req(req, ProtoId.Qot_GetHoldingChangeList, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, []
        raw_quote_list = rsp_pb.s2c.holdingChangeList

        data_list = []
        for record in raw_quote_list:
            quote_list = {
                'holder_name': record.holderName,
                'holding_qty': record.holdingQty,
                'holding_ratio': record.holdingRatio,
                'change_qty': record.changeQty,
                'change_ratio': record.changeRatio,
                'time': record.time,
            }
            data_list.append(quote_list)

        return RET_OK, "", data_list

class OptionDataFilter:
    def __init__(self):
        self.implied_volatility_min = None  # 隐含波动率过滤起点 %
        self.implied_volatility_max = None  # 隐含波动率过滤终点 %
        self.delta_min = None  # 希腊值 Delta过滤起点
        self.delta_max = None  # 希腊值 Delta过滤终点
        self.gamma_min = None  # 希腊值 Gamma过滤起点
        self.gamma_max = None  # 希腊值 Gamma过滤终点
        self.vega_min = None # 希腊值 Vega过滤起点
        self.vega_max = None  # 希腊值 Vega过滤终点
        self.theta_min = None  # 希腊值 Theta过滤起点
        self.theta_max = None  # 希腊值 Theta过滤终点
        self.rho_min = None  # 希腊值 Rho过滤起点
        self.rho_max = None  # 希腊值 Rho过滤终点
        self.net_open_interest_min = None  # 净未平仓合约数过滤起点
        self.net_open_interest_max = None  # 净未平仓合约数过滤终点
        self.open_interest_min = None  # 未平仓合约数过滤起点
        self.open_interest_max = None  # 未平仓合约数过滤终点
        self.vol_min = None  # 成交量过滤起点
        self.vol_max = None  # 成交量过滤终点

class OptionChain:
    """
    Query Conversion for getting option chain information.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, index_option_type, conn_id, start_date, end_date=None, option_type=OptionType.ALL, option_cond_type=OptionCondType.ALL, data_filter = None):

        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            error_str = content
            return RET_ERROR, error_str, None

        market_code, stock_code = content

        if start_date is None:
            msg = "The start date is none."
            return RET_ERROR, msg, None
        else:
            ret, msg = normalize_date_format(start_date)
            if ret != RET_OK:
                return ret, msg, None
            start_date = msg

        if end_date is None:
            today = datetime.today()
            end_date = today.strftime("%Y-%m-%d")
        else:
            ret, msg = normalize_date_format(end_date)
            if ret != RET_OK:
                return ret, msg, None
            end_date = msg

        r, option_cond_type = OptionCondType.to_number(option_cond_type)
        if r is False:
            option_cond_type = None

        r, option_type = OptionType.to_number(option_type)
        if r is False:
            option_type = None

        r, index_option_type = IndexOptionType.to_number(index_option_type)
        if r is False:
            index_option_type = None

        from futu.common.pb.Qot_GetOptionChain_pb2 import Request
        req = Request()
        req.c2s.owner.market = market_code
        req.c2s.owner.code = stock_code
        if index_option_type is not None:
            req.c2s.indexOptionType = index_option_type
        req.c2s.beginTime = start_date
        req.c2s.endTime = end_date
        if option_type is not None:
            req.c2s.type = option_type
        if option_cond_type is not None:
            req.c2s.condition = option_cond_type

        if data_filter is not None:
            if data_filter.implied_volatility_min is not None:
                req.c2s.dataFilter.impliedVolatilityMin = data_filter.implied_volatility_min
            if data_filter.implied_volatility_max is not None:
                req.c2s.dataFilter.impliedVolatilityMax = data_filter.implied_volatility_max

            if data_filter.delta_min is not None:
                req.c2s.dataFilter.deltaMin = data_filter.delta_min
            if data_filter.delta_max is not None:
                req.c2s.dataFilter.deltaMax = data_filter.delta_max

            if data_filter.gamma_min is not None:
                req.c2s.dataFilter.gammaMin = data_filter.gamma_min
            if data_filter.gamma_max is not None:
                req.c2s.dataFilter.gammaMax = data_filter.gamma_max

            if data_filter.vega_min is not None:
                req.c2s.dataFilter.vegaMin = data_filter.vega_min
            if data_filter.vega_max is not None:
                req.c2s.dataFilter.vegaMax = data_filter.vega_max

            if data_filter.theta_min is not None:
                req.c2s.dataFilter.thetaMin = data_filter.theta_min
            if data_filter.theta_max is not None:
                req.c2s.dataFilter.thetaMax = data_filter.theta_max

            if data_filter.rho_min is not None:
                req.c2s.dataFilter.rhoMin = data_filter.rho_min
            if data_filter.rho_max is not None:
                req.c2s.dataFilter.rhoMax = data_filter.rho_max

            if data_filter.net_open_interest_min is not None:
                req.c2s.dataFilter.netOpenInterestMin = data_filter.net_open_interest_min
            if data_filter.net_open_interest_max is not None:
                req.c2s.dataFilter.netOpenInterestMax = data_filter.net_open_interest_max

            if data_filter.open_interest_min is not None:
                req.c2s.dataFilter.openInterestMin = data_filter.open_interest_min
            if data_filter.open_interest_max is not None:
                req.c2s.dataFilter.openInterestMax = data_filter.open_interest_max

            if data_filter.vol_min is not None:
                req.c2s.dataFilter.volMin = data_filter.vol_min
            if data_filter.vol_max is not None:
                req.c2s.dataFilter.volMax = data_filter.vol_max

        return pack_pb_req(req, ProtoId.Qot_GetOptionChain, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, []
        raw_quote_list = rsp_pb.s2c.optionChain

        data_list = []
        for OptionItem in raw_quote_list:
            for record_all in OptionItem.option:
                record_list = []
                if record_all.HasField('call'):
                    record_list.append(record_all.call)
                if record_all.HasField('put'):
                    record_list.append(record_all.put)

                for record in record_list:
                    quote_list = {
                        'code': merge_qot_mkt_stock_str(int(record.basic.security.market), record.basic.security.code),
                        "stock_id": record.basic.id,
                        "name": record.basic.name,
                        "lot_size": record.basic.lotSize,
                        "stock_type": SecurityType.to_string2(record.basic.secType),
                        "option_type": OptionType.to_string2(record.optionExData.type) if record.HasField('optionExData') else "",
                        "stock_owner": merge_qot_mkt_stock_str(int(record.optionExData.owner.market), record.optionExData.owner.code)
                        if record.HasField('optionExData') else "",
                        "strike_time": record.optionExData.strikeTime,
                        "strike_price": record.optionExData.strikePrice if record.HasField('optionExData') else NoneDataType,
                        "suspension": record.optionExData.suspend if record.HasField('optionExData') else NoneDataType,
                        "index_option_type": IndexOptionType.to_string2(record.optionExData.indexOptionType) if record.HasField('optionExData') else NoneDataType,
                    }
                    data_list.append(quote_list)

        return RET_OK, "", data_list


class OrderDetail:
    """
    Query Conversion for getting order detail information.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, conn_id):

        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            error_str = content
            return RET_ERROR, error_str, None

        market_code, stock_code = content

        from futu.common.pb.Qot_GetOrderDetail_pb2 import Request
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code

        return pack_pb_req(req, ProtoId.Qot_GetOrderDetail, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        code = merge_qot_mkt_stock_str(
            int(rsp_pb.s2c.security.market), rsp_pb.s2c.security.code)
        ask = [0, []]
        bid = [0, []]
        svr_recv_time_bid = rsp_pb.s2c.svrRecvTimeBid
        svr_recv_time_ask = rsp_pb.s2c.svrRecvTimeAsk

        ask[0] = rsp_pb.s2c.orderDetailAsk.orderCount
        for vol in rsp_pb.s2c.orderDetailAsk.orderVol:
            ask[1].append(vol)

        bid[0] = rsp_pb.s2c.orderDetailBid.orderCount
        for vol in rsp_pb.s2c.orderDetailBid.orderVol:
            bid[1].append(vol)

        data = {
            'code': code,
            'Ask': ask,
            'Bid': bid,
            'svr_recv_time_ask': svr_recv_time_ask,
            'svr_recv_time_bid': svr_recv_time_bid
        }
        return RET_OK, "", data


class QuoteWarrant:
    """
    拉取窝轮
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, req, conn_id):
        from futu.quote.quote_get_warrant import Request as WarrantRequest
        if (req is None) or (not isinstance(req, WarrantRequest)):
            req = WarrantRequest()
        ret, context = req.fill_request_pb()
        if ret == RET_OK:
            return pack_pb_req(context, ProtoId.Qot_GetWarrant, conn_id)
        else:
            return ret, context, None

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        from futu.quote.quote_get_warrant import Response as WarrantResponse
        return WarrantResponse.unpack_response_pb(rsp_pb)


class HistoryKLQuota:
    """
    拉取限额
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, get_detail, conn_id):
        from futu.common.pb.Qot_RequestHistoryKLQuota_pb2 import Request
        req = Request()
        req.c2s.bGetDetail = get_detail
        return pack_pb_req(req, ProtoId.Qot_RequestHistoryKLQuota, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None
        used_quota = rsp_pb.s2c.usedQuota
        remain_quota = rsp_pb.s2c.remainQuota
        detail_list = []

        details = rsp_pb.s2c.detailList
        for item in details:
            code = merge_qot_mkt_stock_str(
                int(item.security.market), item.security.code)
            request_time = str(item.requestTime)
            detail_list.append({"code": code, "request_time": request_time})

        data = {
            "used_quota": used_quota,
            "remain_quota": remain_quota,
            "detail_list": detail_list
        }
        return RET_OK, "", data


class RequestRehab:
    """
    获取除权信息
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, stock, conn_id):
        ret_code, content = split_stock_str(stock)
        if ret_code != RET_OK:
            msg = content
            error_str = ERROR_STR_PREFIX + msg
            return RET_ERROR, error_str, None
        market, code = content

        from futu.common.pb.Qot_RequestRehab_pb2 import Request
        req = Request()
        req.c2s.security.market = market
        req.c2s.security.code = code
        return pack_pb_req(req, ProtoId.Qot_RequestRehab, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):

        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        class KLRehabFlag(object):
            SPLIT = 1
            JOIN = 2
            BONUS = 4
            TRANSFER = 8
            ALLOT = 16
            ADD = 32
            DIVIDED = 64
            SP_DIVIDED = 128

        rehab_list = list()
        for rehab in rsp_pb.s2c.rehabList:
            stock_rehab_tmp = {}
            stock_rehab_tmp['ex_div_date'] = rehab.time.split()[0]  # 时间字符串
            stock_rehab_tmp['forward_adj_factorA'] = rehab.fwdFactorA
            stock_rehab_tmp['forward_adj_factorB'] = rehab.fwdFactorB
            stock_rehab_tmp['backward_adj_factorA'] = rehab.bwdFactorA
            stock_rehab_tmp['backward_adj_factorB'] = rehab.bwdFactorB

            act_flag = rehab.companyActFlag
            if act_flag == 0:
                continue

            if act_flag & KLRehabFlag.SP_DIVIDED:
                stock_rehab_tmp['special_dividend'] = rehab.spDividend
            if act_flag & KLRehabFlag.DIVIDED:
                stock_rehab_tmp['per_cash_div'] = rehab.dividend
            if act_flag & KLRehabFlag.ADD:
                stock_rehab_tmp['stk_spo_ratio'] = rehab.addBase / rehab.addErt
                stock_rehab_tmp['stk_spo_price'] = rehab.addPrice
            if act_flag & KLRehabFlag.ALLOT:
                stock_rehab_tmp['allotment_ratio'] = rehab.allotBase / \
                    rehab.allotErt
                stock_rehab_tmp['allotment_price'] = rehab.allotPrice
            if act_flag & KLRehabFlag.TRANSFER:
                stock_rehab_tmp['per_share_trans_ratio'] = rehab.transferBase / \
                    rehab.transferErt
            if act_flag & KLRehabFlag.BONUS:
                stock_rehab_tmp['per_share_div_ratio'] = rehab.bonusBase / \
                    rehab.bonusErt
            if act_flag & KLRehabFlag.JOIN:
                stock_rehab_tmp['join_ratio'] = rehab.joinBase / rehab.joinErt
            if act_flag & KLRehabFlag.SPLIT:
                stock_rehab_tmp['split_ratio'] = rehab.splitBase / \
                    rehab.splitErt

            rehab_list.append(stock_rehab_tmp)

        return RET_OK, "", rehab_list


"""-------------------------------------------------------------"""


class GetUserInfo:
    """
    拉取用户信息
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, info_field, conn_id):
        from futu.common.pb.GetUserInfo_pb2 import Request
        req = Request()
        if info_field is None:
            req.c2s.flag = 0
        else:
            req.c2s.flag = UserInfoField.fields_to_flag_val(info_field)
        return pack_pb_req(req, ProtoId.GetUserInfo, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None
        nick_name = rsp_pb.s2c.nickName if rsp_pb.s2c.HasField(
            'nickName') else "N/A"
        avatar_url = rsp_pb.s2c.avatarUrl if rsp_pb.s2c.HasField(
            'avatarUrl') else "N/A"
        api_level = rsp_pb.s2c.apiLevel if rsp_pb.s2c.HasField(
            'apiLevel') else "N/A"
        hk_qot_right = rsp_pb.s2c.hkQotRight if rsp_pb.s2c.HasField(
            'hkQotRight') else "N/A"
        hk_option_qot_right = rsp_pb.s2c.hkOptionQotRight if rsp_pb.s2c.HasField(
            'hkOptionQotRight') else "N/A"
        hk_future_qot_right = rsp_pb.s2c.hkFutureQotRight if rsp_pb.s2c.HasField(
            'hkFutureQotRight') else "N/A"
        us_qot_right = rsp_pb.s2c.usQotRight if rsp_pb.s2c.HasField(
            'usQotRight') else "N/A"
        cn_qot_right = rsp_pb.s2c.cnQotRight if rsp_pb.s2c.HasField(
            'cnQotRight') else "N/A"
        is_need_agree_disclaimer = rsp_pb.s2c.isNeedAgreeDisclaimer if rsp_pb.s2c.HasField(
            'isNeedAgreeDisclaimer') else "N/A"
        user_id = rsp_pb.s2c.userID if rsp_pb.s2c.HasField('userID') else "N/A"
        update_type = rsp_pb.s2c.updateType if rsp_pb.s2c.HasField(
            'updateType') else "N/A"
        web_key = rsp_pb.s2c.webKey if rsp_pb.s2c.HasField('webKey') else "N/A"
        sub_quota = rsp_pb.s2c.subQuota if rsp_pb.s2c.HasField('subQuota') else "N/A"
        history_kl_quota = rsp_pb.s2c.historyKLQuota if rsp_pb.s2c.HasField('historyKLQuota') else "N/A"
        data = {
            "nick_name": nick_name,
            "avatar_url": avatar_url,
            "api_level": api_level,
            "hk_qot_right": QotRight.to_string2(hk_qot_right),
            "hk_option_qot_right": QotRight.to_string2(hk_option_qot_right),
            "hk_future_qot_right": QotRight.to_string2(hk_future_qot_right),
            "us_qot_right": QotRight.to_string2(us_qot_right),
            "cn_qot_right": QotRight.to_string2(cn_qot_right),
            "is_need_agree_disclaimer": is_need_agree_disclaimer,
            "user_id": user_id,
            "update_type": UpdateType.to_string2(update_type),
            "web_key": web_key,
            "sub_quota": sub_quota,
            "history_kl_quota": history_kl_quota,
        }
        return RET_OK, "", data


class GetCapitalDistributionQuery:
    """
    Query GetCapitalDistribution.
    个股资金分布
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, conn_id):
        """check stock_code 股票"""
        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            error_str = content
            return RET_ERROR, error_str, None
        market_code, stock_code = content

        # 开始组包
        from futu.common.pb.Qot_GetCapitalDistribution_pb2 import Request
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code
        return pack_pb_req(req, ProtoId.Qot_GetCapitalDistribution, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None
        ret = dict()
        #  流入资金额度，大单 type=double
        ret["capital_in_big"] = rsp_pb.s2c.capitalInBig
        #  流入资金额度，中单 type=double
        ret["capital_in_mid"] = rsp_pb.s2c.capitalInMid
        #  流入资金额度，小单 type=double
        ret["capital_in_small"] = rsp_pb.s2c.capitalInSmall
        #  流出资金额度，大单 type=double
        ret["capital_out_big"] = rsp_pb.s2c.capitalOutBig
        #  流出资金额度，中单 type=double
        ret["capital_out_mid"] = rsp_pb.s2c.capitalOutMid
        #  流出资金额度，小单 type=double
        ret["capital_out_small"] = rsp_pb.s2c.capitalOutSmall
        #  更新时间字符串 type=string
        ret["update_time"] = rsp_pb.s2c.updateTime
        return RET_OK, "", ret


class GetCapitalFlowQuery:
    """
    Query GetCapitalFlow.
    个股资金流入流出
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, conn_id):
        """check stock_code 股票"""
        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            error_str = content
            return RET_ERROR, error_str, None
        market_code, stock_code = content

        # 开始组包
        from futu.common.pb.Qot_GetCapitalFlow_pb2 import Request
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code
        return pack_pb_req(req, ProtoId.Qot_GetCapitalFlow, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None
        ret_list = list()
        #  资金流向 type = Qot_GetCapitalFlow.CapitalFlowItem
        flow_item_list = rsp_pb.s2c.flowItemList
        #  数据最后有效时间字符串 type = string
        last_valid_time = rsp_pb.s2c.lastValidTime
        for item in flow_item_list:
            data = dict()
            ret_list.append(data)
            #  净流入的资金额度 type = double
            data["in_flow"] = item.inFlow
            #  开始时间字符串,以分钟为单位 type = string
            data["capital_flow_item_time"] = item.time
            data["last_valid_time"] = last_valid_time
        return RET_OK, "", ret_list


class GetDelayStatisticsQuery:
    """
    Query GetDelayStatistics.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, type_list, qot_push_stage, segment_list, conn_id):
        """check type_list 统计数据类型，DelayStatisticsType"""
        """check qot_push_stage 行情推送统计的区间，行情推送统计时有效，QotPushStage"""
        """check segment_list 统计分段，默认100ms以下以2ms分段，100ms以上以500，1000，2000，-1分段，-1表示无穷大。"""

        # 开始组包
        from futu.common.pb.GetDelayStatistics_pb2 import Request
        req = Request()
        for t in type_list:
            r, v = DelayStatisticsType.to_number(t)
            if r:
                req.c2s.typeList.append(v)

        r, v = QotPushStage.to_number(qot_push_stage)
        if r:
            req.c2s.qotPushStage = v

        for t in segment_list:
            req.c2s.segmentList.append(t)

        return pack_pb_req(req, ProtoId.GetDelayStatistics, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None
        ret_dic = dict()
        #  行情推送延迟统计 type = GetDelayStatistics.DelayStatistics
        qot_push_statistics_list = rsp_pb.s2c.qotPushStatisticsList
        #  请求延迟统计 type = GetDelayStatistics.ReqReplyStatisticsItem
        req_reply_statistics_list = rsp_pb.s2c.reqReplyStatisticsList
        #  下单延迟统计 type = GetDelayStatistics.PlaceOrderStatisticsItem
        place_order_statistics_list = rsp_pb.s2c.placeOrderStatisticsList
        # 请求延迟统计  列表类型
        ret_list_req_reply_statistics_list = list()
        ret_dic["req_reply_statistics_list"] = ret_list_req_reply_statistics_list
        # 下单延迟统计  列表类型
        ret_list_place_order_statistics_list = list()
        ret_dic["place_order_statistics_list"] = ret_list_place_order_statistics_list

        # 行情推送延迟统计 总表  列表类型
        qot_push_all_statistics_list = list()
        ret_dic["qot_push_all_statistics_list"] = qot_push_all_statistics_list

        for item in qot_push_statistics_list:
            #  平均延迟和总包数加入总表
            info = dict()
            qot_push_all_statistics_list.append(info)

            #  行情推送类型,QotPushType type = int32
            qot_push_type = item.qotPushType
            info["qot_push_type"] = qot_push_type
            #  统计信息 type = GetDelayStatistics.DelayStatisticsItem
            item_list = item.itemList
            #  平均延迟 type = float
            delay_avg = item.delayAvg
            info["delay_avg"] = delay_avg
            #  总包数 type = int32
            count = item.count
            info["count"] = count
            #  区段列表
            ls = list()
            info["list"] = ls

            for sub_item in item_list:
                data = dict()
                ls.append(data)
                #  范围左闭右开，[begin,end)耗时范围起点，毫秒单位 type = int32
                data["begin"] = sub_item.begin
                #  耗时范围结束，毫秒单位 type = int32
                data["end"] = sub_item.end
                #  个数 type = int32
                data["count"] = sub_item.count
                #  占比, % type = float
                data["proportion"] = sub_item.proportion
                #  累计占比, % type = float
                data["cumulative_ratio"] = sub_item.cumulativeRatio
        for item in req_reply_statistics_list:
            data = dict()
            ret_list_req_reply_statistics_list.append(data)
            #  协议ID type = int32
            data["proto_id"] = item.protoID
            #  请求个数 type = int32
            data["count"] = item.count
            #  平均总耗时，毫秒单位 type = float
            data["total_cost_avg"] = item.totalCostAvg
            #  平均OpenD耗时，毫秒单位 type = float
            data["open_d_cost_avg"] = item.openDCostAvg
            #  平均网络耗时，非当时实际请求网络耗时，毫秒单位 type = float
            data["net_delay_avg"] = item.netDelayAvg
            #  是否本地直接回包，没有向服务器请求数据 type = bool
            data["is_local_reply"] = item.isLocalReply
        for item in place_order_statistics_list:
            data = dict()
            ret_list_place_order_statistics_list.append(data)
            #  订单ID type = string
            data["order_id"] = item.orderID
            #  总耗时，毫秒单位 type = float
            data["total_cost"] = item.totalCost
            #  OpenD耗时，毫秒单位 type = float
            data["open_d_cost"] = item.openDCost
            #  网络耗时，非当时实际请求网络耗时，毫秒单位 type = float
            data["net_delay"] = item.netDelay
            #  订单回包后到接收到订单下到交易所的耗时，毫秒单位 type = float
            data["update_cost"] = item.updateCost
        return RET_OK, "", ret_dic


class Verification:
    """
    拉验证码
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, verification_type, verification_op, code, conn_id):
        from futu.common.pb.Verification_pb2 import Request
        req = Request()
        ret, data = VerificationType.to_number(verification_type)
        if ret:
            req.c2s.type = data
        else:
            return RET_ERROR, data, None

        ret, data = VerificationOp.to_number(verification_op)
        if ret:
            req.c2s.op = data
        else:
            return RET_ERROR, data, None

        if code is not None and len(code) != 0:
            req.c2s.code = code
        return pack_pb_req(req, ProtoId.Verification, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        return rsp_pb.retType, rsp_pb.retMsg, None

    """
    ===============================================================================
    ===============================================================================
    """


class ModifyUserSecurityQuery:
    """
    Query ModifyUserSecurity.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, group_name, op, code_list, conn_id):
        """check group_name 分组名,有同名的返回首个"""
        """check op ModifyUserSecurityOp,操作类型"""
        """check code_list 新增或删除该分组下的股票"""
        stock_tuple_list = []
        failure_tuple_list = []
        for stock_str in code_list:
            ret_code, content = split_stock_str(stock_str)
            if ret_code != RET_OK:
                error_str = content
                failure_tuple_list.append((ret_code, error_str))
                continue
            market_code, stock_code = content
            stock_tuple_list.append((market_code, stock_code))
        if len(failure_tuple_list) > 0:
            error_str = '\n'.join([x[1] for x in failure_tuple_list])
            return RET_ERROR, error_str, None

        # 开始组包
        from futu.common.pb.Qot_ModifyUserSecurity_pb2 import Request
        req = Request()
        req.c2s.groupName = group_name
        req.c2s.op = op
        for market_code, stock_code in stock_tuple_list:
            stock_inst = req.c2s.securityList.add()
            stock_inst.market = market_code
            stock_inst.code = stock_code

        return pack_pb_req(req, ProtoId.Qot_ModifyUserSecurity, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None
        return RET_OK, "", None


class GetUserSecurityQuery:
    """
    Query GetUserSecurity.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, group_name, conn_id):
        """check group_name 分组名,有同名的返回首个"""
        # 开始组包
        from futu.common.pb.Qot_GetUserSecurity_pb2 import Request
        req = Request()
        req.c2s.groupName = group_name
        return pack_pb_req(req, ProtoId.Qot_GetUserSecurity, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None
        #  自选股分组下的股票列表 type = Qot_Common.SecurityStaticInfo
        static_info_list = rsp_pb.s2c.staticInfoList
        #  基本股票静态信息 type = SecurityStaticBasic
        basic_info_list = [{
            "code": merge_qot_mkt_stock_str(record.basic.security.market,
                                            record.basic.security.code),
            "stock_id": record.basic.id,
            "name": record.basic.name,
            "lot_size": record.basic.lotSize,
            "stock_type": SecurityType.to_string2(record.basic.secType),
            "stock_child_type": WrtType.to_string2(record.warrantExData.type),
            "stock_owner": merge_qot_mkt_stock_str(
                record.warrantExData.owner.market,
                record.warrantExData.owner.code) if record.HasField('warrantExData') else (
                merge_qot_mkt_stock_str(
                    record.optionExData.owner.market,
                    record.optionExData.owner.code) if record.HasField('optionExData')
                else ""),
            "listing_date": "N/A" if record.HasField('optionExData') else record.basic.listTime,
            "option_type": OptionType.to_string2(record.optionExData.type) if record.HasField('optionExData') else "",
            "strike_time": record.optionExData.strikeTime,
            "strike_price": record.optionExData.strikePrice if record.HasField(
                'optionExData') else NoneDataType,
            "suspension": record.optionExData.suspend if record.HasField('optionExData') else NoneDataType,
            "delisting": record.basic.delisting if record.basic.HasField('delisting') else NoneDataType,
            "main_contract": record.futureExData.isMainContract,
            "last_trade_time": record.futureExData.lastTradeTime,
        } for record in static_info_list]
        return RET_OK, "", basic_info_list


class StockFilterQuery:
    """
    Query StockFilterQuery.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, market, filter_list, plate_code, begin, num, conn_id):
        """check group_name 分组名,有同名的返回首个"""
        # 开始组包
        from futu.common.pb.Qot_StockFilter_pb2 import Request
        req = Request()
        req.c2s.begin = begin
        req.c2s.num = num

        """拆解market"""
        r, req.c2s.market = Market.to_number(market)

        """拆解plate_code"""
        if plate_code is not None:
            ret, content = split_stock_str(plate_code)
            if ret != RET_OK:
                msg = str(content)
                error_str = ERROR_STR_PREFIX + msg
                return RET_ERROR, error_str, None
            market, code = content
            req.c2s.plate.code = code
            req.c2s.plate.market = market

        ret = RET_OK
        error_str = ""
        if filter_list is not None:
            for filter_item in filter_list:
                if isinstance(filter_item, SimpleFilter):
                    filter_req = req.c2s.baseFilterList.add()
                    ret, error_str = filter_item.fill_request_pb(filter_req)
                elif isinstance(filter_item, AccumulateFilter):
                    filter_req = req.c2s.accumulateFilterList.add()
                    ret, error_str = filter_item.fill_request_pb(filter_req)
                elif isinstance(filter_item, FinancialFilter):
                    filter_req = req.c2s.financialFilterList.add()
                    ret, error_str = filter_item.fill_request_pb(filter_req)
                else :
                    ret = RET_ERROR
                    error_str = ERROR_STR_PREFIX + "the item in filter_list is wrong"

        if (ret == RET_ERROR):
            return RET_ERROR, error_str, None

        return pack_pb_req(req, ProtoId.Qot_StockFilter, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None
        #  是否最后一页了,false:非最后一页,还有窝轮记录未返回; true:已是最后一页 type = bool
        last_page = rsp_pb.s2c.lastPage
        #  该条件请求所有数据的个数 type = int32
        all_count = rsp_pb.s2c.allCount
        #   type = Qot_StockFilter.StockData
        data_list = rsp_pb.s2c.dataList
        ret_list = list()
        for item in data_list:
            data = FilterStockData(item)
            ret_list.append(data)
        return RET_OK, "", (last_page, all_count, ret_list)


class GetCodeChangeQuery:
    """
    Query GetCodeChange.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code_list, time_filter_list, type_list, conn_id):
        stock_tuple_list = []
        failure_tuple_list = []
        for stock_str in code_list:
            ret_code, content = split_stock_str(stock_str)
            if ret_code != RET_OK:
                error_str = content
                failure_tuple_list.append((ret_code, error_str))
                continue
            market_code, stock_code = content
            stock_tuple_list.append((market_code, stock_code))
        if len(failure_tuple_list) > 0:
            error_str = '\n'.join([x[1] for x in failure_tuple_list])
            return RET_ERROR, error_str, None

        # 开始组包
        from futu.common.pb.Qot_GetCodeChange_pb2 import Request
        req = Request()
        req.c2s.placeHolder = 0
        for market_code, stock_code in stock_tuple_list:
            stock_inst = req.c2s.securityList.add()
            stock_inst.market = market_code
            stock_inst.code = stock_code

        for type in type_list:
            _, n = CodeChangeType.to_number(type)
            req.c2s.typeList.append(n)

        for time_filter in time_filter_list:
            time_filter_inst = req.c2s.timeFilterList.add()
            _, time_filter_inst.type = TimeFilterType.to_number(time_filter.type)
            time_filter_inst.beginTime = time_filter.begin_time
            time_filter_inst.endTime = time_filter.end_time

        return pack_pb_req(req, ProtoId.Qot_GetCodeChange, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None
        ret_list = list()
        #  股票代码更换信息，目前仅有港股数据 type = Qot_GetCodeChange.CodeChangeInfo
        code_change_list = rsp_pb.s2c.codeChangeList
        for item in code_change_list:
            data = {}
            #  CodeChangeType,代码变化或者新增临时代码的事件类型 type = int32
            data["code_change_info_type"] = CodeChangeType.to_string2(
                item.type)
            #  主代码，在创业板转主板中表示主板 type = code
            data["code"] = merge_qot_mkt_stock_str(
                item.security.market, item.security.code)
            #  关联代码，在创业板转主板中表示创业板，在剩余事件中表示临时代码 type = code
            data["related_code"] = merge_qot_mkt_stock_str(
                item.relatedSecurity.market, item.relatedSecurity.code)
            #  公布时间 type = string
            data["public_time"] = item.publicTime
            #  生效时间 type = string
            data["effective_time"] = item.effectiveTime
            #  结束时间，在创业板转主板事件不存在该字段，在剩余事件表示临时代码交易结束时间 type = string
            data["end_time"] = item.endTime
            ret_list.append(data)
        return RET_OK, "", ret_list


class GetIpoListQuery:
    """
    Query GetIpoListQuery.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, conn_id, market):
        # 开始组包
        from futu.common.pb.Qot_GetIpoList_pb2 import Request
        req = Request()
        _, req.c2s.market = Market.to_number(market)

        return pack_pb_req(req, ProtoId.Qot_GetIpoList, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        ret_list = []
        for pb_item in rsp_pb.s2c.ipoList:
            data = {}

            set_item_from_pb(data, pb_item.basic, pb_field_map_BasicIpoData)
            if pb_item.HasField('cnExData'):
                set_item_from_pb(data, pb_item.cnExData, pb_field_map_CNIpoExData)
            else:
                set_item_none(data, pb_field_map_CNIpoExData)

            if pb_item.HasField('hkExData'):
                set_item_from_pb(data, pb_item.hkExData, pb_field_map_HKIpoExData)
            else:
                set_item_none(data, pb_field_map_HKIpoExData)

            if pb_item.HasField('usExData'):
                set_item_from_pb(data, pb_item.usExData, pb_field_map_USIpoExData)
            else:
                set_item_none(data, pb_field_map_USIpoExData)

            ret_list.append(data)
        return RET_OK, "", ret_list

class GetFutureInfoQuery:
    """
    Query GetFutureInfo.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code_list, conn_id):
        """check code_list 股票列表"""
        stock_tuple_list = []
        failure_tuple_list = []
        for stock_str in code_list:
            ret_code, content = split_stock_str(stock_str)
            if ret_code != RET_OK:
                error_str = content
                failure_tuple_list.append((ret_code, error_str))
                continue
            market_code, stock_code = content
            stock_tuple_list.append((market_code, stock_code))
        if len(failure_tuple_list) > 0:
            error_str = '\n'.join([x[1] for x in failure_tuple_list])
            return RET_ERROR, error_str, None

        # 开始组包
        from futu.common.pb.Qot_GetFutureInfo_pb2 import Request
        req = Request()
        for market_code, stock_code in stock_tuple_list:
            stock_inst = req.c2s.securityList.add()
            stock_inst.market = market_code
            stock_inst.code = stock_code

        return pack_pb_req(req, ProtoId.Qot_GetFutureInfo, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None
        ret_list = list()
        #  期货合约资料 type = Qot_GetFutureInfo.FutureInfo
        future_info_list = rsp_pb.s2c.futureInfoList
        for item in future_info_list:
            data = {}
            #  合约名称 type = string
            data['name'] = item.name
            #  合约代码 type = string
            data['code'] = merge_qot_mkt_stock_str(item.security.market,item.security.code)
            #  最后交易日，只有非主连期货合约才有该字段 type = string
            data['last_trade_time'] = item.lastTradeTime
            if item.HasField('owner'):
                data['owner'] = merge_qot_mkt_stock_str(item.owner.market,item.owner.code)
            else:
                data['owner'] = item.ownerOther
            #  交易所 type = string
            data['exchange'] = item.exchange
            #  合约类型 type = string
            data['type'] = item.contractType
            #  合约规模 type = double
            data['size'] = item.contractSize
            #  合约规模的单位 type = string
            data['size_unit'] = item.contractSizeUnit
            #  报价货币 type = string
            data['price_currency'] = item.quoteCurrency
            #  报价单位 type = string
            data['price_unit'] = item.quoteUnit
            #  最小变动单位 type = double
            data['min_change'] = item.minVar
            #  最小变动单位的单位 type = string
            data['min_change_unit'] = item.minVarUnit
            #  交易时间 type = Qot_GetFutureInfo.TradeTime
            trade_time = ''
            for time_range in item.tradeTime:
                if (len(trade_time) > 0):
                    trade_time += ', '
                begin_neg = time_range.begin < 0
                if begin_neg:
                    begin = time.strftime("%M:%S", time.localtime(24 * 60 + time_range.begin))
                else:
                    begin = time.strftime("%M:%S", time.localtime(time_range.begin))
                end = time.strftime("%M:%S", time.localtime(abs(time_range.end)))
                trade_time += '(%s%s - %s)' % (begin, '(T-1)' if begin_neg else '', end)

            data['trade_time'] = trade_time
            #  所在时区 type = string
            data['time_zone'] = item.timeZone
            #  交易所规格 type = string
            data['exchange_format_url'] = item.exchangeFormatUrl
            ret_list.append(data)
        return RET_OK, "", ret_list

class TestCmd:
    @classmethod
    def pack_req(cls, cmd, params):

        from futu.common.pb.TestCmd_pb2 import Request
        req = Request()
        req.c2s.cmd = cmd
        req.c2s.params = params

        return pack_pb_req(req, ProtoId.TestCmd, 0)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        """Unpack the init connect response"""
        ret_type = rsp_pb.retType
        ret_msg = rsp_pb.retMsg

        if ret_type != RET_OK:
            return RET_ERROR, ret_msg, None

        res = {}
        if rsp_pb.HasField('s2c'):
            res['cmd'] = rsp_pb.s2c.cmd
            res['result'] = rsp_pb.s2c.result
        else:
            return RET_ERROR, "rsp_pb error", None

        return RET_OK, "", res


class UpdatePriceReminder:
    @classmethod
    def unpack_rsp(cls, rsp_pb):
        """Unpack the init connect response"""
        ret_type = rsp_pb.retType
        ret_msg = rsp_pb.retMsg

        if ret_type != RET_OK:
            return RET_ERROR, ret_msg, None

        res = {}
        if rsp_pb.HasField('s2c'):
            res['code'] = merge_qot_mkt_stock_str(rsp_pb.s2c.security.market,
                                                  rsp_pb.s2c.security.code)
            res['price'] = rsp_pb.s2c.price
            res['change_rate'] = rsp_pb.s2c.changeRate
            res['market_status'] = PriceReminderMarketStatus.to_string2(rsp_pb.s2c.marketStatus)
            res['content'] = rsp_pb.s2c.content
            res['note'] = rsp_pb.s2c.note
            if rsp_pb.s2c.key is not None:
                res['key'] = rsp_pb.s2c.key
            if rsp_pb.s2c.type is not None:
                res['reminder_type'] = PriceReminderType.to_string2(rsp_pb.s2c.type)
            if rsp_pb.s2c.setValue is not None:
                res['set_value'] = rsp_pb.s2c.setValue
            if rsp_pb.s2c.curValue is not None:
                res['cur_value'] = rsp_pb.s2c.curValue
        else:
            return RET_ERROR, "rsp_pb error", None

        return RET_OK, "", res

class SetPriceReminderQuery:
    """
    Query SetPriceReminder.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, op, key, reminder_type, reminder_freq, value, note, conn_id):
        """check stock_code 股票"""
        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            error_str = content
            return RET_ERROR, error_str, None
        market_code, stock_code = content

        # 开始组包
        from futu.common.pb.Qot_SetPriceReminder_pb2 import Request
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code
        _, req.c2s.op = SetPriceReminderOp.to_number(op)

        if key is not None:
            req.c2s.key = key
        if reminder_type is not None:
            _, req.c2s.type = PriceReminderType.to_number(reminder_type)
        if reminder_freq is not None:
            _, req.c2s.freq = PriceReminderFreq.to_number(reminder_freq)
        if value is not None:
            req.c2s.value = value
        if note is not None:
            req.c2s.note = note

        return pack_pb_req(req, ProtoId.Qot_SetPriceReminder, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        key = rsp_pb.s2c.key
        return RET_OK, "", key


class GetPriceReminderQuery:
    """
    Query GetPriceReminder.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, market, conn_id):
        """check stock_code 查询股票下的到价提醒项"""
        market_code = 0
        stock_code = ''
        if code is not None:
            ret, content = split_stock_str(code)
            if ret == RET_ERROR:
                error_str = content
                return RET_ERROR, error_str, None
            market_code, stock_code = content

        # 开始组包
        from futu.common.pb.Qot_GetPriceReminder_pb2 import Request
        req = Request()
        if code is not None:
            req.c2s.security.market = market_code
            req.c2s.security.code = stock_code
        elif market is not None and market is not Market.NONE:
            _, req.c2s.market = Market.to_number(market)
        return pack_pb_req(req, ProtoId.Qot_GetPriceReminder, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        ret_list = list()
        #  到价提醒 type = Qot_GetPriceReminder.PriceReminder
        for item in rsp_pb.s2c.priceReminderList:
            stock_code = merge_qot_mkt_stock_str(item.security.market, item.security.code)
            #  提醒信息列表 type = Qot_GetPriceReminder.PriceReminderItem
            for sub_item in item.itemList:
                data = {}
                data["code"] = stock_code
                #  每个提醒的唯一标识 type = int64
                data["key"] = sub_item.key
                #  Qot_Common::PriceReminderType 提醒类型 type = int32
                data["reminder_type"] = PriceReminderType.to_string2(sub_item.type)
                #  Qot_Common::PriceReminderFreq 提醒频率类型 type = int32
                data["reminder_freq"] = PriceReminderFreq.to_string2(sub_item.freq)
                #  提醒参数值 type = double
                data["value"] = sub_item.value
                #  该提醒设置是否生效。false不生效，true生效 type = bool
                data["enable"] = sub_item.isEnable
                #  用户设置到价提醒时的标注 type = string
                data["note"] = sub_item.note
                ret_list.append(data)
        return RET_OK, "", ret_list

class GetUserSecurityGroupQuery:
    """
    Query GetUserSecurityGroup.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, group_type, conn_id):
        """check group_type GroupType,自选股分组类型。"""

        # 开始组包
        from futu.common.pb.Qot_GetUserSecurityGroup_pb2 import Request
        req = Request()
        _, req.c2s.groupType = UserSecurityGroupType.to_number(group_type)
        return pack_pb_req(req, ProtoId.Qot_GetUserSecurityGroup, conn_id)


    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        ret_list = list()
        #  自选股分组列表 type = Qot_GetUserSecurityGroup.GroupData
        group_list = rsp_pb.s2c.groupList
        for item in group_list:
            data = {}
            #  自选股分组名字 type = string
            data["group_name"] = item.groupName
            #  GroupType,自选股分组类型。 type = int32
            data["group_type"] = UserSecurityGroupType.to_string2(item.groupType)
            ret_list.append(data)

        return RET_OK, "", ret_list

class GetMarketStateQuery:
    """
    Query GetMarketState.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code_list, conn_id):
        """check code_list 股票列表"""
        stock_tuple_list = []
        failure_tuple_list = []
        for stock_str in code_list:
            ret_code, content = split_stock_str(stock_str)
            if ret_code != RET_OK:
                error_str = content
                failure_tuple_list.append((ret_code, error_str))
                continue
            market_code, stock_code = content
            stock_tuple_list.append((market_code, stock_code))
        if len(failure_tuple_list) > 0:
            error_str = '\n'.join([x[1] for x in failure_tuple_list])
            return RET_ERROR, error_str, None

        # 开始组包
        from futu.common.pb.Qot_GetMarketState_pb2 import Request
        req = Request()
        for market_code, stock_code in stock_tuple_list:
            stock_inst = req.c2s.securityList.add()
            stock_inst.market = market_code
            stock_inst.code = stock_code

        return pack_pb_req(req, ProtoId.Qot_GetMarketState, conn_id)

    @classmethod
    def unpack(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        ret_list = list()
        #  市场状态信息 type = Qot_GetMarketState.MarketInfo
        market_info_list = rsp_pb.s2c.marketInfoList
        for item in market_info_list:
            data = {}
            ret_list.append(data)
            #  股票代码 type = code
            data["code"] = merge_qot_mkt_stock_str(item.security.market, item.security.code)
            #  股票名称 type = string
            data["stock_name"] = item.name
            #  Qot_Common.QotMarketState,市场状态 type = int32
            data["market_state"] = MarketState.to_string2(item.marketState)
        return RET_OK, "", ret_list