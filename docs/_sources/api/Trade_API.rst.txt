===========
交易API
===========

 .. _TrdEnv: Base_API.html#trdenv
 
 .. _TrdMarket: Base_API.html#trdmarket
 
 .. _PositionSide: Base_API.html#positionside
 
 .. _OrderType : Base_API.html#ordertype
 
 .. _OrderStatus: Base_API.html#orderstatus
 
 .. _TrdSide: Base_API.html#trdside
 
 .. _order-list-query: #id3
 
 .. _deal-list-query: #id4
 
 .. _ModifyOrderOp: Base_API.html#ModifyOrderOp
 
一分钟上手
==============

如下范例，创建api交易对象，先调用unlock_trade对交易解锁，然后调用place_order下单，以700.0价格，买100股腾讯00700，最后关闭对象。

注意交易对象区分港股美股。

.. code:: python

	from futu import *
	pwd_unlock = '123456'
	trd_ctx = OpenHKTradeContext(host='127.0.0.1', port=11111)
	print(trd_ctx.unlock_trade(pwd_unlock))
	print(trd_ctx.place_order(price=700.0, qty=100, code="HK.00700", trd_side=TrdSide.BUY))
	trd_ctx.close()



接口类对象
==============

OpenHKTradeContext、OpenUSTradeContext、OpenHKCCTradeContext(A股通)、OpenCNTradeContext - 交易接口类
---------------------------------------------------------------------------------------------------------------------------

close
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: close

关闭上下文对象。默认情况下，futuquant内部创建的线程会阻止进程退出，只有当所有context都close后，进程才能正常退出。但通过SysConfig.set_all_thread_daemon可以设置所有内部线程为daemon线程，这时即使没有调用context的close，进程也可以正常退出。

.. code:: python

    from futu import *
    quote_ctx = OpenHKTradeContext(host='127.0.0.1', port=11111)
    quote_ctx.close()
	


get_acc_list - 获取交易业务账户列表
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: get_acc_list(self)

 获取交易业务账户列表。要调用交易接口前，必须先获取此列表，后续交易接口根据不同市场传入不同的交易业务账户ID，传0默认第一个账户
		
 :return(ret_code, ret_data): ret_code为RET_OK时，ret_data为DataFrame数据，否则为错误原因字符串，DataFrame数据如下：
 
 ==============   ===========   ===================================================================
 参数             类型          说明
 ==============   ===========   ===================================================================
 acc_id           int           交易业务账户
 trd_env          str           交易环境，TrdEnv.REAL(真实环境)或TrdEnv.SIMULATE(仿真环境)
 ==============   ===========   ===================================================================

 :example:
 
 .. code:: python
 
	trd_ctx = OpenHKTradeContext(host='127.0.0.1', port=11111)
	print(trd_ctx.get_acc_list())
	trd_ctx.close()
	
----------------------------

unlock_trade - 解锁交易
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: unlock_trade(self, password, password_md5=None, is_unlock=True)

 解锁交易。

 :param password: str，交易密码，如果password_md5不为空就使用传入的password_md5解锁，否则使用password转MD5得到password_md5再解锁
 :param password_md5: str，交易密码的32位MD5加密16进制字符串(全小写)，解锁交易必须要填密码，锁定交易忽略
 :param is_unlock: bool，解锁或锁定，True解锁，False锁定
 :return(ret_code, ret_data): 	ret == RET_OK时, data为None，如果之前已经解锁过了，data为提示字符串，指示出已经解锁
 
								ret != RET_OK时， data为错误字符串

 :example:
 
 .. code:: python
 
  from futu import *
  pwd_unlock = '123456'
  trd_ctx = OpenHKTradeContext(host='127.0.0.1', port=11111)
  print(trd_ctx.unlock_trade(pwd_unlock))
  trd_ctx.close()
 
----------------------------
 
