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

        self.diff_result = list()
        self.error_times = 0

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

            if code not in self.opend_dict:
                self.opend_dict[code] = dict()
                self.opend_dict[code]["ask"] = list()
                self.opend_dict[code]["bid"] = list()

            if code not in self.opend_find_dict:
                self.opend_find_dict[code] = dict()

            self.opend_find_dict[code][json_to_python["millis"]] = {"ask": ask_items, "bid": bid_items}
            self.opend_dict[code]["ask"].append(ask_items)
            self.opend_dict[code]["bid"].append(bid_items)


    def save_opend_dict(self, file_path, stock_code):
        f = open(file_path, 'w')
        stock_dict = self.opend_find_dict[stock_code]
        keys = sorted(stock_dict)
        for k in keys:
            v = stock_dict[k]
            f.write(json.dumps({k: v}, indent=4).replace('\n', '').replace('\t', '').replace(' ', '') + "\n")
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
        send_time_dict = dict()
        self.server_find_dict[stock_code] = dict()
        for line in open(file_path, "r+"):
            line = line.strip()
            json_to_python = json.loads(line)
            seq = int(json_to_python["SeqNum"])
            if seq != 0:
                adict[seq] = json_to_python
            send_time_dict[seq] = json_to_python["SendTime"]
        keys = sorted(adict)
        match_group_ask = []
        match_group_bid = []
        for k in keys:
            json_to_python = adict[k]
            side = int(json_to_python["Side"])
            if side == 2:
                trim_items = BrokerAnalysis.trim_server_items(json_to_python["items"])
                match_group_ask.append(trim_items)
                self.server_find_dict[stock_code][k] = {"items": trim_items, "side": side, "sendtime": send_time_dict[k]}
            if side == 1:
                trim_items = BrokerAnalysis.trim_server_items(json_to_python["items"])
                match_group_bid.append(trim_items)
                self.server_find_dict[stock_code][k] = {"items": trim_items, "side": side, "sendtime": send_time_dict[k]}

        self.server_dict[stock_code] = dict()
        self.server_dict[stock_code]["ask"] = match_group_ask
        self.server_dict[stock_code]["bid"] = match_group_bid


    def save_server_dict(self, file_path, stock_code, filter = None):
        f = open(file_path, 'w')
        stock_dict = self.server_find_dict[stock_code]
        keys = sorted(stock_dict)
        for k in keys:
            v = stock_dict[k]
            side = v["side"]
            if filter == "ask" and side != 2:
                continue
            if filter == "bid" and side != 1:
                continue
            f.write(json.dumps({k: v}, indent=4).replace('\n', '').replace('\t', '').replace(' ', '') + "\n")
        f.close()

    def trim_server_dict(self):
        for v in self.server_dict.values():
            v["ask"] = BrokerAnalysis.trim_list(v["ask"])
            v["bid"] = BrokerAnalysis.trim_list(v["bid"])


    def try_find_opend_items(self, find_item, side, stock_code):
        find_list = list()
        for k, v in self.opend_find_dict[stock_code].items():
            item = v[side]
            if operator.eq(find_item, item):
                find_list.append({"millis": k})
        return find_list



    def try_find_server_items(self, find_item, side, stock_code):
        find_list = list()

        target_side = 1
        if side == "ask":
            target_side = 2

        for k, v in self.server_find_dict[stock_code].items():
            source_side = v["side"]
            if target_side == source_side:
                item = v["items"]
                if operator.eq(find_item, item):
                    d = dict()
                    d["SeqNum"] = k
                    d["SendTime"] = v["sendtime"]
                    find_list.append(d)
        return find_list


    def compare(self, source, target, source_offset=0, target_offset= 0):
        if source_offset == 0 and target_offset == 0:
            self.diff_result = list()
            self.error_times = 0
        find_start = False
        find_start_times = 0 #连续重复3个才能认为是找到了
        while target_offset < len(target) and source_offset < len(source):
            target_item = target[target_offset]
            source_item = source[source_offset]
            if not operator.eq(target_item, source_item):
                find_start_times = 0
                if not find_start:
                    source_offset = source_offset + 1
                    continue
                else:
                    self.diff_result.append({"S": source_item, "T": target_item})
                    self.error_times = self.error_times + 1
                    source_offset = source_offset + 1
                    target_offset = target_offset + 1
                    self.compare(source, target, source_offset, target_offset)
                    break
            else:
                if not find_start and len(target_item) > 0:
                    find_start_times = find_start_times + 1
                if find_start_times > 5:
                    find_start = True

            source_offset = source_offset + 1
            target_offset = target_offset + 1

        if not find_start:
            print("------no find_start----------")

        return self.diff_result


    def compare_ask(self, stock_code):
        if stock_code in self.server_dict and stock_code in self.opend_dict:
            source = BrokerAnalysis.trim_list(self.server_dict[stock_code]["ask"])
            target = BrokerAnalysis.trim_list(self.opend_dict[stock_code]["ask"])
            return self.compare(source, target)


    def compare_bid(self, stock_code):
        if stock_code in self.server_dict and stock_code in self.opend_dict:
            source = BrokerAnalysis.trim_list(self.server_dict[stock_code]["bid"])
            target = BrokerAnalysis.trim_list(self.opend_dict[stock_code]["bid"])
            self.compare(source, target)
            return self.compare(source, target)

    def save_compare_result(self, diff_result, side, stock_code, file_path):
        f = open(file_path, 'w')
        for item in diff_result:
            target_item = item["T"]
            source_item = item["S"]
            target_find_item = self.try_find_opend_items(target_item, side, stock_code)
            source_find_item = self.try_find_server_items(source_item, side, stock_code)
            f.write("T ={} \n".format(str(target_item).replace(' ', '')))
            f.write("S ={} \n".format(str(source_item).replace(' ', '')))
            f.write("OpenD ={} \n".format(
                json.dumps(target_find_item, indent=4).replace('\n', '').replace('\t', '').replace(' ', '')))
            f.write("Server ={} \n".format(
                json.dumps(source_find_item, indent=4).replace('\n', '').replace('\t', '').replace(' ', '')))
            f.write("----------------------------------------\n")
        f.close()



if __name__ =="__main__":
    analysis = BrokerAnalysis()
    analysis.analysis_opend_json("D:\\tmp\\Track_2018_12_18_1545104613045_BrokerTest.log")
    analysis.save_opend_dict("D:\\tmp\\Broker_OpenD.json", "HK.00700")
    analysis.analysis_server_json("D:\\tmp\\sort_700_BrokerQueue.json", "HK.00700")
    analysis.save_server_dict("D:\\tmp\\Broker_Server.json", "HK.00700", "ask")

    diff_result = analysis.compare_ask("HK.00700")
    analysis.save_compare_result(diff_result, "ask", "HK.00700", "D:\\tmp\\diff_result_ask.json")

    diff_result = analysis.compare_bid("HK.00700")
    analysis.save_compare_result(diff_result, "bid", "HK.00700", "D:\\tmp\\diff_result_bid.json",)

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

