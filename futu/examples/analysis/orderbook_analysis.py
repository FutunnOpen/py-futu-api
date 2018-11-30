import json
import operator
import os
import datetime
import time
import copy

class OrderBookItem(object):

    def __init__(self, price=0, aggregate_quantity=0, number_of_orders=0, price_level=0, update_action=0, seq=0):
        self.price = price
        self.aggregate_quantity = aggregate_quantity
        self.number_of_orders = number_of_orders
        self.seq = seq
        self.price_level = price_level
        self.update_action = update_action

    # def __init__(self):
    #     self.price = 0
    #     self.aggregate_quantity = 0
    #     self.number_of_orders = 0
    #     self.seq = 0
    #     self.price_level = 0
    #     self.update_action = 0

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
            order_book_item = OrderBookItem(price, aggregate_quantity, number_of_orders, price_level, 0, millis)
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

    # def analysis_server_json(self, file_path, stock_code):
    #     self.server_dict[stock_code] = dict()
    #     self.server_dict[stock_code]["ask"] = list()
    #     self.server_dict[stock_code]["bid"] = list()
    #
    #     for line in open(file_path, "r+"):
    #         line = line.strip()
    #         json_to_python = json.loads(line)
    #         seq = int(json_to_python["SeqNum"])
    #         send_time = json_to_python["SendTime"]
    #         order_book_items_ask = list()
    #         order_book_items_bid = list()
    #         dtime = datetime.datetime.strptime(send_time, "%Y-%m-%d %H:%M:%S")
    #         un_time = int(time.mktime(dtime.timetuple()))
    #         for item in json_to_python["BookEntries"]:
    #             price = item["Price"]
    #             aggregate_quantity = item["AggregateQuantity"]
    #             number_of_orders = item["NumberOfOrders"]
    #             price_level = item["PriceLevel"]
    #             update_action = item["UpdateAction"]
    #             order_book_item = OrderBookItem(price, aggregate_quantity, number_of_orders, price_level, update_action, seq)
    #             side = item["Side"]
    #             if side == 1:
    #                 order_book_items_ask.append(order_book_item)
    #             elif side == 0:
    #                 order_book_items_bid.append(order_book_item)
    #         if len(order_book_items_ask) > 0:
    #             self.server_dict[stock_code]["ask"].append({"seq": seq, "time": un_time, "items": order_book_items_ask})
    #         if len(order_book_items_bid) > 0:
    #             self.server_dict[stock_code]["bid"].append({"seq": seq, "time": un_time, "items": order_book_items_bid})


    def analysis_server_json2(self, file_path, stock_code):
        ask_ten_order_book = list()
        bid_ten_order_book = list()
        for i in range(10):
            ask_ten_order_book.append(OrderBookItem())
            bid_ten_order_book.append(OrderBookItem())

        self.server_dict[stock_code] = dict()
        self.server_dict[stock_code]["ask"] = list()
        self.server_dict[stock_code]["bid"] = list()

        for line in open(file_path, "r+"):
            line = line.strip()
            json_to_python = json.loads(line)
            seq = int(json_to_python["SeqNum"])
            send_time = json_to_python["SendTime"]
            dtime = datetime.datetime.strptime(send_time, "%Y-%m-%d %H:%M:%S")
            un_time = int(time.mktime(dtime.timetuple()))
            for item in json_to_python["BookEntries"]:
                price = item["Price"]
                aggregate_quantity = item["AggregateQuantity"]
                number_of_orders = item["NumberOfOrders"]
                price_level = item["PriceLevel"]
                update_action = item["UpdateAction"]
                order_book_item = OrderBookItem(price, aggregate_quantity, number_of_orders, price_level, update_action, seq)
                side = item["Side"]
                if side == 1:
                    self.trim_server_ten_order(ask_ten_order_book, order_book_item, side)
                elif side == 0:
                    self.trim_server_ten_order(bid_ten_order_book, order_book_item, side)

            self.server_dict[stock_code]["ask"].append({"seq": seq, "time": un_time, "items": copy.deepcopy(ask_ten_order_book)})
            self.server_dict[stock_code]["bid"].append({"seq": seq, "time": un_time, "items": copy.deepcopy(bid_ten_order_book)})

    def update_server_ten_order(self, ten_order_books, side, step_price=200):
        if side == 0:
            step_price = -step_price
        first_price = ten_order_books[0].price
        order_books_len = len(ten_order_books)

        if first_price == 0:
            return

        for i in range(10):
            price = first_price + step_price * i
            price_level = i + 1

            # 不足10个就填满
            if i > order_books_len - 1:
                ten_order_books.append(OrderBookItem(price, 0, 0, price_level, 0, 0))
            else:
                order_item = ten_order_books[i]

                if order_item.price != price:
                    has_empty = False
                    if side == 0 and order_item.price < price: #bid是逐个减小的
                        has_empty = True
                    elif side == 1 and order_item.price > price:#ask是逐个增大的
                        has_empty = True
                    if has_empty:
                        ten_order_books.insert(i, OrderBookItem(price, 0, 0, price_level, 0, 0))
                        continue
                    order_item.aggregate_quantity = 0

                order_item.price = price
                order_item.price_level = price_level

        if len(ten_order_books) > 10:
            for i in range(len(ten_order_books) - 10):
                ten_order_books.pop(10)

    def trim_server_ten_order(self, ten_order_book, order_book_item, side):
        price_index = order_book_item.price_level - 1
        update_action = order_book_item.update_action
        self.update_server_ten_order(ten_order_book, side)

        if update_action == 0:
            ten_order_book.insert(price_index, order_book_item)
        elif update_action == 1:
            ten_order_book[price_index] = order_book_item
        elif update_action == 2:
            ten_order_book.pop(price_index)
        self.update_server_ten_order(ten_order_book, side)

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
                if target_items[0].price == 0:
                    target_offset = target_offset + 1
                    continue
                target_time_sec_tag = target[target_offset]["time"]
                source_time_sec_tag = source[source_offset]["time"]

                if abs(target_time_sec_tag - source_time_sec_tag) < 10:
                    if self.compare_item(target_items, source_items):
                        print("----------start----------")
                        print(target_time_sec_tag)
                        print(source_time_sec_tag)
                        find_start = True
            if find_start:
                if not self.compare_item(target_items, source_items):
                    diff_result.append({"T": {"target_time_sec_tag": target_time_sec_tag, "items": target_items}, \
                                        "S": {"source_time_sec_tag": source_time_sec_tag, "items": source_items}})
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

    def compare_bid(self, stock_code):
        source = self.server_dict[stock_code]["bid"]
        target = self.opend_dict[stock_code]["bid"]
        return self.compare(self.trim_items(source), self.trim_items(target))