accinfo_query - 获取账户资金数据
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: accinfo_query(self, trd_env=TrdEnv.REAL, acc_id=0, acc_index=0)

 获取账户资金数据。获取账户的资产净值、证券市值、现金、购买力等资金数据。

 :param trd_env: str，交易环境 TrdEnv_ ，TrdEnv.REAL(真实环境)或TrdEnv.SIMULATE(仿真环境)
 :param acc_id: int，交易业务账户ID，acc_id为ID号时以acc_id为准，传0使用acc_index所对应的账户
 :param acc_index: int，交易业务子账户ID列表所对应的下标，默认0，表示第1个业务ID
 :return(ret_code, ret_data): ret_code为RET_OK时，ret_data为DataFrame数据，否则为错误原因字符串，DataFrame数据如下：

 =====================        ===========   ===================================================================
 参数                         类型          说明
 =====================        ===========   ===================================================================
 power                        float         购买力，即可使用用于买入的资金
 total_assets                 float         资产净值
 cash                         float         现金
 market_val                   float         证券市值
 frozen_cash                  float         冻结金额
 avl_withdrawal_cash          float         可提金额
 =====================        ===========   ===================================================================
 
 :example:
 
 .. code:: python
 
  from futu import *
  pwd_unlock = '123456'
  trd_ctx = OpenHKTradeContext(host='127.0.0.1', port=11111)
  trd_ctx.unlock_trade(pwd_unlock)
  print(trd_ctx.accinfo_query())
  trd_ctx.close()
  

----------------------------

position_list_query - 获取账户持仓列表
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: position_list_query(self, code='', pl_ratio_min=None, pl_ratio_max=None, trd_env=TrdEnv.REAL, acc_id=0, acc_index=0)

 获取账户持仓列表。获取账户的证券持仓列表。

 :param code: str，代码过滤，只返回包含这个代码的数据，没传不过滤，返回所有
 :param pl_ratio_min: float，过滤盈亏比例下限，高于此比例的会返回，如0.1，返回盈亏比例大于10%的持仓
 :param pl_ratio_max: float，过滤盈亏比例上限，低于此比例的会返回，如0.2，返回盈亏比例小于20%的持仓
 :param trd_env: str，交易环境，TrdEnv.REAL(真实环境)或TrdEnv.SIMULATE(仿真环境)
 :param acc_id: int，交易业务账户ID，acc_id为ID号时以acc_id为准，传0使用acc_index所对应的账户
 :param acc_index: int，交易业务子账户ID列表所对应的下标，默认0，表示第1个业务ID
 :return(ret_code, ret_data): ret_code为RET_OK时，ret_data为DataFrame数据，否则为错误原因字符串，DataFrame数据如下：

 =====================        ===========   ===================================================================
 参数                         类型          说明
 =====================        ===========   ===================================================================
 position_side                str           持仓方向，PositionSide.LONG(多仓)或PositionSide.SHORT(空仓)
 code                         str           代码
 stock_name                   str           名称
 qty                          float         持有数量，2位精度，期权单位是"张"，下同
 can_sell_qty                 float         可卖数量
 nominal_price                float         市价，3位精度(A股2位)
 cost_price                   float        	成本价，无精度限制
 cost_price_valid             bool          成本价是否有效，True有效，False无效
 market_val                   float         市值，3位精度(A股2位)
 pl_ratio                     float         盈亏比例，无精度限制
 pl_ratio_valid               bool          盈亏比例是否有效，True有效，False无效
 pl_val                       float         盈亏金额，3位精度(A股2位)
 pl_val_valid                 bool          盈亏金额是否有效，True有效，False无效
 today_pl_val                 float         今日盈亏金额，3位精度(A股2位)，下同
 today_buy_qty                float         今日买入总量
 today_buy_val                float         今日买入总额
 today_sell_qty               float         今日卖出总量
 today_sell_val               float         今日卖出总额
 =====================        ===========   ===================================================================
 
 :example:
 
 .. code:: python
 
  from futu import *
  pwd_unlock = '123456'
  trd_ctx = OpenHKTradeContext(host='127.0.0.1', port=11111)
  trd_ctx.unlock_trade(pwd_unlock)
  print(trd_ctx.position_list_query())
  trd_ctx.close()

