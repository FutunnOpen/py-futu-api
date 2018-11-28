import json
import operator
import os
import datetime
import time


class OrderBookItem(object):
    """OrderBook"""
    def __init__(self, price, aggregate_quantity, number_of_orders, price_level, seq):
        self.price = price
        self.aggregate_quantity = aggregate_quantity
        self.number_of_orders = number_of_orders
        self.seq = seq
        self.price_level = price_level

    def __cmp__(self, other):
        if self.price < other.price:
            return -1
        if self.price > other.price:
            return 1
        if self.aggregate_quantity < other.aggregate_quantity:
            return -1
        if self.aggregate_quantity > other.aggregate_quantity:
            return 1
        if self.number_of_orders < other.number_of_orders:
            return -1
        if self.number_of_orders > other.number_of_orders:
            return 1
        if self.price_level < other.price_level:
            return -1
        if self.price_level > other.price_level:
            return 1
        return 0

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            r = (self.price == other.price) and \
                (self.aggregate_quantity == other.aggregate_quantity) and \
                (self.number_of_orders == other.number_of_orders) and \
                (self.price_level == other.price_level)

            return r
        else:
            return False


def order_book_to_dict(obj):
    if isinstance(obj, OrderBookItem):
        return [obj.price, obj.aggregate_quantity, obj.number_of_orders, obj.price_level]
    else:
        return None



