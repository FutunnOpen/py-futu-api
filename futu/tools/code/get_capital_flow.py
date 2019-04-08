    def get_capital_flow(self, stock_code):
        """
        GetCapitalFlow
        """
        if stock_code is None or is_str(stock_code) is False:
            error_str = ERROR_STR_PREFIX + 'the type of stock_code param is wrong'
            return RET_ERROR, error_str    

        query_processor = self._get_sync_query_processor(
            GetCapitalFlowQuery.pack_req,
            GetCapitalFlowQuery.unpack,
        )

        kargs = {
            "stock_code": stock_code,
            "conn_id": self.get_sync_conn_id()
        }
        ret_code, msg, ret = query_processor(**kargs)
        if ret_code == RET_ERROR:
            return ret_code, msg
        if isinstance(ret,list):
            col_list = [
            'last_valid_time',
            'last_valid_timestamp',
            'in_flow',
            'capital_flow_item_time',
            'timestamp'
            ]
            ret_frame = pd.DataFrame(ret, columns=col_list)
            return RET_OK, ret_frame
        else:
            return RET_ERROR, "empty data"

        
    """
    ===============================================================================
    ===============================================================================
    """    
        
    class GetCapitalFlowQuery:
    """
    Query GetCapitalFlow.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, stock_code, conn_id):
        """check stock_code 股票"""
        ret, content = split_stock_str(stock_code)
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
            ret_list.append(data)
            #  净流入的资金额度 type = double
            data["in_flow"] = item.inFlow
            #  开始时间字符串,以分钟为单位 type = string
            data["capital_flow_item_time"] = item.time
            data["last_valid_time"] = last_valid_time
            return RET_OK, "", ret_list
    
