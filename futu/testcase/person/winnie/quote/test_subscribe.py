# -*- coding:utf-8 -*-
from futuquant import *


def test_subscribe():
    SysConfig.set_all_thread_daemon(False)
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11112)
    big_sub_codes = ['HK.02318', 'HK.02828', 'HK.00939', 'HK.01093', 'HK.01299', 'HK.00175',
                     'HK.01299', 'HK.01833', 'HK.00005', 'HK.00883', 'HK.00388', 'HK.01398',
                     'HK.01114', 'HK.02800', 'HK.02018', 'HK.03988', 'HK.00386', 'HK.01211',
                     'HK.00857', 'HK.01177', 'HK.02601', 'HK.02628', 'HK.00700', 'HK.800000',
                     'HK.03888', 'US.AMC', 'US.DIS', 'HK.01357', 'HK.00434', 'US.OPRA', 'HK.01810',
                     'HK.00268', 'US.AAPL', 'HK.01758', 'HK.01918', 'SZ.002230', 'HK.02628', 'HK.00002',
                     'HK.00006', 'HK.00020', 'HK.00021', 'HK.00023', 'HK.00026', 'HK.00128', 'HK.00062',
                     'US.VBFC', 'US.ARTX', 'US.DSWL', 'US.IDSA', 'US.OESX', 'US.ELY', 'US.TWLVW', 'US.AQST',
                     'US.SRE-B', 'US.BNGO', 'US.HCACU', 'SZ.000055', 'SZ.000058', 'SZ.000418', 'SZ.000596',
                     'SZ.000666', 'SZ.000869', 'SZ.002734', 'SZ.002735', 'SZ.002736', 'SZ.002737', 'SZ.002738',
                     'SZ.002739', 'SZ.000581', 'SZ.002740', 'SZ.002741', 'SZ.002742', 'SZ.300634', 'SZ.082548',
                     'HK.01775', 'HK.02952', 'HK.08525', 'HK.08540', 'HK.08606', 'HK.03302', 'HK.02048', 'HK.02956',
                      'HK.01581', 'US.GNK', 'US.IDRA', 'US.NIHD', 'US.TNET', 'US.KODK', 'US.WSTG',
                     'US.PEIX', 'US.CETV', 'US.GME', 'US.CBK', 'US.VNCE', 'US.EDU', 'US.VBFC', 'US.DSWL',
                     'US.KOSS', 'US.IDSA', 'US.WBAI', 'US.HCACU', 'US.MIII', 'US.MIIIW', 'US.HCCHW', 'US.SRE-B',
                     'SH.601138', 'SH.603666', 'SH.603650', 'SH.603693', 'SH.603733', 'SH.603301', 'SH.600929',
                     'SH.600860']
    print(quote_ctx.subscribe(big_sub_codes, SubType.TICKER))
    # print(quote_ctx.subscribe(['HK.00002'], SubType.TICKER))
    print(quote_ctx.query_subscription())
    quote_ctx.close()


if __name__ == '__main__':
    test_subscribe()
