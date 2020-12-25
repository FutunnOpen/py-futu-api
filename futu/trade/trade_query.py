# -*- coding: utf-8 -*-
"""
    Trade query
"""
import datetime as dt
from futu.common.utils import *
from futu.quote.quote_query import pack_pb_req

# 无数据时的值
NoneDataValue = 'N/A'

def is_HKTrade_order_status_finish(status):
    val = int(status)
    if val == 3 or val == 5 or val == 6 or val == 7:
        return True
    return False


def is_USTrade_order_status_finish(status):
    val = int(status)
    if val == 3 or val == 5 or val == 6 or val == 7:
        return True
    return False


class GetAccountList:
    """Get the trade account list"""
    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, user_id, conn_id):
        from futu.common.pb.Trd_GetAccList_pb2 import Request

        req = Request()
        req.c2s.userID = user_id
        return pack_pb_req(req, ProtoId.Trd_GetAccList, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        """Convert from PLS response to user response"""
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        raw_acc_list = rsp_pb.s2c.accList
        acc_list = [{
            'acc_id': record.accID,
            'trd_env': TrdEnv.to_string2(record.trdEnv),
            'trdMarket_list': [TrdMarket.to_string2(trdMkt) for trdMkt in record.trdMarketAuthList],
            'acc_type': TrdAccType.to_string2(record.accType) if record.HasField("accType") else TrdAccType.NONE,
            'card_num': record.cardNum if record.HasField("cardNum") else "N/A",
            'security_firm': SecurityFirm.to_string2(record.securityFirm) if record.HasField('securityFirm') else SecurityFirm.NONE,
            'sim_acc_type': SimAccType.to_string2(record.simAccType) if record.HasField('simAccType') else SimAccType.NONE
        } for record in raw_acc_list]

        return RET_OK, "", acc_list


class UnlockTrade:
    """Unlock trade limitation lock"""
    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, is_unlock, password_md5, conn_id):
        """Convert from user request for trading days to PLS request"""
        from futu.common.pb.Trd_UnlockTrade_pb2 import Request
        req = Request()
        req.c2s.unlock = is_unlock
        req.c2s.pwdMD5 = password_md5

        return pack_pb_req(req, ProtoId.Trd_UnlockTrade, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        """Convert from PLS response to user response"""
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        if rsp_pb.HasField('retMsg'):
            return RET_OK, rsp_pb.retMsg, None
        return RET_OK, "", None


class SubAccPush:
    """sub acc push"""
    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, acc_id_list, conn_id):
        from futu.common.pb.Trd_SubAccPush_pb2 import Request
        req = Request()
        for x in acc_id_list:
            req.c2s.accIDList.append(x)

        return pack_pb_req(req, ProtoId.Trd_SubAccPush, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        """Convert from PLS response to user response"""
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        return RET_OK, "", None


class AccInfoQuery:
    """Class for querying information of account"""

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, acc_id, trd_market, trd_env, conn_id, refresh_cache, currency):
        from futu.common.pb.Trd_GetFunds_pb2 import Request
        req = Request()
        _, req.c2s.header.trdEnv = TrdEnv.to_number(trd_env)
        req.c2s.header.accID = acc_id
        _, req.c2s.header.trdMarket = TrdMarket.to_number(trd_market)
        if refresh_cache:
            req.c2s.refreshCache = refresh_cache
        req.c2s.currency = Currency.to_number(currency)[1]
        return pack_pb_req(req, ProtoId.Trd_GetFunds, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        """Convert from PLS response to user response"""
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        raw_funds = rsp_pb.s2c.funds
        accinfo_list = [{
            'power': raw_funds.power,
            'max_power_short': raw_funds.maxPowerShort if raw_funds.HasField('maxPowerShort') else NoneDataValue,
            'net_cash_power': raw_funds.netCashPower if raw_funds.HasField('netCashPower') else NoneDataValue,
            'total_assets': raw_funds.totalAssets,
            'cash': raw_funds.cash,
            'market_val': raw_funds.marketVal,
            'long_mv': raw_funds.longMv if raw_funds.HasField('longMv') else NoneDataValue,
            'short_mv': raw_funds.shortMv if raw_funds.HasField('shortMv') else NoneDataValue,
            'pending_asset': raw_funds.pendingAsset if raw_funds.HasField('pendingAsset') else NoneDataValue,
            'interest_charged_amount': raw_funds.debtCash if raw_funds.HasField('debtCash') else NoneDataValue,
            'frozen_cash': raw_funds.frozenCash,
            'avl_withdrawal_cash': raw_funds.avlWithdrawalCash if raw_funds.HasField('avlWithdrawalCash') else NoneDataValue,
            'max_withdrawal': raw_funds.maxWithdrawal if raw_funds.HasField('maxWithdrawal') else NoneDataValue,
            'currency': Currency.to_string2(raw_funds.currency) if raw_funds.HasField('currency') else Currency.NONE,
            'available_funds': raw_funds.availableFunds if raw_funds.HasField('availableFunds') else NoneDataValue,
            'unrealized_pl': raw_funds.unrealizedPL if raw_funds.HasField('unrealizedPL') else NoneDataValue,
            'realized_pl': raw_funds.realizedPL if raw_funds.HasField('realizedPL') else NoneDataValue,
            'risk_level': CltRiskLevel.to_string2(raw_funds.riskLevel) if raw_funds.HasField('riskLevel') else CltRiskLevel.NONE,
            'risk_status': CltRiskStatus.to_string2(raw_funds.riskStatus) if raw_funds.HasField('riskStatus') else CltRiskStatus.NONE,
            'initial_margin': raw_funds.initialMargin if raw_funds.HasField('initialMargin') else NoneDataValue,
            'margin_call_margin': raw_funds.marginCallMargin if raw_funds.HasField('marginCallMargin') else NoneDataValue,
            'maintenance_margin': raw_funds.maintenanceMargin if raw_funds.HasField('maintenanceMargin') else NoneDataValue,
            'hk_cash': NoneDataValue,
            'hk_avl_withdrawal_cash': NoneDataValue,
            'us_cash': NoneDataValue,
            'us_avl_withdrawal_cash': NoneDataValue
        }]
        for cashInfo in raw_funds.cashInfoList:
            if cashInfo.currency == Trd_Common_pb2.Currency_HKD:
                accinfo_list[0]['hk_cash'] = cashInfo.cash
                accinfo_list[0]['hk_avl_withdrawal_cash'] = cashInfo.availableBalance
            elif cashInfo.currency == Trd_Common_pb2.Currency_USD:
                accinfo_list[0]['us_cash'] = cashInfo.cash
                accinfo_list[0]['us_avl_withdrawal_cash'] = cashInfo.availableBalance
        return RET_OK, "", accinfo_list


class PositionListQuery:
    """Class for querying position list"""

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, pl_ratio_min,
                 pl_ratio_max, trd_env, acc_id, trd_mkt, conn_id, refresh_cache):
        """Convert from user request for trading days to PLS request"""
        from futu.common.pb.Trd_GetPositionList_pb2 import Request
        req = Request()
        _, req.c2s.header.trdEnv = TrdEnv.to_number(trd_env)
        req.c2s.header.accID = acc_id
        _, req.c2s.header.trdMarket = TrdMarket.to_number(trd_mkt)
        if code:
            req.c2s.filterConditions.codeList.append(code)
        if pl_ratio_min is not None:
            req.c2s.filterPLRatioMin = float(pl_ratio_min) / 100.0
        if pl_ratio_max is not None:
            req.c2s.filterPLRatioMax = float(pl_ratio_max) / 100.0
        if refresh_cache:
            req.c2s.refreshCache = refresh_cache

        return pack_pb_req(req, ProtoId.Trd_GetPositionList, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        """Convert from PLS response to user response"""
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        raw_position_list = rsp_pb.s2c.positionList

        position_list = [{
                             "code": merge_trd_mkt_stock_str(position.secMarket, position.code),
                             "stock_name": position.name,
                             "qty": position.qty,
                             "can_sell_qty": position.canSellQty,
                             "cost_price": position.costPrice if position.HasField('costPrice') else NoneDataValue,
                             "cost_price_valid": position.HasField('costPrice'),
                             "market_val": position.val,
                             "nominal_price": position.price,
                             "pl_ratio": 100 * position.plRatio if position.HasField('plRatio') else NoneDataValue,
                             "pl_ratio_valid": position.HasField('plRatio'),
                             "pl_val": position.plVal,
                             "pl_val_valid": position.HasField('plVal'),
                             "today_buy_qty": position.td_buyQty if position.HasField('td_buyQty') else NoneDataValue,
                             "today_buy_val": position.td_buyVal if position.HasField('td_buyVal') else NoneDataValue,
                             "today_pl_val": position.td_plVal if position.HasField('td_plVal') else NoneDataValue,
                             "today_sell_qty": position.td_sellQty if position.HasField('td_sellQty') else NoneDataValue,
                             "today_sell_val": position.td_sellVal if position.HasField('td_sellVal') else NoneDataValue,
                             "position_side": PositionSide.to_string2(position.positionSide),
                             "unrealized_pl": position.unrealizedPL if position.HasField('unrealizedPL') else NoneDataValue,
                             "realized_pl": position.realizedPL if position.HasField('realizedPL') else NoneDataValue
                         } for position in raw_position_list]
        return RET_OK, "", position_list


class OrderListQuery:
    """Class for querying list queue"""
    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, order_id, status_filter_list, code, start, end,
                 trd_env, acc_id, trd_mkt, conn_id, refresh_cache):
        """Convert from user request for trading days to PLS request"""
        from futu.common.pb.Trd_GetOrderList_pb2 import Request
        req = Request()
        _, req.c2s.header.trdEnv = TrdEnv.to_number(trd_env)
        req.c2s.header.accID = acc_id
        _, req.c2s.header.trdMarket = TrdMarket.to_number(trd_mkt)

        if code:
            req.c2s.filterConditions.codeList.append(code)
        if order_id:
            req.c2s.filterConditions.idList.append(int(order_id))

        if start:
            req.c2s.filterConditions.beginTime = start
        if end:
            req.c2s.filterConditions.endTime = end
        if refresh_cache:
            req.c2s.refreshCache = refresh_cache

        if len(status_filter_list):
            for order_status in status_filter_list:
                r, v = OrderStatus.to_number(order_status)
                if r:
                    req.c2s.filterStatusList.append(v)

        return pack_pb_req(req, ProtoId.Trd_GetOrderList, conn_id)

    @classmethod
    def parse_order(cls, rsp_pb, order):
        order_dict = {
            "code": merge_trd_mkt_stock_str(order.secMarket, order.code),
            "stock_name": order.name,
            "trd_side": TrdSide.to_string2(order.trdSide),
            "order_type": OrderType.to_string2(order.orderType),
            "order_status": OrderStatus.to_string2(order.orderStatus),
            "order_id": str(order.orderID),
            "qty": order.qty,
            "price": order.price,
            "create_time": order.createTime,
            "updated_time": order.updateTime,
            "dealt_qty": order.fillQty,
            "dealt_avg_price": order.fillAvgPrice,
            "last_err_msg": order.lastErrMsg,
            "remark": order.remark if order.HasField("remark") else "",
            "time_in_force": TimeInForce.to_string2(order.timeInForce),
            "fill_outside_rth": order.fillOutsideRTH if order.HasField("fillOutsideRTH") else 'N/A'
        }
        return order_dict

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        """Convert from PLS response to user response"""
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        raw_order_list = rsp_pb.s2c.orderList
        order_list = [OrderListQuery.parse_order(rsp_pb, order) for order in raw_order_list]
        return RET_OK, "", order_list