class OrderBookAnalysis(object):
    """分析摆盘"""
    def __init__(self):
        self.opend_dict = dict()
        self.server_dict = dict()

    def compare_item(self, source, target):
        if isinstance(source, dict) and isinstance(target, dict):
            source_items = source["items"]
            target_items = target["items"]
        elif isinstance(source, list) and isinstance(target, list):
            source_items = source
            target_items = target
        else:
            return False

        if len(source_items) != len(target_items):
            return False
        if len(source_items) == 0:
            return True

        for i in range(len(source_items)):
            source_item = source_items[i]
            target_item = target_items[i]
            if source_item != target_item:
                return False
        return True



    def trim_opend_items(self, items, millis):
        result_lists = list()
        price_level = 1
        for item in items:
            if len(item) != 3:
                continue
            price = int(float(item[0])*1000)
            aggregate_quantity = item[1]
            number_of_orders = item[2]
            order_book_item = OrderBookItem(price, aggregate_quantity, number_of_orders, price_level, millis)
            result_lists.append(order_book_item)
            price_level = price_level + 1
        return result_lists


    def analysis_opend_json(self, file_path):
        """从log里面找出关键数据"""
        self.opend_dict.clear()

        for line in open(file_path, "r+"):
            line = line.strip()
            json_to_python = json.loads(line)
            content = json_to_python["content"]
            millis = json_to_python["millis"]
            un_time = int(millis / 1000)
            code = content["code"]
            bid_groups = content["Bid"]
            ask_groups = content["Ask"]
            ask_items = self.trim_opend_items(ask_groups, millis)
            bid_items = self.trim_opend_items(bid_groups, millis)
            if code not in self.opend_dict:
                self.opend_dict[code] = dict()
                self.opend_dict[code]["ask"] = list()
                self.opend_dict[code]["bid"] = list()
            self.opend_dict[code]["ask"].append({"seq": millis, "time": un_time, "items": ask_items})
            self.opend_dict[code]["bid"].append({"seq": millis, "time": un_time, "items": bid_items})
        self.trim_items(self.opend_dict["HK.00700"]["ask"])

    def save_opend_dict(self, file_path, stock_code):
        f = open(file_path + "_ask.txt", 'w')
        ask_items = self.opend_dict[stock_code]["ask"]
        for item in ask_items:
            f.write(json.dumps(item, indent=4, default=order_book_to_dict).replace('\n', '').replace('\t', '').replace(' ', '') + "\n")
        f.close()

        f = open(file_path + "_bid.txt", 'w')
        bid_items = self.opend_dict[stock_code]["bid"]
        for item in bid_items:
            f.write(json.dumps(item, indent=4, default=order_book_to_dict).replace('\n', '').replace('\t', '').replace(' ', '') + "\n")
        f.close()

    def analysis_server_json(self, file_path, stock_code):
        self.server_dict[stock_code] = dict()
        self.server_dict[stock_code]["ask"] = list()
        self.server_dict[stock_code]["bid"] = list()

        for line in open(file_path, "r+"):
            line = line.strip()
            json_to_python = json.loads(line)
            seq = int(json_to_python["SeqNum"])
            send_time = json_to_python["SendTime"]
            order_book_items_ask = list()
            order_book_items_bid = list()
            dtime = datetime.datetime.strptime(send_time, "%Y-%m-%d %H:%M:%S")
            un_time = int(time.mktime(dtime.timetuple()))
            for item in json_to_python["BookEntries"]:
                price = item["Price"]
                aggregate_quantity = item["AggregateQuantity"]
                number_of_orders = item["NumberOfOrders"]
                price_level = item["PriceLevel"]
                order_book_item = OrderBookItem(price, aggregate_quantity, number_of_orders, price_level, seq)
                side = item["Side"]
                if side == 1:
                    order_book_items_ask.append(order_book_item)
                elif side == 0:
                    order_book_items_bid.append(order_book_item)
            if len(order_book_items_ask) > 0:
                self.server_dict[stock_code]["ask"].append({"seq": seq, "time": un_time, "items": order_book_items_ask})
            if len(order_book_items_bid) > 0:
                self.server_dict[stock_code]["bid"].append({"seq": seq, "time": un_time, "items": order_book_items_bid})

    def save_server_dict(self, file_path, stock_code):
        f = open(file_path + "_ask.txt", 'w')
        ask_items = self.server_dict[stock_code]["ask"]
        for item in ask_items:
            f.write(json.dumps(item, indent=4, default=order_book_to_dict).replace('\n', '').replace('\t', '').replace(' ', '') + "\n")
        f.close()

        f = open(file_path + "_bid.txt", 'w')
        bid_items = self.server_dict[stock_code]["bid"]
        for item in bid_items:
            f.write(json.dumps(item, indent=4, default=order_book_to_dict).replace('\n', '').replace('\t', '').replace(' ', '') + "\n")
        f.close()

    def trim_items(self, items):
        """去除掉重复元素和脏数据"""
        new_list = list()
        last = None
        for item in items:
            if self.compare_item(item, last):
                continue
            else:
                last = item
                new_list.append(item)
        return new_list

    def compare(self, source, target):
        diff_result = list()
        target_offset = 0
        source_offset = 0
        find_start = False
        error_times = 0
        while target_offset < len(target) and source_offset < len(source):
            target_items = target[target_offset]["items"]
            source_items = source[source_offset]["items"]
            if not find_start:
                target_time_sec_tag = target[target_offset]["time"]
                source_time_sec_tag = source[source_offset]["time"]
                if abs(target_time_sec_tag - source_time_sec_tag) < 10 :
                    if self.compare_item(target_items, source_items):
                        print("----------start----------")
                        print(target_time_sec_tag)
                        print(source_time_sec_tag)
                        find_start = True
            if find_start:
                if not self.compare_item(target_items, source_items):
                    diff_result.append({"T": target_items, "S": source_items})
                    error_times = error_times + 1
                    if error_times > 3:
                        break
                else:
                    error_times = 0
                target_offset = target_offset + 1
            source_offset = source_offset + 1
        return diff_result



    def compare_ask(self, stock_code):
        source = self.server_dict[stock_code]["ask"]
        target = self.opend_dict[stock_code]["ask"]
        return self.compare(self.trim_items(source), self.trim_items(target))




if __name__ =="__main__":

    analysis = OrderBookAnalysis()
    analysis.analysis_opend_json("D:\\tmp\\Track_2018_11_21_1542768961719_OrderBookTest.log")
    analysis.save_opend_dict("D:\\tmp\\OrderBook_OpenD", "HK.00700")
    analysis.analysis_server_json("D:\\tmp\\sort_700_AggregateOrderBookUpdate_11_21.json", "HK.00700")
    analysis.save_server_dict("D:\\tmp\\OrderBook_Server", "HK.00700")
    print(analysis.compare_ask("HK.00700"))