----------------------------

place_order - 下单
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: place_order(self, price, qty, code, trd_side, order_type=OrderType.NORMAL, adjust_limit=0, trd_env=TrdEnv.REAL, acc_id=0, acc_index=0)

 下单交易。
 
 注意，由于python api是同步的，但网络收发是异步的，当place_order对应的应答数据包与订单成交推送（TradeDealHandlerBase）或订单状态变化推送（TradeOrderHandlerBase）间隔很短时，就可能出现虽然是place_order的数据包先返回，但推送的回调会先被调用的情况。例如可能先调用了TradeOrderHandlerBase，然后place_order这个接口才返回。

 :param price: float，订单价格，3位精度(A股2位)，当订单是市价单或竞价单类型，忽略该参数传值
 :param qty: float，订单数量，2位精度，期权单位是"张"
 :param code: str，代码
 :param trd_side: str，交易方向，参考TrdSide类的定义
 :param order_type: str，订单类型，参考OrderType类的定义
 :param adjust_limit: folat，港股有价位表，订单价格必须在规定的价位上，OpenD会对传入价格自动调整到合法价位上，此参数指定价格调整方向和调整幅度百分比限制，正数代表向上调整，负数代表向下调整，具体值代表调整幅度限制，如：0.015代表向上调整且幅度不超过1.5%；-0.01代表向下调整且幅度不超过1%
 :param trd_env: str，交易环境，TrdEnv.REAL(真实环境)或TrdEnv.SIMULATE(仿真环境)
 :param acc_id: int，交易业务账户ID，acc_id为ID号时以acc_id为准，传0使用acc_index所对应的账户
 :param acc_index: int，交易业务子账户ID列表所对应的下标，默认0，表示第1个业务ID
 :return(ret_code, ret_data): ret_code为RET_OK时，ret_data为DataFrame数据，否则为错误原因字符串，DataFrame数据跟下面的 order-list-query_ (获取订单列表)相同。
 
	如果是OpenHKCCTradeContext，返回数据中order_type仅有OrderType.NORMAL
 
 :example:
 
 .. code:: python
 
 	from futu import *
	pwd_unlock = '123456'
	trd_ctx = OpenHKTradeContext(host='127.0.0.1', port=11111)
	print(trd_ctx.unlock_trade(pwd_unlock))
	print(trd_ctx.place_order(price=700.0, qty=100, code="HK.00700", trd_side=TrdSide.SELL))
	trd_ctx.close()

----------------------------

