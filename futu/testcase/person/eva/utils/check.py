#-*-coding:utf-8-*-

class Check(object):

    def checkAwrite(self):
        readF = 'C:\\Users\\admin\\Desktop\\TickerTest.txt'
        writeF = 'C:\\Users\\admin\\Desktop\\TickerTest_00700.txt'
        w = open(writeF,'a')
        for line in open(readF):
            if line.__contains__('HK.00700'):
                w.write(line)

        print('done...')
        w.close()

    def checkRep(self):
        readF = 'C:\\Users\\admin\\Desktop\\TickerTest_00700_0711.txt'
        sequence_list = []
        for line in open(readF):
            line_list = line.split()
            sequence_list.append(line_list[len(line_list)-2])
        for sequence in sequence_list:
            print(sequence)
            t = sequence_list.count(sequence)
            if t>1:
                print(sequence+'出现次数：'+str(t))


if __name__ == '__main__':
    c = Check()
    # c.checkAwrite()
    c.checkRep()