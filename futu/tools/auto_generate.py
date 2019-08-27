import sys
import os
from generate_code import generate

for arg in sys.argv:
    if len(sys.argv) < 1:
        break
    file_list = list()
    for str_path in sys.argv:
        (_, temp_name) = os.path.split(str_path)
        (file_name, _) = os.path.splitext(temp_name)
        file_list.append(file_name)
    generate(file_list)




