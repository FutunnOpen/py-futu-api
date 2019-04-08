    def get_capital_distribution(self, stock_code):
        """
        GetCapitalDistribution
        """
        if stock_code is None or is_str(stock_code) is False:
            error_str = ERROR_STR_PREFIX + 'the type of stock_code param is wrong'
            return RET_ERROR, error_str    

        query_processor = self._get_sync_query_processor(
            GetCapitalDistributionQuery.pack_req,
            GetCapitalDistributionQuery.unpack,
        )

        kargs = {
            "stock_code": stock_code,
            "conn_id": self.get_sync_conn_id()
        }
        ret_code, msg, ret = query_processor(**kargs)
        if ret_code == RET_ERROR:
            return ret_code, msg
        if isinstance(ret,dict):
            col_list = [
                'capital_in_big',
                'capital_in_mid',
                'capital_in_small',
                'capital_out_big',
                'capital_out_mid',
                'capital_out_small',
                'update_time',
            ]
            ret_frame = pd.DataFrame(ret, columns=col_list, index=[0])
            return RET_OK, ret_frame
        else:
            return RET_ERROR, "empty data"

        
    """
    ===============================================================================
    ===============================================================================
    """    
        
    class GetCapitalDistributionQuery:
    """
    Query GetCapitalDistribution.
    """

    def __init__(self):
        pass

    @classmethod
    def pack_req(cls, stock_code, conn_id):
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
        ret["capital_in_big"]=rsp_pb.s2c.capitalInBig
        #  流入资金额度，中单 type=double
        ret["capital_in_mid"]=rsp_pb.s2c.capitalInMid
        #  流入资金额度，小单 type=double
        ret["capital_in_small"]=rsp_pb.s2c.capitalInSmall
        #  流出资金额度，大单 type=double
        ret["capital_out_big"]=rsp_pb.s2c.capitalOutBig
        #  流出资金额度，中单 type=double
        ret["capital_out_mid"]=rsp_pb.s2c.capitalOutMid
        #  流出资金额度，小单 type=double
        ret["capital_out_small"]=rsp_pb.s2c.capitalOutSmall
        #  更新时间字符串 type=string
        ret["update_time"]=rsp_pb.s2c.updateTime
        return RET_OK, "", ret
    