class PlaceOrder:
    """Palce order class"""
    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, trd_side, order_type, price, qty,
                 code, adjust_limit, trd_env, sec_mkt_str, acc_id, trd_mkt, conn_id, remark,
                 time_in_force, fill_outside_rth):
        """Convert from user request for place order to PLS request"""
        from futu.common.pb.Trd_PlaceOrder_pb2 import Request
        req = Request()
        serial_no = get_unique_id32()
        req.c2s.packetID.serialNo = serial_no
        req.c2s.packetID.connID = conn_id

        _, req.c2s.header.trdEnv = TrdEnv.to_number(trd_env)
        req.c2s.header.accID = acc_id
        _, req.c2s.header.trdMarket = TrdMarket.to_number(trd_mkt)

        _, req.c2s.trdSide = TrdSide.to_number(trd_side)
        _, req.c2s.orderType = OrderType.to_number(order_type)
        req.c2s.code = code
        req.c2s.qty = qty
        req.c2s.price = price
        req.c2s.adjustPrice = adjust_limit != 0
        req.c2s.adjustSideAndLimit = adjust_limit
        if remark is not None:
            req.c2s.remark = remark
        r, proto_qot_mkt = Market.to_number(sec_mkt_str)
        if not r:
            proto_qot_mkt = Qot_Common_pb2.QotMarket_Unknown
        proto_trd_sec_mkt = QOT_MARKET_TO_TRD_SEC_MARKET_MAP.get(proto_qot_mkt, Trd_Common_pb2.TrdSecMarket_Unknown)
        req.c2s.secMarket = proto_trd_sec_mkt
        ret, val = TimeInForce.to_number(time_in_force)
        if not ret:
            return RET_ERROR, val, None
        else:
            req.c2s.timeInForce = val

        req.c2s.fillOutsideRTH = fill_outside_rth

        return pack_pb_req(req, ProtoId.Trd_PlaceOrder, conn_id, serial_no)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        """Convert from PLS response to user response"""
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        order_id = str(rsp_pb.s2c.orderID)

        return RET_OK, "", order_id


