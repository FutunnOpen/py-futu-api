# -*- coding: utf-8 -*-
import re
import json
import operator
import os


class BrokerAnalysis(object):
    """分析broker"""
    def __init__(self):
        self.opend_dict = dict()
        self.opend_find_dict = dict()
        self.server_find_dict = dict()
        self.server_dict = dict()

    @staticmethod
    def trim_list(items):
        """去除掉重复元素和脏数据"""
        new_list = []
        for item in items:
            new_sub_list = []
            for it in item:
                it = int(it)
                if it < 100: #小于100的不是券商id
                    continue
                new_sub_list.append(it)
            new_list.append(new_sub_list)

        last = []
        new_list2 = []
        for item in new_list:
            if operator.eq(item, last):
                continue
            else:
                last = item
                new_list2.append(item)
        return new_list2

    def analysis_opend_json(self, file_path):
        """从log里面找出关键数据"""
        self.opend_dict.clear()
        for line in open(file_path, "r+"):
            line = line.strip()
            json_to_python = json.loads(line)
            content = json_to_python["content"]
            if not isinstance(content, list):
                print(line)
                continue
            code = content[0].strip()
            bid_groups = content[1]
            ask_groups = content[2]
            ask_items = list()
            bid_items = list()
            for item in bid_groups:
                bid_items.append(item["bid_broker_id"])
            for item in ask_groups:
                ask_items.append(item["ask_broker_id"])

            if code in self.opend_dict:
                ask_id_list = self.opend_dict[code]["ask"]
                bid_id_list = self.opend_dict[code]["bid"]
            else:
                ask_id_list = list()
                bid_id_list = list()
                self.opend_dict[code] = dict()
                self.opend_dict[code]["ask"] = ask_id_list
                self.opend_dict[code]["bid"] = bid_id_list

            self.opend_find_dict[json_to_python["millis"]] = [ask_items, bid_items]
            ask_id_list.append(ask_items)
            bid_id_list.append(bid_items)

    def save_opend_dict(self, file_path):
        f = open(file_path, 'w')
        f.write(json.dumps(self.opend_dict, indent=4) + "\n")
        f.close()

    def trim_opend_dict(self):
        for v in self.opend_dict.values():
            v["ask"] = BrokerAnalysis.trim_list(v["ask"])
            v["bid"] = BrokerAnalysis.trim_list(v["bid"])


    @staticmethod
    def trim_server_items(json_items):
        match_group = []
        for it in json_items:
            t = it["Type"].strip()
            if t == "S":
                continue
            match_group.append(it["Item"])
        return match_group


    def analysis_server_json(self, file_path, stock_code):
        adict = {}
        for line in open(file_path, "r+"):
            line = line.strip()
            json_to_python = json.loads(line)
            seq = int(json_to_python["SeqNum"])
            if seq != 0:
                adict[seq] = json_to_python
        keys = sorted(adict)
        match_group_ask = []
        match_group_bid = []
        for k in keys:
            json_to_python = adict[k]
            side = int(json_to_python["Side"])
            if side == 2:
                trim_items = BrokerAnalysis.trim_server_items(json_to_python["items"])
                match_group_ask.append(trim_items)
                self.server_find_dict[k] = trim_items
            if side == 1:
                trim_items = BrokerAnalysis.trim_server_items(json_to_python["items"])
                match_group_bid.append(trim_items)
                self.server_find_dict[k] = trim_items

        self.server_dict[stock_code] = dict()
        self.server_dict[stock_code]["ask"] = match_group_ask
        self.server_dict[stock_code]["bid"] = match_group_bid


    def save_server_dict(self, file_path):
        f = open(file_path, 'w')
        f.write(json.dumps(self.server_dict, indent=4) + "\n")
        f.close()

    def trim_server_dict(self):
        for v in self.opend_dict.values():
            v["ask"] = BrokerAnalysis.trim_list(v["ask"])
            v["bid"] = BrokerAnalysis.trim_list(v["bid"])


    def compare(self, source, target):
        target_offset = 0
        source_offset = 0
        find_start = False
        error_times = 0
        targer_error_times = 0
        while target_offset < len(target) and source_offset < len(source):
            target_item = target[target_offset]
            source_item = source[source_offset]
            if not operator.eq(target_item, source_item):
                if not find_start:
                    source_offset = source_offset + 1
                else:
                    print(target_item)
                    print(source_item)
                    print("target_offset = " + str(target_offset + 1) + "       source_offset = " + str(source_offset + 1))
                    if error_times < 3:
                        source_offset = source_offset + 1
                        error_times = error_times + 1
                        targer_error_times = 0
                    else: #此路不通，再试试回滚后调整target_offset
                        source_offset = source_offset - error_times
                        error_times = 0
                        target_offset = target_offset + 1
                        targer_error_times = targer_error_times + 1
                if targer_error_times > 3:
                    print("------------------------")
                    break
            else:
                source_offset = source_offset + 1
                target_offset = target_offset + 1
                find_start = True
                error_times = 0
                targer_error_times = 0

        if not find_start:
            print("------no find_start----------")


    def compare_ask(self, stock_code):
        if stock_code in self.server_dict and stock_code in self.opend_dict:
            source = BrokerAnalysis.trim_list(self.server_dict[stock_code]["ask"])
            target = BrokerAnalysis.trim_list(self.opend_dict[stock_code]["ask"])
            self.compare(source, target)

    def compare_bid(self, stock_code):
        if stock_code in self.server_dict and stock_code in self.opend_dict:
            source = BrokerAnalysis.trim_list(self.server_dict[stock_code]["bid"])
            target = BrokerAnalysis.trim_list(self.opend_dict[stock_code]["bid"])
            self.compare(source, target)



