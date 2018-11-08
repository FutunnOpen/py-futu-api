# -*- coding: utf-8 -*-
"""
    Quote query
"""

from futu.common.utils import *



# 无数据时的值
NoneDataType = 'N/A'

class InitConnect:
    """
    A InitConnect request must be sent first
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, client_ver, client_id, recv_notify=False):

        from futu.common.pb.InitConnect_pb2 import Request
        req = Request()
        req.c2s.clientVer = client_ver
        req.c2s.clientID = client_id
        req.c2s.recvNotify = recv_notify
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
        if market not in MKT_MAP:
            error_str = ERROR_STR_PREFIX + " market is %s, which is not valid. (%s)" \
                                           % (market, ",".join([x for x in MKT_MAP]))
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
        mkt = MKT_MAP[market]
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
        # convert to list format that we use
        trading_day_list = [x.time.split()[0] for x in raw_trading_day_list]

        return RET_OK, "", trading_day_list


class StockBasicInfoQuery:
    """
    Query Conversion for getting stock basic information.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, market, conn_id, stock_type='STOCK', code_list=None):

        if market not in MKT_MAP:
            error_str = ERROR_STR_PREFIX + " market is %s, which is not valid. (%s)" \
                                           % (market, ",".join([x for x in MKT_MAP]))
            return RET_ERROR, error_str, None

        if stock_type not in SEC_TYPE_MAP:
            error_str = ERROR_STR_PREFIX + " stock_type is %s, which is not valid. (%s)" \
                                           % (stock_type, ",".join([x for x in SEC_TYPE_MAP]))
            return RET_ERROR, error_str, None

        from futu.common.pb.Qot_GetStaticInfo_pb2 import Request
        req = Request()
        req.c2s.market = MKT_MAP[market]
        req.c2s.secType = SEC_TYPE_MAP[stock_type]
        if code_list is not None:
            for code in code_list:
                sec = req.c2s.securityList.add()
                ret, data = split_stock_str(code)
                if ret == RET_OK:
                    sec.market, sec.code = data
                else:
                    return RET_ERROR, data, None

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
            "stock_type": QUOTE.REV_SEC_TYPE_MAP[record.basic.secType]
                if record.basic.secType in QUOTE.REV_SEC_TYPE_MAP else SecurityType.NONE,
            "stock_child_type": QUOTE.REV_WRT_TYPE_MAP[record.warrantExData.type]
                if record.warrantExData.type in QUOTE.REV_WRT_TYPE_MAP else WrtType.NONE,
            "stock_owner":merge_qot_mkt_stock_str(
                    record.warrantExData.owner.market,
                    record.warrantExData.owner.code) if record.HasField('warrantExData') else (
                    merge_qot_mkt_stock_str(
                    record.optionExData.owner.market,
                    record.optionExData.owner.code) if record.HasField('optionExData')
                    else ""),
            "listing_date": "N/A" if record.HasField('optionExData') else record.basic.listTime,
            "option_type": QUOTE.REV_OPTION_TYPE_CLASS_MAP[record.optionExData.type]
                if record.HasField('optionExData') else "",
            "strike_time": record.optionExData.strikeTime,
            "strike_price": record.optionExData.strikePrice if record.HasField('optionExData') else NoneDataType,
            "suspension": record.optionExData.suspend if record.HasField('optionExData') else NoneDataType,
            "delisting": record.basic.delisting if record.basic.HasField('delisting') else NoneDataType
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
            snapshot_tmp['listing_date'] = "N/A" if record.HasField('optionExData') else record.basic.listTime
            snapshot_tmp['price_spread'] = record.basic.priceSpread
            snapshot_tmp['lot_size'] = record.basic.lotSize

            snapshot_tmp['equity_valid'] = False
            # equityExData
            if record.HasField('equityExData'):
                snapshot_tmp['equity_valid'] = True
                snapshot_tmp[
                    'issued_shares'] = record.equityExData.issuedShares
                snapshot_tmp[
                    'total_market_val'] = record.equityExData.issuedMarketVal
                snapshot_tmp['net_asset'] = record.equityExData.netAsset
                snapshot_tmp['net_profit'] = record.equityExData.netProfit
                snapshot_tmp[
                    'earning_per_share'] = record.equityExData.earningsPershare
                snapshot_tmp[
                    'outstanding_shares'] = record.equityExData.outstandingShares
                snapshot_tmp[
                    'circular_market_val'] = record.equityExData.outstandingMarketVal
                snapshot_tmp[
                    'net_asset_per_share'] = record.equityExData.netAssetPershare
                snapshot_tmp['ey_ratio'] = record.equityExData.eyRate
                snapshot_tmp['pe_ratio'] = record.equityExData.peRate
                snapshot_tmp['pb_ratio'] = record.equityExData.pbRate
                snapshot_tmp['pe_ttm_ratio'] = record.equityExData.peTTMRate

            snapshot_tmp['wrt_valid'] = False
            if record.basic.type == SEC_TYPE_MAP[SecurityType.WARRANT]:
                snapshot_tmp['wrt_valid'] = True
                snapshot_tmp[
                    'wrt_conversion_ratio'] = record.warrantExData.conversionRate
                snapshot_tmp['wrt_type'] = QUOTE.REV_WRT_TYPE_MAP[
                    record.warrantExData.warrantType]
                snapshot_tmp[
                    'wrt_strike_price'] = record.warrantExData.strikePrice
                snapshot_tmp[
                    'wrt_maturity_date'] = record.warrantExData.maturityTime
                snapshot_tmp[
                    'wrt_end_trade'] = record.warrantExData.endTradeTime
                snapshot_tmp['stock_owner'] = merge_qot_mkt_stock_str(
                    record.warrantExData.owner.market,
                    record.warrantExData.owner.code)
                snapshot_tmp[
                    'wrt_recovery_price'] = record.warrantExData.recoveryPrice
                snapshot_tmp[
                    'wrt_street_vol'] = record.warrantExData.streetVolumn
                snapshot_tmp[
                    'wrt_issue_vol'] = record.warrantExData.issueVolumn
                snapshot_tmp[
                    'wrt_street_ratio'] = record.warrantExData.streetRate
                snapshot_tmp['wrt_delta'] = record.warrantExData.delta
                snapshot_tmp[
                    'wrt_implied_volatility'] = record.warrantExData.impliedVolatility
                snapshot_tmp['wrt_premium'] = record.warrantExData.premium

            snapshot_tmp['option_valid'] = False
            if record.basic.type == SEC_TYPE_MAP[SecurityType.DRVT]:
                snapshot_tmp['option_valid'] = True
                snapshot_tmp[
                    'option_type'] = QUOTE.REV_OPTION_TYPE_CLASS_MAP[record.optionExData.type]
                snapshot_tmp['stock_owner'] = merge_qot_mkt_stock_str(
                    record.optionExData.owner.market, record.optionExData.owner.code)
                snapshot_tmp[
                    'strike_time'] = record.optionExData.strikeTime
                snapshot_tmp[
                    'option_strike_price'] = record.optionExData.strikePrice
                snapshot_tmp[
                    'option_contract_size'] = record.optionExData.contractSize
                snapshot_tmp[
                    'option_open_interest'] = record.optionExData.openInterest
                snapshot_tmp['option_implied_volatility'] = record.optionExData.impliedVolatility
                snapshot_tmp[
                    'option_premium'] = record.optionExData.premium
                snapshot_tmp[
                    'option_delta'] = record.optionExData.delta
                snapshot_tmp[
                    'option_gamma'] = record.optionExData.gamma
                snapshot_tmp[
                    'option_vega'] = record.optionExData.vega
                snapshot_tmp['option_theta'] = record.optionExData.theta
                snapshot_tmp['option_rho'] = record.optionExData.rho
            else:
                pass
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
        req.c2s.market = MKT_MAP[market]
        req.c2s.plateSetType = PLATE_CLASS_MAP[plate_class]

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
    def pack_req(cls, plate_code, conn_id):

        ret_code, content = split_stock_str(plate_code)
        if ret_code != RET_OK:
            msg = content
            error_str = ERROR_STR_PREFIX + msg
            return RET_ERROR, error_str, None

        market, code = content
        if market not in QUOTE.REV_MKT_MAP:
            error_str = ERROR_STR_PREFIX + "market is %s, which is not valid. (%s)" \
                                           % (market, ",".join([x for x in MKT_MAP]))
            return RET_ERROR, error_str, None
        from futu.common.pb.Qot_GetPlateSecurity_pb2 import Request
        req = Request()
        req.c2s.plate.market = market
        req.c2s.plate.code = code

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
            stock_tmp['code'] = merge_qot_mkt_stock_str(record.basic.security.market, record.basic.security.code)
            stock_tmp['stock_name'] = record.basic.name
            stock_tmp['list_time'] = record.basic.listTime
            stock_tmp['stock_type'] = QUOTE.REV_SEC_TYPE_MAP[record.basic.secType] if record.basic.secType in QUOTE.REV_SEC_TYPE_MAP else SecurityType.NONE
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
                "code": merge_qot_mkt_stock_str(rsp_pb.s2c.security.market, rsp_pb.s2c.security.code)
            } for record in raw_broker_bid]

        raw_broker_ask = rsp_pb.s2c.brokerAskList
        ask_list = []
        if raw_broker_ask is not None:
            ask_list = [{
                "ask_broker_id": record.id,
                "ask_broker_name": record.name,
                "ask_broker_pos": record.pos,
                "code": merge_qot_mkt_stock_str(rsp_pb.s2c.security.market, rsp_pb.s2c.security.code)
            } for record in raw_broker_ask]

        return RET_OK, "", (stock_code, bid_list, ask_list)