order_list_query - 获取订单列表
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: order_list_query(self, order_id="", status_filter_list=[], code='', start='', end='', trd_env=TrdEnv.REAL, acc_id=0)

 获取订单列表。获取账户的交易订单列表。

 :param order_id: str，订单号过滤，只返回此订单号的数据，没传不过滤，返回所有
 :param status_filter_list: str数组，订单状态过滤，只返回这些状态的订单数据，没传不过滤，返回所有，参考 OrderStatus_ 类的定义
 :param code: str，代码过滤，只返回包含这个代码的数据，没传不过滤，返回所有
 :param start: str，开始时间，严格按YYYY-MM-DD HH:MM:SS或YYYY-MM-DD HH:MM:SS.MS格式传
 :param end: str，结束时间，严格按YYYY-MM-DD HH:MM:SS或YYYY-MM-DD HH:MM:SS.MS格式传
 :param trd_env: str，交易环境，TrdEnv.REAL(真实环境)或TrdEnv.SIMULATE(仿真环境)
 :param acc_id: int，交易业务账户ID，acc_id为ID号时以acc_id为准，传0使用acc_index所对应的账户
 :param acc_index: int，交易业务子账户ID列表所对应的下标，默认0，表示第1个业务ID
 :return(ret_code, ret_data): ret_code为RET_OK时，ret_data为DataFrame数据，否则为错误原因字符串，DataFrame数据如下：

 =====================        ===========   =======================================================================
 参数                         类型          说明
 =====================        ===========   =======================================================================
 trd_side                     str           交易方向，参考 TrdSide_ 类的定义
 order_type                   str           订单类型，参考 OrderType_ 类的定义。OpenHKCCTradeContext仅返回NORMAL
 order_status                 str           订单状态，参考 OrderStatus_ 类的定义。OpenHKCCTradeContext没有DISABLED
 order_id                     str           订单号
 code                         str           代码
 stock_name                   str           名称
 qty                          float         订单数量，2位精度，期权单位是"张"
 price                        float         订单价格，3位精度(A股2位)
 create_time                  str           创建时间，严格按YYYY-MM-DD HH:MM:SS或YYYY-MM-DD HH:MM:SS.MS格式传
 updated_time                 str        	最后更新时间，严格按YYYY-MM-DD HH:MM:SS或YYYY-MM-DD HH:MM:SS.MS格式传
 dealt_qty                    float         成交数量，2位精度，期权单位是"张"
 dealt_avg_price              float         成交均价，无精度限制
 last_err_msg                 str           最后的错误描述，如果有错误，会有此描述最后一次错误的原因，无错误为空
 =====================        ===========   =======================================================================
 
 :example:
 
 .. code:: python
 
  from futu import *
  pwd_unlock = '123456'
  trd_ctx = OpenHKTradeContext(host='127.0.0.1', port=11111)
  print(trd_ctx.unlock_trade(pwd_unlock))
  print(trd_ctx.order_list_query())
  trd_ctx.close()
  
----------------------------

modify_order - 修改订单
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: modify_order(self, modify_order_op, order_id, qty, price, adjust_limit=0, trd_env=TrdEnv.REAL, acc_id=0, acc_index=0)

 修改订单。修改订单，包括修改订单的价格和数量(即以前的改单)、撤单、失效、生效、删除等。
 
 如果是OpenHKCCTradeContext，将不支持改单。可撤单。删除订单是本地操作。

 :param modify_order_op: str，改单操作类型，参考 ModifyOrderOp_ 类的定义，有
 :param order_id: str，订单号
 :param qty: float，(改单有效)新的订单数量，2位精度，期权单位是"张"
 :param price: float，(改单有效)新的订单价格，3位精度(A股2位)
 :param adjust_limit: folat，(改单有效)港股有价位表，订单价格必须在规定的价位上，OpenD会对传入价格自动调整到合法价位上，此参数指定价格调整方向和调整幅度百分比限制，正数代表向上调整，负数代表向下调整，具体值代表调整幅度限制，如：0.015代表向上调整且幅度不超过1.5%；-0.01代表向下调整且幅度不超过1%
 :param trd_env: str，交易环境 TrdEnv_ ，TrdEnv.REAL(真实环境)或TrdEnv.SIMULATE(仿真环境)
 :param acc_id: int，交易业务账户ID，acc_id为ID号时以acc_id为准，传0使用acc_index所对应的账户
 :param acc_index: int，交易业务子账户ID列表所对应的下标，默认0，表示第1个业务ID
 :return(ret_code, ret_data): ret_code为RET_OK时，ret_data为DataFrame数据，否则为错误原因字符串，DataFrame数据如下：
 
 =====================        ===========   ===================================================================
 参数                         类型          说明
 =====================        ===========   ===================================================================
 trd_env                      str           交易环境 TrdEnv_ ，TrdEnv.REAL(真实环境)或TrdEnv.SIMULATE(仿真环境)
 order_id                     str           str，订单号
 =====================        ===========   ===================================================================
 
 :example:
 
 .. code:: python
 
  from futu import *
  pwd_unlock = '123456'
  trd_ctx = OpenHKTradeContext(host='127.0.0.1', port=11111)
  print(trd_ctx.unlock_trade(pwd_unlock))
  order_id = "12345"
  print(trd_ctx.modify_order(ModifyOrderOp.CANCEL, order_id, 0, 0))
  trd_ctx.close()

