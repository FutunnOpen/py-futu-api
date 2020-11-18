from futu import *
quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

# ret, data = quote_ctx.get_user_security_group(group_type = UserSecurityGroupType.NONE)

ret,data = quote_ctx.get_ten_broker('HK.01611','sell',500)
if ret == RET_OK:
    print(data)
else:
    print('error:', data)
quote_ctx.close() # 结束后记得关闭当条连接，防止连接条数用尽