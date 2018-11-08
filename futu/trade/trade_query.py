# -*- coding: utf-8 -*-
"""
    Trade query
"""
import datetime as dt
from futu.common.utils import *
from futu.quote.quote_query import pack_pb_req


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
            'trd_env': TRADE.REV_TRD_ENV_MAP[record.trdEnv] if record.trdEnv in TRADE.REV_TRD_ENV_MAP else "",
            'trdMarket_list': [(TRADE.REV_TRD_MKT_MAP[trdMkt] if trdMkt in TRADE.REV_TRD_MKT_MAP else TrdMarket.NONE) for trdMkt in record.trdMarketAuthList]
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
    def pack_req(cls, acc_id, trd_market, trd_env, conn_id):
        from futu.common.pb.Trd_GetFunds_pb2 import Request
        req = Request()
        req.c2s.header.trdEnv = TRD_ENV_MAP[trd_env]
        req.c2s.header.accID = acc_id
        req.c2s.header.trdMarket = TRD_MKT_MAP[trd_market]

        return pack_pb_req(req, ProtoId.Trd_GetFunds, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        """Convert from PLS response to user response"""
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        raw_funds = rsp_pb.s2c.funds
        accinfo_list = [{
            'power': raw_funds.power,
            'total_assets': raw_funds.totalAssets,
            'cash': raw_funds.cash,
            'market_val': raw_funds.marketVal,
            'frozen_cash': raw_funds.frozenCash,
            'avl_withdrawal_cash': raw_funds.avlWithdrawalCash,
        }]
        return RET_OK, "", accinfo_list


class PositionListQuery:
    """Class for querying position list"""

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, pl_ratio_min,
                 pl_ratio_max, trd_env, acc_id, trd_mkt, conn_id):
        """Convert from user request for trading days to PLS request"""
        from futu.common.pb.Trd_GetPositionList_pb2 import Request
        req = Request()
        req.c2s.header.trdEnv = TRD_ENV_MAP[trd_env]
        req.c2s.header.accID = acc_id
        req.c2s.header.trdMarket = TRD_MKT_MAP[trd_mkt]
        if code:
            req.c2s.filterConditions.codeList.append(code)
        if pl_ratio_min is not None:
            req.c2s.filterPLRatioMin = float(pl_ratio_min) / 100.0
        if pl_ratio_max is not None:
            req.c2s.filterPLRatioMax = float(pl_ratio_max) / 100.0

        return pack_pb_req(req, ProtoId.Trd_GetPositionList, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        """Convert from PLS response to user response"""
        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        raw_position_list = rsp_pb.s2c.positionList

        position_list = [{
                             "code": merge_trd_mkt_stock_str(rsp_pb.s2c.header.trdMarket, position.code),
                             "stock_name": position.name,
                             "qty": position.qty,
                             "can_sell_qty": position.canSellQty,
                             "cost_price": position.costPrice if position.HasField('costPrice') else 0,
                             "cost_price_valid": 1 if position.HasField('costPrice') else 0,
                             "market_val": position.val,
                             "nominal_price": position.price,
                             "pl_ratio": 100 * position.plRatio if position.HasField('plRatio') else 0,
                             "pl_ratio_valid": 1 if position.HasField('plRatio') else 0,
                             "pl_val": position.plVal if position.HasField('plVal') else 0,
                             "pl_val_valid": 1 if position.HasField('plVal') else 0,
                             "today_buy_qty": position.td_buyQty if position.HasField('td_buyQty') else 0,
                             "today_buy_val": position.td_buyVal if position.HasField('td_buyVal') else 0,
                             "today_pl_val": position.td_plVal if position.HasField('td_plVal') else 0,
                             "today_sell_qty": position.td_sellQty if position.HasField('td_sellQty') else 0,
                             "today_sell_val": position.td_sellVal if position.HasField('td_sellVal') else 0,
                             "position_side": TRADE.REV_POSITION_SIDE_MAP[position.positionSide]
                                if position.positionSide in TRADE.REV_POSITION_SIDE_MAP else PositionSide.NONE,
                         } for position in raw_position_list]
        return RET_OK, "", position_list


class OrderListQuery:
    """Class for querying list queue"""
    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, order_id, status_filter_list, code, start, end,
                 trd_env, acc_id, trd_mkt, conn_id):
        """Convert from user request for trading days to PLS request"""
        from futu.common.pb.Trd_GetOrderList_pb2 import Request
        req = Request()
        req.c2s.header.trdEnv = TRD_ENV_MAP[trd_env]
        req.c2s.header.accID = acc_id
        req.c2s.header.trdMarket = TRD_MKT_MAP[trd_mkt]

        if code:
            req.c2s.filterConditions.codeList.append(code)
        if order_id:
            req.c2s.filterConditions.idList.append(int(order_id))

        if start:
            req.c2s.filterConditions.beginTime = start
        if end:
            req.c2s.filterConditions.endTime = end

        if len(status_filter_list):
            for order_status in status_filter_list:
                req.c2s.filterStatusList.append(ORDER_STATUS_MAP[order_status])

        return pack_pb_req(req, ProtoId.Trd_GetOrderList, conn_id)

    @classmethod
    def parse_order(cls, rsp_pb, order):
        order_dict = {
            "code": merge_trd_mkt_stock_str(rsp_pb.s2c.header.trdMarket, order.code),
            "stock_name": order.name,
            "trd_side": TRADE.REV_TRD_SIDE_MAP[order.trdSide] if order.trdSide in TRADE.REV_TRD_SIDE_MAP else TrdSide.NONE,
            "order_type": TRADE.REV_ORDER_TYPE_MAP[order.orderType] if order.orderType in TRADE.REV_ORDER_TYPE_MAP else OrderType.NONE,
            "order_status": TRADE.REV_ORDER_STATUS_MAP[order.orderStatus] if order.orderStatus in TRADE.REV_ORDER_STATUS_MAP else OrderStatus.NONE,
            "order_id": str(order.orderID),
            "qty": order.qty,
            "price": order.price,
            "create_time": order.createTime,
            "updated_time": order.updateTime,
            "dealt_qty": order.fillQty,
            "dealt_avg_price": order.fillAvgPrice,
            "last_err_msg": order.lastErrMsg
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
                 code, adjust_limit, trd_env, sec_mkt_str, acc_id, trd_mkt, conn_id):
        """Convert from user request for place order to PLS request"""
        from futu.common.pb.Trd_PlaceOrder_pb2 import Request
        req = Request()
        serial_no = get_unique_id32()
        req.c2s.packetID.serialNo = serial_no
        req.c2s.packetID.connID = conn_id

        req.c2s.header.trdEnv = TRD_ENV_MAP[trd_env]
        req.c2s.header.accID = acc_id
        req.c2s.header.trdMarket = TRD_MKT_MAP[trd_mkt]

        req.c2s.trdSide = TRD_SIDE_MAP[trd_side]
        req.c2s.orderType = ORDER_TYPE_MAP[order_type]
        req.c2s.code = code
        req.c2s.qty = qty
        req.c2s.price = price
        req.c2s.adjustPrice = adjust_limit != 0
        req.c2s.adjustSideAndLimit = adjust_limit
        proto_qot_mkt = MKT_MAP.get(sec_mkt_str, Qot_Common_pb2.QotMarket_Unknown)
        proto_trd_sec_mkt = QOT_MARKET_TO_TRD_SEC_MARKET_MAP.get(proto_qot_mkt,
                                                                 Trd_Common_pb2.TrdSecMarket_Unknown)
        req.c2s.secMarket = proto_trd_sec_mkt

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

        req.c2s.header.trdEnv = TRD_ENV_MAP[trd_env]
        req.c2s.header.accID = acc_id
        req.c2s.header.trdMarket = TRD_MKT_MAP[trd_mkt]

        req.c2s.orderID = int(order_id)
        req.c2s.modifyOrderOp = MODIFY_ORDER_OP_MAP[modify_order_op]
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
            'trd_env': TRADE.REV_TRD_ENV_MAP[rsp_pb.s2c.header.trdEnv],
            'order_id': order_id
        }]

        return RET_OK, "", modify_order_list


