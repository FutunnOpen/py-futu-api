from futuquant import *
import pandas
import sys


def test_multiple_hository_kline():
    quote_ctx = OpenQuoteContext(host='172.18.10.58', port=11111)

    # 设置打印信息
    pandas.set_option('max_columns', 100)
    pandas.set_option('display.width', 1000)

    # print输出到指定的data.txt中
    output = sys.stdout
    outputfile = open('data.txt', 'w')
    sys.stdout = outputfile

    k_types = [KLType.K_1M, KLType.K_5M, KLType.K_15M, KLType.K_30M, KLType.K_60M,
               KLType.K_DAY, KLType.K_WEEK, KLType.K_MON]
    # 获取指定的股票的所有k数据
    print('获取指定的股票HK.999010的所有k数据')
    for k_type in k_types:
        print(quote_ctx.get_multiple_history_kline(codelist='HK.999010', start='2018-05-20', end='2018-07-05',
                                                   ktype=k_type, autype=AuType.QFQ))
    # 获取其他股票的日k数据
    codelist = ['HK.999011', 'HK.999050', 'HK.999051', 'HK.999070', 'HK.999071', 'HK.999030', 'HK.999031']
    print(quote_ctx.get_multiple_history_kline(codelist=codelist, start='2018-05-21', end='2018-07-03',
                                               ktype=KLType.K_DAY, autype=AuType.QFQ))


if __name__ == '__main__':
    test_multiple_hository_kline()
