from futu import *
import pandas


def test_get_reference_list():
    print('hello')
    quote_ctx = OpenQuoteContext(host='172.18.10.58', port=11111)
    code1 = 'HK.00700'  # 港股
    code2 = 'HK.03128'  # A股
    code3 = 'US.CYTXW'  # 美股
    code4 = 'HK.12819'  # 涡轮
    code5 = 'HK.999010'  # 期货
    print(quote_ctx.get_referencestock_list(code5, SecurityReferenceType.WARRANT))


if __name__ == '__main__':
    test_get_reference_list()

