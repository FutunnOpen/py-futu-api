import json
import os
from abc import abstractmethod
from bidict import bidict

__TemplateFile__ = "template.txt"


class FutuTemplate(object):
    def __init__(self):
        self.local_path = os.path.dirname(os.path.realpath(__file__))
        self.template = dict()
        with open(os.path.join(self.local_path, __TemplateFile__), 'r', encoding='UTF-8') as load_f:
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
                    template_code += line

    def __getitem__(self, key):
        return self.template[key]









