import os

def readFileAndWrite(path, fileName):
    file = open(path, 'r', encoding="utf8")
    lines = file.readlines()

    for index, line in enumerate(lines):
        with open(fileName, 'a', encoding='utf-8') as fp:
            fp.write(line)
    file.close()

def join(dir_path, fileName, headers):
    with open(fileName, 'a', encoding='utf-8') as fp:
                fp.write(headers)

    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            readFileAndWrite(os.path.join(dir_path, path), fileName)

def joinFiles():
    join('olx_files', 'step_1_joined_files\\olx_all.csv', 'publish_date;code;price;sell_diffs;attrs_values;attrs_keys;items;type;city;url;read_date\n')
    join('seminovos_files', 'step_1_joined_files\\seminovos_all.csv', 'code;publish_date;price;motor;brand_model;attrs_keys;attrs_values;items;type;address;read_date\n')