class DealListQuery:
    """Class for """
    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, code, trd_env, acc_id, trd_mkt, conn_id):
        """Convert from user request for place order to PLS request"""
        from futu.common.pb.Trd_GetOrderFillList_pb2 import Request
        req = Request()
        req.c2s.header.trdEnv = TRD_ENV_MAP[trd_env]
        req.c2s.header.accID = acc_id
        req.c2s.header.trdMarket = TRD_MKT_MAP[trd_mkt]

        if code:
            req.c2s.filterConditions.codeList.append(code)

        return pack_pb_req(req, ProtoId.Trd_GetOrderFillList, conn_id)

    @classmethod
    def parse_deal(cls, rsp_pb, deal):
        deal_dict = {
            "code": merge_trd_mkt_stock_str(rsp_pb.s2c.header.trdMarket, deal.code),
            "stock_name": deal.name,
            "deal_id": deal.fillID,
            "order_id": str(deal.orderID) if deal.HasField('orderID') else "",
            "qty": deal.qty,
            "price": deal.price,
            "trd_side": TRADE.REV_TRD_SIDE_MAP[deal.trdSide] if deal.trdSide in TRADE.REV_TRD_SIDE_MAP else TrdSide.NONE,
            "create_time": deal.createTime,
            "counter_broker_id": deal.counterBrokerID,
            "counter_broker_name": deal.counterBrokerName,
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
        req.c2s.header.trdEnv = TRD_ENV_MAP[trd_env]
        req.c2s.header.accID = acc_id
        req.c2s.header.trdMarket = TRD_MKT_MAP[trd_mkt]

        if code:
            req.c2s.filterConditions.codeList.append(code)

        req.c2s.filterConditions.beginTime = start
        req.c2s.filterConditions.endTime = end

        if status_filter_list:
            for order_status in status_filter_list:
                req.c2s.filterStatusList.append(ORDER_STATUS_MAP[order_status])

        return pack_pb_req(req, ProtoId.Trd_GetHistoryOrderList, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):

        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        raw_order_list = rsp_pb.s2c.orderList
        order_list = [{
                      "code": merge_trd_mkt_stock_str(rsp_pb.s2c.header.trdMarket, order.code),
                      "stock_name": order.name,
                      "trd_side": TRADE.REV_TRD_SIDE_MAP[order.trdSide] if order.trdSide in TRADE.REV_TRD_SIDE_MAP else TrdSide.NONE,
                      "order_type": TRADE.REV_ORDER_TYPE_MAP[order.orderType] if order.orderType in TRADE.REV_ORDER_TYPE_MAP else OrderType.NONE,
                      "order_status": TRADE.REV_ORDER_STATUS_MAP[order.orderStatus] if order.orderStatus in TRADE.REV_ORDER_STATUS_MAP else OrderStatus.NONE,
                      "order_id": str(order.orderID),
                      "qty": order.qty,
                      "price": order.price,
                      "create_time": order.createTime,
                      "updated_time": order.updateTime,
                      "dealt_qty": order.fillQty,
                      "dealt_avg_price": order.fillAvgPrice,
                      "last_err_msg": order.lastErrMsg
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
        req.c2s.header.trdEnv = TRD_ENV_MAP[trd_env]
        req.c2s.header.accID = acc_id
        req.c2s.header.trdMarket = TRD_MKT_MAP[trd_mkt]

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
                    "code": merge_trd_mkt_stock_str(rsp_pb.s2c.header.trdMarket, deal.code),
                    "stock_name": deal.name,
                    "deal_id": deal.fillID,
                    "order_id": str(deal.orderID) if deal.HasField('orderID') else "",
                    "qty": deal.qty,
                    "price": deal.price,
                    "trd_side": TRADE.REV_TRD_SIDE_MAP[deal.trdSide] if deal.trdSide in TRADE.REV_TRD_SIDE_MAP else TrdSide.NONE,
                    "create_time": deal.createTime,
                    "counter_broker_id": deal.counterBrokerID,
                    "counter_broker_name": deal.counterBrokerName
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
        order_dict['trd_env'] = TRADE.REV_TRD_ENV_MAP[rsp_pb.s2c.header.trdEnv]
        order_dict['trd_market'] = TRADE.REV_TRD_MKT_MAP[rsp_pb.s2c.header.trdMarket]

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
        deal_dict['trd_env'] = TRADE.REV_TRD_ENV_MAP[rsp_pb.s2c.header.trdEnv]
        deal_dict['trd_market'] = TRADE.REV_TRD_MKT_MAP[rsp_pb.s2c.header.trdMarket]

        return RET_OK, deal_dict


class AccTradingInfoQuery:
    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, order_type, code, price, order_id, adjust_limit, sec_mkt_str, trd_env, acc_id, trd_mkt, conn_id):

        from futu.common.pb.Trd_GetMaxTrdQtys_pb2 import Request
        req = Request()
        req.c2s.header.trdEnv = TRD_ENV_MAP[trd_env]
        req.c2s.header.accID = acc_id
        req.c2s.header.trdMarket = TRD_MKT_MAP[trd_mkt]

        req.c2s.orderType = ORDER_TYPE_MAP[order_type]
        req.c2s.code = code
        req.c2s.price = price
        if order_id is not None:
            req.c2s.orderID = int(order_id)
        if adjust_limit == 0:
            req.c2s.adjustPrice = False
        else:
            req.c2s.adjustPrice = True
            req.c2s.adjustSideAndLimit = adjust_limit

        proto_qot_mkt = MKT_MAP.get(sec_mkt_str, Qot_Common_pb2.QotMarket_Unknown)
        proto_trd_sec_mkt = QOT_MARKET_TO_TRD_SEC_MARKET_MAP.get(proto_qot_mkt,
                                                                 Trd_Common_pb2.TrdSecMarket_Unknown)
        req.c2s.secMarket = proto_trd_sec_mkt

        return pack_pb_req(req, ProtoId.Trd_GetAccTradingInfo, conn_id)

    @classmethod
    def unpack_rsp(cls, rsp_pb):
        from futu.common.pb.Trd_Common_pb2 import MaxTrdQtys

        if rsp_pb.retType != RET_OK:
            return RET_ERROR, rsp_pb.retMsg, None

        info = rsp_pb.s2c.maxTrdQtys    # type: MaxTrdQtys
        data = [{
            'max_cash_buy': info.maxCashBuy,
            'max_cash_and_margin_buy': info.maxCashAndMarginBuy if info.HasField('maxCashAndMarginBuy') else 0,
            'max_position_sell': info.maxPositionSell,
            'max_sell_short': info.maxSellShort if info.HasField('maxSellShort') else 0,
            'max_buy_back': info.maxBuyBack if info.HasField('maxBuyBack') else 0
        }]

        return RET_OK, "", data