class ModifyOrder:
    """modify order class"""
    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, modify_order_op, order_id, price, qty,
                 adjust_limit, trd_env, acc_id, trd_mkt, conn_id):
        """Convert from user request for place order to PLS request"""
        from futu.common.pb.Trd_ModifyOrder_pb2 import Request
        req = Request()
        serial_no = get_unique_id32()
        req.c2s.packetID.serialNo = serial_no
        req.c2s.packetID.connID = conn_id

        _, req.c2s.header.trdEnv = TrdEnv.to_number(trd_env)
        req.c2s.header.accID = acc_id
        _, req.c2s.header.trdMarket = TrdMarket.to_number(trd_mkt)

        req.c2s.orderID = int(order_id)
        _, req.c2s.modifyOrderOp = ModifyOrderOp.to_number(modify_order_op)
        req.c2s.forAll = False

        if modify_order_op == ModifyOrderOp.NORMAL:
            req.c2s.qty = qty
            req.c2s.price = price
            req.c2s.adjustPrice = adjust_limit != 0
            req.c2s.adjustSideAndLimit = adjust_limit

        return pack_pb_req(req, ProtoId.Trd_ModifyOrder, conn_id, serial_no)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        """Convert from PLS response to user response"""
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        order_id = str(rsp_pb.s2c.orderID)
        modify_order_list = [{
            'trd_env': TrdEnv.to_string2(rsp_pb.s2c.header.trdEnv),
            'order_id': order_id
        }]

        return RET_OK, "", modify_order_list