----------------------------

change_order - 改单(老接口，兼容以前)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: change_order(self, order_id, price, qty, adjust_limit=0, trd_env=TrdEnv.REAL, acc_id=0)

 改单(老接口，兼容以前)。改单，即修改订单的价格和数量，是modify_order修改订单的一种操作，为兼容以前，保留此接口，新写代码请使用modify_order。

 :param order_id: str，订单号
 :param qty: float，(改单有效)新的订单数量，2位精度，期权单位是"张"
 :param price: float，(改单有效)新的订单价格，3位精度(A股2位)
 :param adjust_limit: folat，(改单有效)港股有价位表，订单价格必须在规定的价位上，OpenD会对传入价格自动调整到合法价位上，此参数指定价格调整方向和调整幅度百分比限制，正数代表向上调整，负数代表向下调整，具体值代表调整幅度限制，如：0.015代表向上调整且幅度不超过1.5%；-0.01代表向下调整且幅度不超过1%
 :param trd_env: str，交易环境 TrdEnv_ ，TrdEnv.REAL(真实环境)或TrdEnv.SIMULATE(仿真环境)
 :param acc_id: int，交易业务账户ID，传0默认第一个账户
 :return(ret_code, ret_data): ret_code为RET_OK时，ret_data为DataFrame数据，否则为错误原因字符串，DataFrame数据跟下面的modify_order(修改订单)相同。
	
	如果是OpenHKCCTradeContext，将直接返回(RET_ERROR, msg)
 
 :example:
 
 .. code:: python
 
  from futu import *
  pwd_unlock = '123456'
  trd_ctx = OpenHKTradeContext(host='127.0.0.1', port=11111)
  print(trd_ctx.unlock_trade(pwd_unlock))
  order_id = "12345"
  print(trd_ctx.change_order(order_id, 100.0, 1))
  trd_ctx.close()
  
----------------------------

deal_list_query - 获取成交列表
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: deal_list_query(self, code="", trd_env=TrdEnv.REAL, acc_id=0, acc_index=0)

 获取成交列表。获取账户的交易成交列表。

 :param code: str，代码过滤，只返回包含这个代码的数据，没传不过滤，返回所有
 :param trd_env: str，交易环境 TrdEnv_ ，TrdEnv.REAL(真实环境)或TrdEnv.SIMULATE(仿真环境)
 :param acc_id: int，交易业务账户ID，acc_id为ID号时以acc_id为准，传0使用acc_index所对应的账户
 :param acc_index: int，交易业务子账户ID列表所对应的下标，默认0，表示第1个业务ID
 :return(ret_code, ret_data): ret_code为RET_OK时，ret_data为DataFrame数据，否则为错误原因字符串，DataFrame数据如下：

 =====================        ===========   ===================================================================
 参数                         类型          说明
 =====================        ===========   ===================================================================
 trd_side                     str           交易方向，参考 TrdSide_ 类的定义
 deal_id                      str           成交号
 order_id                     str           订单号
 code                         str           代码
 stock_name                   str           名称
 qty                          float         成交数量，2位精度，期权单位是"张"
 price                        float         成交价格，3位精度(A股2位)
 create_time                  str           创建时间，严格按YYYY-MM-DD HH:MM:SS或YYYY-MM-DD HH:MM:SS.MS格式传
 counter_broker_id            int           对手经纪号，港股有效。OpenHKCCTradeContext无此字段
 counter_broker_name          str         	对手经纪名称，港股有效。OpenHKCCTradeContext无此字段
 =====================        ===========   ===================================================================
 
 :example:
 
 .. code:: python
 
  from futu import *
  pwd_unlock = '123456'
  trd_ctx = OpenHKTradeContext(host='127.0.0.1', port=11111)
  print(trd_ctx.unlock_trade(pwd_unlock))
  order_id = "12345"
  print(trd_ctx.deal_list_query(code='HK.00700'))
  trd_ctx.close()