if __name__ =="__main__":

    analysis = OrderBookAnalysis()
    analysis.analysis_server_json2("D:\\tmp\\sort_700_AggregateOrderBookUpdate.json", "HK.00700")
    analysis.save_server_dict("D:\\tmp\\OrderBook2_Server", "HK.00700")

    analysis.analysis_opend_json("D:\\tmp\\Track_2018_11_28_1543370754387_OrderBookTest.log")
    analysis.save_opend_dict("D:\\tmp\\OrderBook_OpenD", "HK.00700")

    # analysis.analysis_server_json("D:\\tmp\\sort_700_AggregateOrderBookUpdate.json", "HK.00700")
    # analysis.save_server_dict("D:\\tmp\\OrderBook_Server", "HK.00700")
    diff_result = analysis.compare_ask("HK.00700")

    with open("D:\\tmp\\diff_OrderBookAnalysis_ask.txt", 'w') as f:
        for item in diff_result:
            f.write(json.dumps(item, indent=4, default=order_book_to_dict).replace('\n', '').replace('\t', '').replace(' ', '') + "\n")

    diff_result = analysis.compare_bid("HK.00700")
    with open("D:\\tmp\\diff_OrderBookAnalysis_bid.txt", 'w') as f:
        for item in diff_result:
            f.write(json.dumps(item, indent=4, default=order_book_to_dict).replace('\n', '').replace('\t', '').replace(' ', '') + "\n")