class TickerAnalysis(object):
    """分析逐笔"""
    def __init__(self):
        self.opend_dict = dict()
        self.opend_find_dict = dict()
        self.server_find_dict = dict()
        self.server_dict = dict()

    def analysis_opend_json(self, file_path):
        """从log里面找出关键数据"""
        pass


if __name__ =="__main__":
    analysis = BrokerAnalysis()
    analysis.analysis_opend_json("C:\\Users\\dream\\AppData\\Roaming\\com.futunn.FutuOpenD\\Log\\Track_2018_11_20_1542695824589_BrokerTest.log")
    analysis.save_opend_dict("C:\\Users\\dream\\AppData\\Roaming\\com.futunn.FutuOpenD\\Log\\BrokerAnalysis.json")
    analysis.trim_opend_dict()
    analysis.save_opend_dict("C:\\Users\\dream\\AppData\\Roaming\\com.futunn.FutuOpenD\\Log\\BrokerAnalysis2.json")

    analysis.analysis_server_json("C:\\Users\\dream\\AppData\\Roaming\\com.futunn.FutuOpenD\\Log\\server.json", "HK.00700")
    analysis.save_server_dict("C:\\Users\\dream\\AppData\\Roaming\\com.futunn.FutuOpenD\\Log\\BrokerAnalysis_server1.json")
    analysis.trim_server_dict()
    analysis.save_server_dict("C:\\Users\\dream\\AppData\\Roaming\\com.futunn.FutuOpenD\\Log\\BrokerAnalysis_server2.json")

    analysis.compare_ask("HK.00700")


    # stock_list = ['HK.66173', 'HK.61039', 'HK.66284', 'HK.62748', 'HK.64836', 'HK.62329']
    # for stock in stock_list:
    #     compare_items(stock)

    # analysis_futu = BrokerAnalysis()
    # futu_match_group_ask, futu_match_group_bid = analysis_futu.analysis_futu('D:\\tmp\\ask.txt', 'D:\\tmp\\bid.txt')
    #
    # analysis_json = BrokerSourceAnalysis()
    # source_match_group_ask, source_match_group_bid, ask_dic, bid_dic = analysis_json.analysis('D:\\tmp\\sort_700_broker.json')
    #
    # save_items(futu_match_group_ask, "D:\\tmp\\futu__ask.txt")
    # save_items(source_match_group_ask, "D:\\tmp\\source__ask.txt")
    # # save_dics(ask_dic, "D:\\tmp\\source__ask__dics.txt")
    #
    # save_items(futu_match_group_ask, "D:\\tmp\\futu__bid.txt")
    # save_items(source_match_group_ask, "D:\\tmp\\source__bid.txt")
    # # save_dics(ask_dic, "D:\\tmp\\source__bid__dics.txt")
    #
    # broker_compare = BrokerSourceCompare()
    # broker_compare.compare(source_match_group_ask, futu_match_group_ask)
    # broker_compare.compare(source_match_group_bid, futu_match_group_bid)