class CancelOrder:
    """modify order class"""
    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, trd_env, acc_id, trd_mkt, conn_id):
        """Convert from user request for place order to PLS request"""
        from futu.common.pb.Trd_ModifyOrder_pb2 import Request
        req = Request()
        serial_no = get_unique_id32()
        req.c2s.packetID.serialNo = serial_no
        req.c2s.packetID.connID = conn_id

        _, req.c2s.header.trdEnv = TrdEnv.to_number(trd_env)
        req.c2s.header.accID = acc_id
        _, req.c2s.header.trdMarket = TrdMarket.to_number(trd_mkt)

        req.c2s.orderID = 0
        req.c2s.modifyOrderOp = Trd_Common_pb2.ModifyOrderOp_Cancel
        req.c2s.forAll = True
        return pack_pb_req(req, ProtoId.Trd_ModifyOrder, conn_id, serial_no)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        """Convert from PLS response to user response"""
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None
        return RET_OK, "success", None


class DealListQuery:
    """Class for """
    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, trd_env, acc_id, trd_mkt, conn_id, refresh_cache):
        """Convert from user request for place order to PLS request"""
        from futu.common.pb.Trd_GetOrderFillList_pb2 import Request
        req = Request()
        _, req.c2s.header.trdEnv = TrdEnv.to_number(trd_env)
        req.c2s.header.accID = acc_id
        _, req.c2s.header.trdMarket = TrdMarket.to_number(trd_mkt)

        if code:
            req.c2s.filterConditions.codeList.append(code)

        if refresh_cache:
            req.c2s.refreshCache = refresh_cache

        return pack_pb_req(req, ProtoId.Trd_GetOrderFillList, conn_id)

    @classmethod
    def parse_deal(cls, rsp_pb, deal):
        deal_dict = {
            "code": merge_trd_mkt_stock_str(deal.secMarket, deal.code),
            "stock_name": deal.name,
            "deal_id": deal.fillID,
            "order_id": str(deal.orderID) if deal.HasField('orderID') else NoneDataValue,
            "qty": deal.qty,
            "price": deal.price,
            "trd_side": TrdSide.to_string2(deal.trdSide),
            "create_time": deal.createTime,
            "counter_broker_id": deal.counterBrokerID if deal.HasField('counterBrokerID') else NoneDataValue,
            "counter_broker_name": deal.counterBrokerName if deal.HasField('counterBrokerName') else NoneDataValue,
            "status": DealStatus.to_string2(deal.status) if deal.HasField("status") else NoneDataValue
        }
        return deal_dict

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        """Convert from PLS response to user response"""
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        raw_deal_list = rsp_pb.s2c.orderFillList
        deal_list = [DealListQuery.parse_deal(rsp_pb, deal) for deal in raw_deal_list]

        return RET_OK, "", deal_list