----------------------------

history_order_list_query - 获取历史订单列表
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: history_order_list_query(self, status_filter_list=[], code='', start='', end='', trd_env=TrdEnv.REAL, acc_id=0, acc_index=0)

 获取历史订单列表。获取账户的历史交易订单列表。

 :param status_filter_list: str数组，订单状态过滤，只返回这些状态的订单数据，没传不过滤，返回所有，参考OrderStatus类的定义
 :param code: str，代码过滤，只返回包含这个代码的数据，没传不过滤，返回所有
 :param start: str，开始时间，严格按YYYY-MM-DD HH:MM:SS或YYYY-MM-DD HH:MM:SS.MS格式传
 :param end: str，结束时间，严格按YYYY-MM-DD HH:MM:SS或YYYY-MM-DD HH:MM:SS.MS格式传
 :param trd_env: str，交易环境 TrdEnv_ ，TrdEnv.REAL(真实环境)或TrdEnv.SIMULATE(仿真环境)
 :param acc_id: int，交易业务账户ID，acc_id为ID号时以acc_id为准，传0使用acc_index所对应的账户
 :param acc_index: int，交易业务子账户ID列表所对应的下标，默认0，表示第1个业务ID
 :return(ret_code, ret_data): ret_code为RET_OK时，ret_data为DataFrame数据，否则为错误原因字符串，DataFrame数据跟上面的 order-list-query_ (获取订单列表)相同
 
 :example:
 
 .. code:: python
 
  from futu import *
  pwd_unlock = '123456'
  trd_ctx = OpenHKTradeContext(host='127.0.0.1', port=11111)
  print(trd_ctx.unlock_trade(pwd_unlock))
  order_id = "12345"
  print(trd_ctx.history_order_list_query([OrderStatus.FILLED_ALL, OrderStatus.FILLED_PART], 'HK.00700'))
  trd_ctx.close()
  
----------------------------

history_deal_list_query - 获取历史成交列表
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: history_deal_list_query(self, code, start='', end='', trd_env=TrdEnv.REAL, acc_id=0, acc_index=0)

 获取历史成交列表。获取账户的历史交易成交列表。

 :param code: str，代码过滤，只返回包含这个代码的数据，没传不过滤，返回所有
 :param start: str，开始时间，严格按YYYY-MM-DD HH:MM:SS或YYYY-MM-DD HH:MM:SS.MS格式传
 :param end: str，结束时间，严格按YYYY-MM-DD HH:MM:SS或YYYY-MM-DD HH:MM:SS.MS格式传
 :param trd_env: str，交易环境 TrdEnv_ ，TrdEnv.REAL(真实环境)或TrdEnv.SIMULATE(仿真环境)
 :param acc_id: int，交易业务账户ID，acc_id为ID号时以acc_id为准，传0使用acc_index所对应的账户
 :param acc_index: int，交易业务子账户ID列表所对应的下标，默认0，表示第1个业务ID
 :return(ret_code, ret_data): ret_code为RET_OK时，ret_data为DataFrame数据，否则为错误原因字符串，DataFrame数据跟上面的 deal-list-query_ (获取成交列表)相同
 
 :example:
 
 .. code:: python
 
  from futu import *
  pwd_unlock = '123456'
  trd_ctx = OpenHKTradeContext(host='127.0.0.1', port=11111)
  print(trd_ctx.unlock_trade(pwd_unlock))
  order_id = "12345"
  print(trd_ctx.history_deal_list_query('HK.00700'))
  trd_ctx.close()

 
----------------------------

