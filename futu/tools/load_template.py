import os


class FutuTemplate(object):
    def __init__(self, template_filename):
        self.local_path = os.path.dirname(os.path.realpath(__file__))
        self.template = dict()
        with open(os.path.join(self.local_path, template_filename), 'r', encoding='UTF-8') as load_f:
            begin_name = template_code = ""

            while True:
                line = load_f.readline()
                if not line:
                    break
                if len(line) > 10:
                    prefix = line[:10]
                else:
                    prefix = ""
                if prefix == "@@@@@@@@@@":  # 专用注释
                    continue
                if prefix == "##########":
                    if begin_name == "":
                        end = line.find('#', 11)
                        begin_name = line[10:end]
                        template_code = ""
                    else:
                        self.template[begin_name] = template_code
                        begin_name = template_code = ""
                    continue
                if begin_name != "":
                    template_code += line\


    @classmethod
    def code_add_space(cls, code, space_count=0, space_str="    "):  # 逐行加空格
        """传入字符串，逐行加入空格，符合python规范"""
        if space_count == 0:
            return code

        ls = code.split('\n')
        ret_code = space_line = ""
        for i in range(space_count):
            space_line += space_str

        for s in ls:
            if len(s) > 0:
                ret_code += (space_line + s + "\n")
            else:
                ret_code += "\n"

        return ret_code[:-1]

    def __getitem__(self, key):
        return self.template[key]

    def get(self, key, space_count=0):
        str_code = self[key]
        return self.code_add_space(str_code, space_count)











