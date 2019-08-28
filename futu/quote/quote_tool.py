import pandas as pd
from futu.quote.quote_query import *


class OpenQuoteTool(object):

    def __init__(self, context):
        self.quote_context = context
        if context is None:
            raise Exception("context is empty!")

    def save_delay_statistics(self, file_path):
        if file_path is None:
            return
        html_file = open(file_path, 'w', encoding='utf-8')
        local_path = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(local_path, "head.html"), 'r', encoding='utf-8') as html_head_file:
            html_file.write(html_head_file.read())

        segment_list = [0, 2, 4, 6, 8, 10, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56,
                        60, 64, 68, 72, 76, 80, 84, 88, 92, 96, 100, 110, 120, 130, 140,
                        150, 160, 170, 180, 200, 250, 300, 500, 1000, -1]
        req_head_describe = [("proto_id", "命令字"),
                             ("count", "请求个数"),
                             ("is_local_reply", "是否本地数据"),
                             ("total_cost_avg", "总体延迟平均值（ms）")]

        push_head_describe = [("begin", "速度区间ms（开始）"),
                              ("end", "速度区间ms（结束）"),
                              ("proportion", "当前区段占比"),
                              ("count", "包数"),
                              ("cumulative_ratio", "累计占比")]

        for stage_type in QotPushStage.ALL[::-1]:

            if stage_type == QotPushStage.SR2_CS:
                delay_statistics_type = DelayStatisticsType.ALL
            else:
                delay_statistics_type = [DelayStatisticsType.QOT_PUSH]
            err, dic = self.quote_context.get_delay_statistics(
                delay_statistics_type,
                stage_type,
                segment_list)
            if err != RET_OK:
                return

            qot_pushes = dic["qot_push"]
            req_replies = dic["req_reply"]
            place_orders = dic["place_order"]
            print(qot_pushes, req_replies, place_orders)

            html_file.write(
                "<div class='title'>{}</div><HR>\n".format(QotPushStage.get_describe(stage_type)))

            if len(qot_pushes) > 0:
                html_file.write("<div class='sub-title'>推送耗时统计</div>\n")

                col_list = list()
                col_new_head = list()
                for t in push_head_describe:
                    col_list.append(t[0])
                    col_new_head.append(t[1])

                for push in qot_pushes:
                    df = pd.DataFrame(push["list"], columns=col_list)
                    df.drop(df[df.proportion == 0.0].index, inplace=True)
                    if len(df) == 0:
                        continue
                    df['proportion'] = df['proportion'].map(
                        lambda x: format(x/100, '.2%'))
                    df['cumulative_ratio'] = df['cumulative_ratio'].map(
                        lambda x: format(x / 100, '.2%'))

                    # df["cumulative_ratio"] = df["begin"].map(str) + ' - ' + df["end"].map(str)
                    df.insert(0, 'interval', '')
                    try:
                        df["interval"] = df.apply(lambda x: str(
                            x.begin) + 'ms - ' + str(x.end) + "ms", axis=1)
                    except Exception as e:
                        print("df.apply error", e)
                        pass

                    df.drop(['begin', 'end'], axis=1,
                            inplace=True)  # 删除begin、end
                    col_new_head = ['统计区间（ms）', '百分比', '包数', '总体延迟百分比']
                    df.columns = col_new_head
                    qot_push_type = QotPushType.to_string2(
                        push["qot_push_type"])
                    html_file.write(
                        "<div class='item'>{}推送耗时</div>".format(QotPushType.get_describe(qot_push_type)))
                    html_file.write(df.to_html(header=True, index=False))
                    html_file.write("<br>\n")

            if len(req_replies) > 0:
                html_file.write("<div class='sub-title'>命令字请求耗时统计</div>")
                col_list = list()
                col_new_head = list()
                for t in req_head_describe:
                    col_list.append(t[0])
                    col_new_head.append(t[1])
                df = pd.DataFrame(req_replies, columns=col_list)
                df.columns = col_new_head
                html_file.write(df.to_html(header=True, index=False))
                html_file.write("<br>\n")

            if len(place_orders) > 0:
                html_file.write("<div class='sub-title'>下单统计耗时</div>")
                df = pd.DataFrame(place_orders)
                html_file.write(df.to_html(header=True, index=False))
                html_file.write("<br><br>\r\n")

        html_file.write("</body></html>")
        html_file.close()