class HistoryOrderListQuery:
    """Class for querying Histroy Order"""

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, status_filter_list, code, start, end,
                 trd_env, acc_id, trd_mkt, conn_id):

        from futu.common.pb.Trd_GetHistoryOrderList_pb2 import Request
        req = Request()
        _, req.c2s.header.trdEnv = TrdEnv.to_number(trd_env)
        req.c2s.header.accID = acc_id
        _, req.c2s.header.trdMarket = TrdMarket.to_number(trd_mkt)

        if code:
            req.c2s.filterConditions.codeList.append(code)

        req.c2s.filterConditions.beginTime = start
        req.c2s.filterConditions.endTime = end

        if status_filter_list:
            for order_status in status_filter_list:
                r, v = OrderStatus.to_number(order_status)
                if r:
                    req.c2s.filterStatusList.append(v)

        return pack_pb_req(req, ProtoId.Trd_GetHistoryOrderList, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):

        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        raw_order_list = rsp_pb.s2c.orderList
        order_list = [{
                      "code": merge_trd_mkt_stock_str(order.secMarket, order.code),
                      "stock_name": order.name,
                      "trd_side": TrdSide.to_string2(order.trdSide),
                      "order_type": OrderType.to_string2(order.orderType),
                      "order_status": OrderStatus.to_string2(order.orderStatus),
                      "order_id": str(order.orderID),
                      "qty": order.qty,
                      "price": order.price,
                      "create_time": order.createTime,
                      "updated_time": order.updateTime,
                      "dealt_qty": order.fillQty,
                      "dealt_avg_price": order.fillAvgPrice,
                      "last_err_msg": order.lastErrMsg,
                      "remark": order.remark if order.HasField("remark") else "",
                      "time_in_force": TimeInForce.to_string2(order.timeInForce),
                      "fill_outside_rth": order.fillOutsideRTH if order.HasField("fillOutsideRTH") else 'N/A'
                      } for order in raw_order_list]
        return RET_OK, "", order_list


