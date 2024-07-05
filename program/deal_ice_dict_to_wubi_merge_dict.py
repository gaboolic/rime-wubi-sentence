import os

def updateFile(fileName):
    
    # cn_dicts_path = os.path.expanduser("~/vscode/rime-frost/cn_dicts")
    cn_dicts_path = "cn_dicts_xh"
    yaml_file_path = os.path.join(cn_dicts_path, fileName)

    char_freq_map = {}
    file = open(yaml_file_path, 'r', encoding='utf-8')
    for line in file:
        if "\t" in line and not line.startswith("#"):
            line = line.strip()
            #print(line)
            params = line.split("\t")
            char = params[0]
            encode = params[1]
            if len(params) == 3:
                freq = (int) (params[2])
            else:
                freq = 0

            char_obj = {}

            if char in char_freq_map:
                freq = char_freq_map[char]["freq"] + freq
                char_obj["freq"] = freq
                char_obj["encode"] = encode
                char_freq_map[char] = char_obj
            else:
                char_obj["freq"] = freq
                char_obj["encode"] = encode
                char_freq_map[char] = char_obj
            
    #print(char_freq_map)

    # 将字典转换为列表以便进行排序
    char_freq_list = [(char, char_info['freq']) for char, char_info in char_freq_map.items()]

    # 按频率对列表进行倒序排序
    sorted_char_freq_list = sorted(char_freq_list, key=lambda x: x[1], reverse=True)

   

    # 将字典转换为列表以便进行排序
    # char_freq_list = [(char, int(freq)) for char, freq in char_freq_map.items()]

    # # 按频率对列表进行倒序排序
    # sorted_char_freq_list = sorted(char_freq_list, key=lambda x: x[1], reverse=True)


    write_file = open(os.path.join("cn_dicts_temp", fileName), 'w', encoding='utf-8')
    write_file.write(f"""# Rime dictionary
# encoding: utf-8
#
---
name: {fileName}
version: "2024-05-21"
sort: by_weight
...\n""")
     # 遍历按频率倒序排好序的数据
    for char, freq in sorted_char_freq_list:
        encode = char_freq_map[char]['encode']
    # 遍历按频率排好序的数据
    #for char, freq in sorted_char_freq_list:
        write_file.write(f"{char}\t{encode}\t{freq}\n")

file_list = ['8105.dict.yaml', '41448.dict.yaml', 'base.dict.yaml', 'ext.dict.yaml', 'others.dict.yaml']
for file_name in file_list:
    #fileName = "8105.dict.yaml"
    updateFile(file_name)