acctradinginfo_query - 查询账户下最大可买卖数量
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: acctradinginfo_query(self, order_type, code, price, order_id=None, adjust_limit=0, trd_env=TrdEnv.REAL, acc_id=0, acc_index=0)

 查询账户下最大可买卖数量
 
 :param order_type: 订单类型，参见 OrderType_
 :param code: 证券代码，例如'HK.00700'
 :param price: 报价，3位精度
 :param order_id: 订单号。如果是新下单，则可以传None。如果是改单则要传单号，此时计算最大可买可卖时会包括该订单所消耗的购买力，新下订单需要等待半秒才可使用该接口。
 :param adjust_limit: 调整方向和调整幅度百分比限制，正数代表向上调整，负数代表向下调整，具体值代表调整幅度限制，如：0.015代表向上调整且幅度不超过1.5%；-0.01代表向下调整且幅度不超过1%。默认0表示不调整
 :param trd_env: 交易环境，参见 TrdEnv_
 :param acc_id: 业务账号，默认0表示第1个
 :param acc_index: int，交易业务子账户ID列表所对应的下标，默认0，表示第1个业务ID
 :return (ret_code, ret_data):
        ret == RET_OK, data为pd.DataFrame，数据列如下

        ret != RET_OK, data为错误信息

=======================   ===========   ==================================================================================================
参数                      类型          说明
=======================   ===========   ==================================================================================================
max_cash_buy              float         不使用融资，仅自己的现金最大可买整手股数
max_cash_and_margin_buy   float         使用融资，自己的现金 + 融资资金总共的最大可买整手股数
max_position_sell         float         不使用融券(卖空)，仅自己的持仓最大可卖整手股数
max_sell_short            float         使用融券(卖空)，最大可卖空整手股数，不包括多仓
max_buy_back              float         卖空后，需要买回的最大整手股数。因为卖空后，必须先买回已卖空的股数，还掉股票，才能再继续买多。
=======================   ===========   ==================================================================================================
 
 :example:
 
 .. code:: python
 
  from futu import *
  pwd_unlock = '123456'
  trd_ctx = OpenHKTradeContext(host='127.0.0.1', port=11111)
  print(trd_ctx.unlock_trade(pwd_unlock))
  order_id = "12345"
  print(trd_ctx.acctradinginfo_query(OrderType.NORMAL, 'HK.00700', 400, order_id, 0.01))
  trd_ctx.close()

----------------------------

TradeOrderHandlerBase - 响应订单推送基类
-----------------------------------------------------------

on_recv_rsp - 响应订单推送
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: on_recv_rsp(self, rsp_pb)

 响应订单推送。OpenD会主动推送订单的最新更新数据过来，需要客户端响应处理。
 
 该类与place_order返回的顺序参见 place_order_ 的说明。
 
 :param rsp_pb: class，订单推送协议pb对象
 :return(ret_code, ret_data): ret_code为RET_OK时，ret_data为DataFrame数据，否则为错误原因字符串，DataFrame数据跟上面的 order-list-query_ (获取订单列表)相同

 :example:
 
 .. code:: python
 
  from futu import *
  from time import sleep
  class TradeOrderTest(TradeOrderHandlerBase):
    """ order update push"""
    def on_recv_rsp(self, rsp_pb):
        ret, content = super(TradeOrderTest, self).on_recv_rsp(rsp_pb)

        if ret == RET_OK:
            print("* TradeOrderTest content={}\n".format(content))

        return ret, content
  
  pwd_unlock = '123456'
  trd_ctx = OpenHKTradeContext(host='127.0.0.1', port=11111)
  trd_ctx.set_handler(TradeOrderTest())
  print(trd_ctx.unlock_trade(pwd_unlock))
  print(trd_ctx.place_order(price=700.0, qty=100, code="HK.00700", trd_side=TrdSide.SELL))
  
  sleep(15)
  trd_ctx.close()
	
----------------------------

TradeDealHandlerBase - 响应成交推送基类
-----------------------------------------------------------