class HistoryDealListQuery:
    """Class for """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, start, end, trd_env, acc_id, trd_mkt, conn_id):

        from futu.common.pb.Trd_GetHistoryOrderFillList_pb2 import Request
        req = Request()
        _, req.c2s.header.trdEnv = TrdEnv.to_number(trd_env)
        req.c2s.header.accID = acc_id
        _, req.c2s.header.trdMarket = TrdMarket.to_number(trd_mkt)

        if code:
            req.c2s.filterConditions.codeList.append(code)

        req.c2s.filterConditions.beginTime = start
        req.c2s.filterConditions.endTime = end

        return pack_pb_req(req, ProtoId.Trd_GetHistoryOrderFillList, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):

        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        raw_deal_list = rsp_pb.s2c.orderFillList
        deal_list = [{
                    "code": merge_trd_mkt_stock_str(deal.secMarket, deal.code),
                    "stock_name": deal.name,
                    "deal_id": deal.fillID,
                    "order_id": str(deal.orderID) if deal.HasField('orderID') else "",
                    "qty": deal.qty,
                    "price": deal.price,
                    "trd_side": TrdSide.to_string2(deal.trdSide),
                    "create_time": deal.createTime,
                    "counter_broker_id": deal.counterBrokerID if deal.HasField('counterBrokerID') else "",
                    "counter_broker_name": deal.counterBrokerName,
                    "status": DealStatus.to_string2(deal.status) if deal.HasField('status') else 'N/A'
                     } for deal in raw_deal_list]

        return RET_OK, "", deal_list


class UpdateOrderPush:
    """Class for order update push"""
    def __init__(self):
        pass

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg

        order_dict = OrderListQuery.parse_order(rsp_pb, rsp_pb.s2c.order)
        order_dict['trd_env'] = TrdEnv.to_string2(rsp_pb.s2c.header.trdEnv)
        order_dict['trd_market'] = TrdMarket.to_string2(rsp_pb.s2c.header.trdMarket)

        return RET_OK, order_dict


class UpdateDealPush:
    """Class for order update push"""
    def __init__(self):
        pass

    @classmethod
    def unpack_rsp(cls, rsp_pb):

        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg

        deal_dict = DealListQuery.parse_deal(rsp_pb, rsp_pb.s2c.orderFill)
        deal_dict['trd_env'] = TrdEnv.to_string2(rsp_pb.s2c.header.trdEnv)
        deal_dict['trd_market'] = TrdMarket.to_string2(rsp_pb.s2c.header.trdMarket)

        return RET_OK, deal_dict


class AccTradingInfoQuery:
    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, order_type, code, price, order_id, adjust_limit, sec_mkt_str, trd_env, acc_id, trd_mkt, conn_id):

        from futu.common.pb.Trd_GetMaxTrdQtys_pb2 import Request
        req = Request()
        _, req.c2s.header.trdEnv = TrdEnv.to_number(trd_env)
        req.c2s.header.accID = acc_id
        _, req.c2s.header.trdMarket = TrdMarket.to_number(trd_mkt)

        _, req.c2s.orderType = OrderType.to_number(order_type)
        req.c2s.code = code
        req.c2s.price = price
        if order_id is not None:
            req.c2s.orderID = int(order_id)
        if adjust_limit == 0:
            req.c2s.adjustPrice = False
        else:
            req.c2s.adjustPrice = True
            req.c2s.adjustSideAndLimit = adjust_limit

        r, proto_qot_mkt = Market.to_number(sec_mkt_str)
        if not r:
            proto_qot_mkt = Qot_Common_pb2.QotMarket_Unknown

        proto_trd_sec_mkt = QOT_MARKET_TO_TRD_SEC_MARKET_MAP.get(proto_qot_mkt, Trd_Common_pb2.TrdSecMarket_Unknown)
        req.c2s.secMarket = proto_trd_sec_mkt

        return pack_pb_req(req, ProtoId.Trd_GetMaxTrdQtys, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        from futu.common.pb.Trd_Common_pb2 import MaxTrdQtys

        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        info = rsp_pb.s2c.maxTrdQtys    # type: MaxTrdQtys
        data = [{
            'max_cash_buy': info.maxCashBuy,
            'max_cash_and_margin_buy': info.maxCashAndMarginBuy if info.HasField('maxCashAndMarginBuy') else NoneDataValue,
            'max_position_sell': info.maxPositionSell,
            'max_sell_short': info.maxSellShort if info.HasField('maxSellShort') else NoneDataValue,
            'max_buy_back': info.maxBuyBack if info.HasField('maxBuyBack') else NoneDataValue,
            'long_required_im': info.longRequiredIM if info.HasField('longRequiredIM') else NoneDataValue,
            'short_required_im': info.shortRequiredIM if info.HasField('shortRequiredIM') else NoneDataValue
        }]

        return RET_OK, "", data