class GetHistoryKlineQuery:
    """
    Query Conversion for getting historic Kline data.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, start_date, end_date, ktype, autype, fields,
                 max_num, conn_id):

        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            error_str = content
            return RET_ERROR, error_str, None

        market_code, stock_code = content

        # check k line type
        if ktype not in KTYPE_MAP:
            error_str = ERROR_STR_PREFIX + "ktype is %s, which is not valid. (%s)" \
                                           % (ktype, ", ".join([x for x in KTYPE_MAP]))
            return RET_ERROR, error_str, None

        if autype not in AUTYPE_MAP:
            error_str = ERROR_STR_PREFIX + "autype is %s, which is not valid. (%s)" \
                                           % (autype, ", ".join([str(x) for x in AUTYPE_MAP]))
            return RET_ERROR, error_str, None

        from futu.common.pb.Qot_GetHistoryKL_pb2 import Request

        req = Request()
        req.c2s.rehabType = AUTYPE_MAP[autype]
        req.c2s.klType = KTYPE_MAP[ktype]
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code
        if start_date:
            req.c2s.beginTime = start_date
        if end_date:
            req.c2s.endTime = end_date
        req.c2s.maxAckKLNum = max_num
        req.c2s.needKLFieldsFlag = KL_FIELD.kl_fields_to_flag_val(fields)

        return pack_pb_req(req, ProtoId.Qot_GetHistoryKL, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):

        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        has_next = False
        next_time = ""
        if rsp_pb.s2c.HasField('nextKLTime'):
            has_next = True
            next_time = rsp_pb.s2c.nextKLTime

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

        return RET_OK, "", (list_ret, has_next, next_time)


class RequestHistoryKlineQuery:
    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, start_date, end_date, ktype, autype, fields,
                 max_num, conn_id, next_req_key):
        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            error_str = content
            return RET_ERROR, error_str, None

        market_code, stock_code = content

        # check k line type
        if ktype not in KTYPE_MAP:
            error_str = ERROR_STR_PREFIX + "ktype is %s, which is not valid. (%s)" \
                        % (ktype, ", ".join([x for x in KTYPE_MAP]))
            return RET_ERROR, error_str, None

        if autype not in AUTYPE_MAP:
            error_str = ERROR_STR_PREFIX + "autype is %s, which is not valid. (%s)" \
                        % (autype, ", ".join([str(x) for x in AUTYPE_MAP]))
            return RET_ERROR, error_str, None

        from futu.common.pb.Qot_RequestHistoryKL_pb2 import Request

        req = Request()
        req.c2s.rehabType = AUTYPE_MAP[autype]
        req.c2s.klType = KTYPE_MAP[ktype]
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

class ExrightQuery:
    """
    Query Conversion for getting exclude-right information of stock.
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
        from futu.common.pb.Qot_GetRehab_pb2 import Request
        req = Request()
        for market_code, stock_code in stock_tuple_list:
            stock_inst = req.c2s.securityList.add()
            stock_inst.market = market_code
            stock_inst.code = stock_code

        return pack_pb_req(req, ProtoId.Qot_GetRehab, conn_id)

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

        raw_exr_list = rsp_pb.s2c.securityRehabList
        exr_list = []
        for stock_rehab in raw_exr_list:
            code = merge_qot_mkt_stock_str(stock_rehab.security.market,
                                        stock_rehab.security.code)
            for rehab in stock_rehab.rehabList:
                stock_rehab_tmp = {}
                stock_rehab_tmp['code'] = code
                stock_rehab_tmp['ex_div_date'] = rehab.time.split()[0]
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
                    stock_rehab_tmp[
                        'stk_spo_ratio'] = rehab.addBase / rehab.addErt
                    stock_rehab_tmp['stk_spo_price'] = rehab.addPrice
                if act_flag & KLRehabFlag.ALLOT:
                    stock_rehab_tmp[
                        'allotment_ratio'] = rehab.allotBase / rehab.allotErt
                    stock_rehab_tmp['allotment_price'] = rehab.allotPrice
                if act_flag & KLRehabFlag.TRANSFER:
                    stock_rehab_tmp[
                        'per_share_trans_ratio'] = rehab.transferBase / rehab.transferErt
                if act_flag & KLRehabFlag.BONUS:
                    stock_rehab_tmp[
                        'per_share_div_ratio'] = rehab.bonusBase / rehab.bonusErt
                if act_flag & KLRehabFlag.JOIN:
                    stock_rehab_tmp[
                        'join_ratio'] = rehab.joinBase / rehab.joinErt
                if act_flag & KLRehabFlag.SPLIT:
                    stock_rehab_tmp[
                        'split_ratio'] = rehab.splitBase / rehab.splitErt
                exr_list.append(stock_rehab_tmp)

        return RET_OK, "", exr_list