on_recv_rsp - 响应成交推送
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  py:function:: on_recv_rsp(self, rsp_pb)

 响应成交推送。OpenD会主动推送新的成交数据过来，需要客户端响应处理
 
 该类与place_order返回的顺序参见 place_order_ 的说明。
 
 :param rsp_pb: class，成交推送协议pb对象
 :return(ret_code, ret_data): ret_code为RET_OK时，ret_data为DataFrame数据，否则为错误原因字符串，DataFrame数据跟上面的 deal-list-query_ (获取成交列表)相同

 :example:
 
 .. code:: python
 
  from futu import *
  from time import sleep
  class TradeDealTest(TradeDealHandlerBase):
    """ order update push"""
    def on_recv_rsp(self, rsp_pb):
        ret, content = super(TradeDealTest, self).on_recv_rsp(rsp_pb)

        if ret == RET_OK:
            print("TradeDealTest content={}".format(content))

        return ret, content
  
  pwd_unlock = '123456'
  trd_ctx = OpenHKTradeContext(host='127.0.0.1', port=11111)
  trd_ctx.set_handler(TradeDealTest())
  print(trd_ctx.unlock_trade(pwd_unlock))
  print(trd_ctx.place_order(price=700.0, qty=100, code="HK.00700", trd_side=TrdSide.SELL))
  
  sleep(15)
  trd_ctx.close()
	
----------------------------

暗盘交易
================

已开户用户需要确认 `暗盘交易风险 <https://help.futu5.com/darktrade/>`_ 才可以进行暗盘交易。

.. note::

  * 暗盘目前仅支持限价单
  
----------------------------

模拟交易
================

支持港美A股三大市场模拟交易，对比真实交易有以下区别：

1.订单的状态不支持删除、部分成交、生效、失效状态

2.不支持生效失效、删除订单操作，仅支持支持改单， 撤单

3.不支持成交数据，包括今日成交，历史成交，成交推送

4.下单仅支持Normal类型

5.模拟交易不需要解锁交易

可视数据可跳转至 `模拟交易 <https://m-match.futunn.com/simulate/>`_，该页面仅支持手机浏览器访问。

----------------------------

真实交易
================

真实交易支持港股、美股、A股通市场，区别如下

+------------------------+-------------------------+-------------------------+----------------------+----------------------+
| 区别                   | 交易方向                | 订单类型                | 股票代码             | 订单操作             |
+========================+=========================+=========================+======================+======================+
| 港股                   | 只支持买入和卖出        | 支持增强限价单，竞价单，| 5位数字              | 支持改单、撤单、生效 |
|                        |                         |                         |                      |                      |
|                        |                         | 竞价限价单，绝对限价单，|                      | 失效、删除           |
|                        |                         |                         |                      |                      |
|                        |                         | 特别限价单              |                      |                      |
+------------------------+-------------------------+-------------------------+----------------------+----------------------+
| 美股                   | 下单只支持传入买入和卖出| 支持限价单，市价单      | 无限制               | 仅支持改单和撤单     |
|                        |                         |                         |                      |                      |
|                        | 但产生的订单类型可能会出|                         |                      |                      |
|                        |                         |                         |                      |                      |
|                        | 现卖空和买回            |                         |                      |                      |
+------------------------+-------------------------+-------------------------+----------------------+----------------------+
| A股通                  | 只支持买入和卖出        | 仅支持A股限价委托       | 6位数字              |  仅支持改单和撤单    |
+------------------------+-------------------------+-------------------------+----------------------+----------------------+

----------------------------

接口频率限制
================

交易相关请求到达网关客户端后， 会转发请求到futu后台服务器，为防止恶意频繁请求，保护服务器负载，会对一些交易接口进行请求频率限制，
目前的频率限制是以连续30秒内，限制请求次数，具体那些接口有限制以及限制次数如下:

 ==========================        =====================
 接口名称                          连续30秒内次数限制
 ==========================        =====================
 unlock_trade                      10
 place_order                       15
 modify_order，change_order        20
 history_order_list_query          10
 history_deal_list_query           10
 ==========================        =====================
.. note::

  * 后台另外限制了下单频率，1秒内下单不可超过5次






