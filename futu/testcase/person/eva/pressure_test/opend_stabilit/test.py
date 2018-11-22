import futu
quote_ctx = futu.OpenQuoteContext(host='172.18.10.58', port=11113)
quote_ctx.start()
ret_code, ret_data = quote_ctx.query_subscription()
sub_weight_used = ret_data.get('total_used')
print('sub_weight_used = %d' % sub_weight_used)