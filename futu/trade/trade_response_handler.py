# -*- coding: utf-8 -*-
import pandas as pd
from futu.common import RspHandlerBase
from futu.trade.trade_query import *


class TradeOrderHandlerBase(RspHandlerBase):
    """sys notify"""
    def on_recv_rsp(self, rsp_pb):
        """receive response callback function"""
        ret_code, ret_data = UpdateOrderPush.unpack_rsp(rsp_pb)

        if ret_code != RET_OK:
            return ret_code, ret_data
        else:
            order_dict = ret_data
            col_list = ['trd_env', 'code', 'stock_name', 'dealt_avg_price', 'dealt_qty',
                        'qty', 'order_id', 'order_type', 'price', 'order_status',
                        'create_time', 'updated_time', 'trd_side', 'last_err_msg', 'trd_market', "remark",
                        "time_in_force", "fill_outside_rth"
                        ]

            trade_frame_table = pd.DataFrame([order_dict], columns=col_list)
            return RET_OK, trade_frame_table


class TradeDealHandlerBase(RspHandlerBase):
    """sys notify"""
    def on_recv_rsp(self, rsp_pb):
        """receive response callback function"""
        ret_code, ret_data = UpdateDealPush.unpack_rsp(rsp_pb)

        if ret_code != RET_OK:
            return ret_code, ret_data
        else:
            deal_dict = ret_data
            col_list = ['trd_env', 'code', 'stock_name', 'deal_id', 'order_id',
                        'qty', 'price', 'trd_side', 'create_time', 'counter_broker_id',
                        'counter_broker_name', 'trd_market', 'status'
                        ]

            trade_frame_table = pd.DataFrame([deal_dict], columns=col_list)
            return RET_OK, trade_frame_table


