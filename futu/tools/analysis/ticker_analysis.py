import json
import operator
import os


class TickerAnalysis(object):
    """分析逐笔"""
    def __init__(self):
        self.opend_dict = dict()
        self.server_dict = dict()

    def analysis_opend_json(self, file_path):
        """从log里面找出关键数据"""
        self.opend_dict.clear()

        for line in open(file_path, "r+"):
            line = line.strip()
            json_to_python = json.loads(line)
            content = json_to_python["content"]
            millis = json_to_python["millis"]
            for item in content:
                code = item["code"]
                time = item["time"]
                price = int(float(item["price"])*1000)
                volume = int(item["volume"])
                d = dict()
                d["time"] = time
                d["volume"] = volume
                d["price"] = price
                d["millis"] = millis
                if code not in self.opend_dict:
                    self.opend_dict[code] = list()
                self.opend_dict[code].append(d)

    def save_opend_dict(self, file_path, stock_code):
        f = open(file_path, 'w')
        stock_list = self.opend_dict[stock_code]
        for item in stock_list:
            f.write(json.dumps(item, indent=4).replace('\n', '').replace('\t', '').replace(' ', '') + "\n")
        f.close()

    def analysis_server_json(self, file_path, stock_code):
        self.server_dict[stock_code] = list()
        for line in open(file_path, "r+"):
            line = line.strip()
            json_to_python = json.loads(line)
            seq = int(json_to_python["SeqNum"])
            time = json_to_python["SendTime"]
            ticker_id = json_to_python["TickerID"]
            price = json_to_python["Price"]
            volume = json_to_python["AggregateQuantity"]
            trade_time = int(json_to_python["TradeTime"] / 1000000000)
            d = dict()
            d["time"] = time
            d["volume"] = volume
            d["price"] = price
            d["trade_time"] = trade_time
            d["ticker_id"] = ticker_id
            self.server_dict[stock_code].append(d)

    def save_server_dict(self, file_path, stock_code):
        f = open(file_path, 'w')
        stock_list = self.server_dict[stock_code]
        for item in stock_list:
            f.write(json.dumps(item, indent=4).replace('\n', '').replace('\t', '').replace(' ', '') + "\n")
        f.close()

    def compare_item(self, source_item, target_item):
       return source_item["volume"] == target_item["volume"] and\
              source_item["price"] == target_item["price"]

    def compare(self, stock_code):
        source = self.server_dict[stock_code]
        target = self.opend_dict[stock_code]
        print(len(target))
        diff_result = list()
        target_offset = 0
        source_offset = 0
        find_start = False
        error_times = 0
        while target_offset < len(target) and source_offset < len(source):
            target_item = target[target_offset]
            source_item = source[source_offset]
            if not find_start:
                target_time_sec_tag = int(target_item["millis"] / 1000)
                source_time_sec_tag = int(source_item["trade_time"] / 1000)
                if abs(target_time_sec_tag - source_time_sec_tag) < 10 and self.compare_item(target_item, source_item):
                    print("----------start----------")
                    print(target_item["millis"])
                    print(source_item["trade_time"])
                    find_start = True
            if find_start:
                if not self.compare_item(target_item, source_item):
                    diff_result.append({"T": target_item, "S": source_item})
                    error_times = error_times + 1
                else:
                    error_times = 0
                target_offset = target_offset + 1
            source_offset = source_offset + 1
        return diff_result






if __name__ =="__main__":
    analysis = TickerAnalysis()
    analysis.analysis_opend_json("D:\\tmp\\Track_2018_12_18_1545104613515_TickerTest.log")
    analysis.save_opend_dict("D:\\tmp\\Track_OpenD.json", "HK.00700")

    analysis.analysis_server_json("D:\\tmp\\sort_700_ticker.json", "HK.00700")
    analysis.save_server_dict("D:\\tmp\\Track_Server.json", "HK.00700")

    diff_result = analysis.compare("HK.00700")
    with open("D:\\tmp\\diff_ticker", 'w')  as f:
        for item in diff_result:
            f.write(json.dumps(item, indent=4).replace('\n', '').replace('\t', '').replace(' ', '') + "\n")
    print(diff_result)