class SubscriptionQuery:
    """
    Query Conversion for getting user's subscription information.
    """
    def __init__(self):
        pass

    @classmethod
    def pack_sub_or_unsub_req(cls, code_list, subtype_list, is_sub, conn_id, is_first_push, reg_or_unreg_push):

        stock_tuple_list = []
        for code in code_list:
            ret_code, content = split_stock_str(code)
            if ret_code != RET_OK:
                return ret_code, content, None
            market_code, stock_code = content
            stock_tuple_list.append((market_code, stock_code))

        from futu.common.pb.Qot_Sub_pb2 import Request
        req = Request()
        for market_code, stock_code in stock_tuple_list:
            stock_inst = req.c2s.securityList.add()
            stock_inst.code = stock_code
            stock_inst.market = market_code
        for subtype in subtype_list:
            req.c2s.subTypeList.append(SUBTYPE_MAP[subtype])
        req.c2s.isSubOrUnSub = is_sub
        req.c2s.isFirstPush = is_first_push
        req.c2s.isRegOrUnRegPush = reg_or_unreg_push

        return pack_pb_req(req, ProtoId.Qot_Sub, conn_id)

    @classmethod
    def pack_subscribe_req(cls, code_list, subtype_list, conn_id, is_first_push):
        return SubscriptionQuery.pack_sub_or_unsub_req(code_list, subtype_list, True, conn_id, is_first_push, True)

    @classmethod
    def unpack_subscribe_rsp(cls, rsp_pb):

        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        return RET_OK, "", None

    @classmethod
    def pack_unsubscribe_req(cls, code_list, subtype_list, conn_id):

        return SubscriptionQuery.pack_sub_or_unsub_req(code_list, subtype_list, False, conn_id, False, False)

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
                if sub_info.subType not in QUOTE.REV_SUBTYPE_MAP:
                    logger.error("error subtype:{}".format(sub_info.subType))
                    continue

                sub_info_tmp['subtype'] = QUOTE.REV_SUBTYPE_MAP[sub_info.subType]
                sub_info_tmp['code_list'] = []
                for stock in sub_info.securityList:
                    sub_info_tmp['code_list'].append(merge_qot_mkt_stock_str(int(stock.market), stock.code),)

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
            req.c2s.subTypeList.append(SUBTYPE_MAP[subtype])
        req.c2s.isRegOrUnReg = is_push
        req.c2s.isFirstPush = True if is_first_push else False

        return pack_pb_req(req, ProtoId.Qot_RegQotPush, conn_id)

    @classmethod
    def pack_push_req(cls, code_list, subtype_list, conn_id, is_first_push):

        return SubscriptionQuery.pack_push_or_unpush_req(code_list, subtype_list, True, conn_id, is_first_push)

    @classmethod
    def pack_unpush_req(cls, code_list, subtype_list, conn_id, is_first_push=False):

        return SubscriptionQuery.pack_push_or_unpush_req(code_list, subtype_list, False, conn_id, is_first_push)


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

        quote_list = [{
            'code': merge_qot_mkt_stock_str(int(record.security.market), record.security.code),
            'data_date': record.updateTime.split()[0],
            'data_time': record.updateTime.split()[1],
            'last_price': record.curPrice,
            'open_price': record.openPrice,
            'high_price': record.highPrice,
            'low_price': record.lowPrice,
            'prev_close_price': record.lastClosePrice,
            'volume': int(record.volume),
            'turnover': record.turnover,
            'turnover_rate': record.turnoverRate,
            'amplitude': record.amplitude,
            'suspension': record.isSuspended,
            'listing_date': record.listTime,
            'price_spread': record.priceSpread if record.HasField('priceSpread') else 0,
            'dark_status': QUOTE.REV_DARK_STATUS_MAP[record.darkStatus] if record.HasField('darkStatus') else DarkStatus.NONE,
            "strike_price": record.optionExData.strikePrice,
            "contract_size": record.optionExData.contractSize,
            "open_interest": record.optionExData.openInterest,
            "implied_volatility": record.optionExData.impliedVolatility,
            "premium": record.optionExData.premium,
            "delta": record.optionExData.delta,
            "gamma": record.optionExData.gamma,
            'vega': record.optionExData.vega,
            'theta': record.optionExData.theta,
            'rho': record.optionExData.rho,
        } for record in raw_quote_list]

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
            "ticker_direction": str(QUOTE.REV_TICKER_DIRECTION[record.dir]) if record.dir in QUOTE.REV_TICKER_DIRECTION else "",
            "sequence": record.sequence,
            "recv_timestamp":record.recvTime,
            "type": QUOTE.REV_TICKER_TYPE_MAP[record.type] if record.type in QUOTE.REV_TICKER_TYPE_MAP else TickerType.UNKNOWN,
			"push_data_type":QUOTE.REV_PUSH_DATA_TYPE_MAP[record.pushDataType] if record.pushDataType in QUOTE.REV_PUSH_DATA_TYPE_MAP else PushDataType.NONE,
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

        if ktype not in KTYPE_MAP:
            error_str = ERROR_STR_PREFIX + "ktype is %s, which is not valid. (%s)" \
                                           % (ktype, ", ".join([x for x in KTYPE_MAP]))
            return RET_ERROR, error_str, None

        if autype not in AUTYPE_MAP:
            error_str = ERROR_STR_PREFIX + "autype is %s, which is not valid. (%s)" \
                                           % (autype, ", ".join([str(x) for x in AUTYPE_MAP]))
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
        req.c2s.rehabType = AUTYPE_MAP[autype]
        req.c2s.reqNum = num
        req.c2s.klType = KTYPE_MAP[ktype]

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

        if rsp_pb.s2c.rehabType != AUTYPE_MAP[AuType.QFQ]:
            return RET_ERROR, "kline push only support AuType.QFQ", None

        kl_type = QUOTE.REV_KTYPE_MAP[rsp_pb.s2c.klType] if rsp_pb.s2c.klType in QUOTE.REV_KTYPE_MAP else None
        if not kl_type:
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
    def pack_req(cls, code, conn_id):

        ret, content = split_stock_str(code)
        if ret == RET_ERROR:
            error_str = content
            return RET_ERROR, error_str, None

        market_code, stock_code = content
        from futu.common.pb.Qot_GetOrderBook_pb2 import Request
        req = Request()
        req.c2s.security.market = market_code
        req.c2s.security.code = stock_code
        req.c2s.num = 10

        return pack_pb_req(req, ProtoId.Qot_GetOrderBook, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):

        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, []

        raw_order_book_ask = rsp_pb.s2c.orderBookAskList
        raw_order_book_bid = rsp_pb.s2c.orderBookBidList

        order_book = {}
        order_book['code'] = merge_qot_mkt_stock_str(rsp_pb.s2c.security.market, rsp_pb.s2c.security.code)
        order_book['Bid'] = []
        order_book['Ask'] = []

        for record in raw_order_book_bid:
            order_book['Bid'].append((record.price, record.volume,
                                      record.orederCount))
        for record in raw_order_book_ask:
            order_book['Ask'].append((record.price, record.volume,
                                      record.orederCount))

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
            code = merge_qot_mkt_stock_str(record.security.market, record.security.code)
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
    def pack_req(cls,user_id, conn_id):

        from futu.common.pb.GetGlobalState_pb2 import Request
        req = Request()
        req.c2s.userID = user_id
        return pack_pb_req(req, ProtoId.GetGlobalState, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):

        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        state = rsp_pb.s2c
        state_dict = {
            'market_sz': QUOTE.REV_MARKET_STATE_MAP[state.marketSZ]
                    if state.marketSZ in QUOTE.REV_MARKET_STATE_MAP else MarketState.NONE,
            'market_us': QUOTE.REV_MARKET_STATE_MAP[state.marketUS]
                    if state.marketUS in QUOTE.REV_MARKET_STATE_MAP else MarketState.NONE,
            'market_sh': QUOTE.REV_MARKET_STATE_MAP[state.marketSH]
                    if state.marketSH in QUOTE.REV_MARKET_STATE_MAP else MarketState.NONE,
            'market_hk': QUOTE.REV_MARKET_STATE_MAP[state.marketHK]
                    if state.marketHK in QUOTE.REV_MARKET_STATE_MAP else MarketState.NONE,
            'market_hkfuture': QUOTE.REV_MARKET_STATE_MAP[state.marketHKFuture]
                    if state.marketHKFuture in QUOTE.REV_MARKET_STATE_MAP else MarketState.NONE,

            'server_ver': str(state.serverVer),
            'trd_logined': "1" if state.trdLogined else "0",
            'timestamp': str(state.time),
            'qot_logined': "1" if state.qotLogined else "0",
            'local_timestamp': state.localTime if state.HasField('localTime') else time.time(),
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

        tmp_type = rsp_pb.s2c.type

        notify_type = SysNoitfy.REV_SYS_EVENT_TYPE_MAP[tmp_type] if tmp_type in SysNoitfy.REV_SYS_EVENT_TYPE_MAP else SysNotifyType.NONE
        sub_type = GtwEventType.NONE
        msg = ""
        if notify_type == SysNotifyType.GTW_EVENT:
            tmp_type = rsp_pb.s2c.event.eventType
            if tmp_type in SysNoitfy.REV_GTW_EVENT_MAP:
                sub_type = SysNoitfy.REV_GTW_EVENT_MAP[tmp_type]
            msg = rsp_pb.s2c.event.desc

        return RET_OK, (notify_type, sub_type, msg)


class MultiPointsHisKLine:
    """
    Query MultiPointsHisKLine
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code_list, dates, fields, ktype, autype, max_req,
                 no_data_mode, conn_id):

        list_req_stock = []
        for code in code_list:
            ret, content = split_stock_str(code)
            if ret == RET_ERROR:
                return RET_ERROR, content, None
            else:
                list_req_stock.append(content)

        for x in dates:
            ret, msg = check_date_str_format(x)
            if ret != RET_OK:
                return ret, msg, None

        if ktype not in KTYPE_MAP:
            error_str = ERROR_STR_PREFIX + "ktype is %s, which is not valid. (%s)" \
                                           % (ktype, ", ".join([x for x in KTYPE_MAP]))
            return RET_ERROR, error_str, None

        if autype not in AUTYPE_MAP:
            error_str = ERROR_STR_PREFIX + "autype is %s, which is not valid. (%s)" \
                                           % (autype, ", ".join([str(x) for x in AUTYPE_MAP]))
            return RET_ERROR, error_str, None

        from futu.common.pb.Qot_GetHistoryKLPoints_pb2 import Request
        req = Request()
        req.c2s.needKLFieldsFlag = KL_FIELD.kl_fields_to_flag_val(fields)
        req.c2s.rehabType = AUTYPE_MAP[autype]
        req.c2s.klType = KTYPE_MAP[ktype]
        req.c2s.noDataMode = no_data_mode
        req.c2s.maxReqSecurityNum = max_req
        for market_code, code in list_req_stock:
            stock_inst = req.c2s.securityList.add()
            stock_inst.market = market_code
            stock_inst.code = code
        for date_ in dates:
            req.c2s.timeList.append(date_)

        return pack_pb_req(req, ProtoId.Qot_GetHistoryKLPoints, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):

        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        has_next = rsp_pb.s2c.hasNext if rsp_pb.s2c.HasField(
            'hasNext') else False

        list_ret = []
        dict_data = {}
        raw_kline_points = rsp_pb.s2c.klPointList

        for raw_kline in raw_kline_points:
            code = merge_qot_mkt_stock_str(raw_kline.security.market,
                                         raw_kline.security.code)
            for raw_kl in raw_kline.klList:
                dict_data['code'] = code
                dict_data['time_point'] = raw_kl.reqTime
                dict_data['data_status'] = QUOTE.REV_KLDATA_STATUS_MAP[raw_kl.status] if raw_kl.status in QUOTE.REV_KLDATA_STATUS_MAP else KLDataStatus.NONE
                dict_data['time_key'] = raw_kl.kl.time

                dict_data['open'] = raw_kl.kl.openPrice if raw_kl.kl.HasField(
                    'openPrice') else 0
                dict_data['high'] = raw_kl.kl.highPrice if raw_kl.kl.HasField(
                    'highPrice') else 0
                dict_data['low'] = raw_kl.kl.lowPrice if raw_kl.kl.HasField(
                    'lowPrice') else 0
                dict_data[
                    'close'] = raw_kl.kl.closePrice if raw_kl.kl.HasField(
                        'closePrice') else 0
                dict_data['volume'] = raw_kl.kl.volume if raw_kl.kl.HasField(
                    'volume') else 0
                dict_data[
                    'turnover'] = raw_kl.kl.turnover if raw_kl.kl.HasField(
                        'turnover') else 0
                dict_data['pe_ratio'] = raw_kl.kl.pe if raw_kl.kl.HasField(
                    'pe') else 0
                dict_data[
                    'turnover_rate'] = raw_kl.kl.turnoverRate if raw_kl.kl.HasField(
                        'turnoverRate') else 0
                dict_data[
                    'change_rate'] = raw_kl.kl.changeRate if raw_kl.kl.HasField(
                        'changeRate') else 0
                dict_data[
                    'last_close'] = raw_kl.kl.lastClosePrice if raw_kl.kl.HasField(
                        'lastClosePrice') else 0

                list_ret.append(dict_data.copy())

        return RET_OK, "", (list_ret, has_next)


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
        req.c2s.referenceType = STOCK_REFERENCE_TYPE_MAP[ref_type]

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
            data['code'] = merge_qot_mkt_stock_str(info.basic.security.market, info.basic.security.code)
            # item['stock_id'] = info.basic.id
            data['lot_size'] = info.basic.lotSize
            data['stock_type'] = QUOTE.REV_SEC_TYPE_MAP[info.basic.secType] if info.basic.secType in QUOTE.REV_SEC_TYPE_MAP else SecurityType.NONE
            data['stock_name'] = info.basic.name
            data['list_time'] = info.basic.listTime
            if info.HasField('warrantExData'):
                data['wrt_valid'] = True
                data['wrt_type'] = QUOTE.REV_WRT_TYPE_MAP[info.warrantExData.type]
                data['wrt_code'] = merge_qot_mkt_stock_str(info.warrantExData.owner.market,
                                                           info.warrantExData.owner.code)
            else:
                data['wrt_valid'] = False

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
                    'plate_type': PLATE_TYPE_ID_TO_NAME[plate_info.plateType]
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


class OptionChain:
    """
    Query Conversion for getting option chain information.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, conn_id, start_date, end_date=None, option_type=OptionType.ALL, option_cond_type=OptionCondType.ALL):

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

        option_cond_type = OPTION_COND_TYPE_CLASS_MAP[option_cond_type]
        if option_cond_type == 0:
            option_cond_type = None

        option_type = OPTION_TYPE_CLASS_MAP[option_type]
        if option_type == 0:
            option_type = None

        from futu.common.pb.Qot_GetOptionChain_pb2 import Request
        req = Request()
        req.c2s.owner.market = market_code
        req.c2s.owner.code = stock_code
        req.c2s.beginTime = start_date
        req.c2s.endTime = end_date
        if option_type:
            req.c2s.type = option_type
        if option_cond_type:
            req.c2s.condition = option_cond_type

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
                        "stock_type": QUOTE.REV_SEC_TYPE_MAP[record.basic.secType]
                            if record.basic.secType in QUOTE.REV_SEC_TYPE_MAP else SecurityType.NONE,
                        "option_type": QUOTE.REV_OPTION_TYPE_CLASS_MAP[record.optionExData.type]
                            if record.HasField('optionExData') else "",
                        "stock_owner": merge_qot_mkt_stock_str(int(record.optionExData.owner.market), record.optionExData.owner.code)
                            if record.HasField('optionExData') else "",
                        "strike_time": record.optionExData.strikeTime,
                        "strike_price": record.optionExData.strikePrice if record.HasField('optionExData') else NoneDataType,
                        "suspension": record.optionExData.suspend if record.HasField('optionExData') else NoneDataType,
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

        code = merge_qot_mkt_stock_str(int(rsp_pb.s2c.security.market), rsp_pb.s2c.security.code)
        ask = [0, []]
        bid = [0, []]

        ask[0] = rsp_pb.s2c.orderDetailAsk.orderCount
        for vol in rsp_pb.s2c.orderDetailAsk.orderVol:
            ask[1].append(vol)

        bid[0] = rsp_pb.s2c.orderDetailBid.orderCount
        for vol in rsp_pb.s2c.orderDetailBid.orderVol:
            bid[1].append(vol)

        data = {
            'code': code,
            'Ask': ask,
            'Bid': bid
        }
        return RET_OK, "", data
