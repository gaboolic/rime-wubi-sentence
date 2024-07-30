import os

# Function to read a file
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Function to write content to a file
def write_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

# Function to update missing encodings in the file
def update_missing_encodings(file_path, write_file_path, dict_data):
    # Read the file content
    file_content = read_file(file_path)
    # Split the content into lines
    lines = file_content.split('\n')
    # Create an updated content variable
    updated_content = ''

    char_map = {}
    # Process each line
    for line in lines:
        if '\t' not in line or line.startswith("#"):
            updated_content += line + '\n'
            continue
        
        char_list = line.split('\t')[0]
        if char_list in char_map:
            continue

        lack_flag = False
        for char in char_list:
            if char not in dict_data:
                print("缺失"+char)
                lack_flag = True
                continue
        if lack_flag:
            continue

        word_encode_list = []
        for char in char_list:
            if char not in dict_data:
                print("缺失"+char)
                continue
            dict_encode_list = dict_data[char]
            dict_encode = ';'.join(dict_encode_list)
            word_encode_list.append(dict_encode)

        word_encode = ' '.join(word_encode_list)
        if char_list in word_freq:
            freq = word_freq[char_list]
        else:
            freq = 0
        updated_line = f"{char_list}\t{word_encode}\t{freq}"
        updated_content += updated_line + '\n'
        char_map[char_list] = ''

    # Write the updated content back to the file
    write_file(write_file_path, updated_content)

# 载入频率
freq_file = open(os.path.expanduser("~/vscode/rime-frost/others/知频.txt"), 'r', encoding='utf-8')
word_freq = {}
for line in freq_file:
    line = line.strip()
    params = line.split("\t")
    word = params[0]
    freq = int(params[1])

    if word in word_freq:
        word_freq[word] += freq
    else:
        word_freq[word] = freq

dict_data = {}



with open('program/tiger.dict.yaml', 'r', encoding='utf-8') as dict_file:
    lines = dict_file.readlines()  # 读取所有行到列表中  

    for line in reversed(lines):
        if "\t" in line and not line.startswith("#"):
            
            params = line.strip().split('\t')
            if len(params) == 4:
                continue
            character = params[0]
            encoding = params[1]
            if len(encoding) == 1:
                continue
            if character == '纛':
                print("纛")
                print(line)
            encode_left = encoding[0:2]

            encode_right = encoding[2:]
            compare_encoding = encode_left + ',' + encode_right
            if len(encode_right) == 1:
                encode_right = encode_right + '0'
            if len(encode_right) == 0:
                encode_right = '00'

            encoding = encode_left + ',' + encode_right
            
            if character not in dict_data:
                dict_data[character] = [encoding]
            else:
                add_flag = True
                if character == '纛':
                    print("dict_data[character]:")
                    print(dict_data[character])
                for exist_encode in dict_data[character]:
                    if exist_encode.startswith(encoding) or exist_encode.startswith(compare_encoding):
                        add_flag = False
                    if encoding.startswith(exist_encode) or encoding.startswith(exist_encode.rstrip('0') ):
                        add_flag = False
                if add_flag:
                    dict_data[character].append(encoding)
                else:
                    pass


print(dict_data['巴'])
print(dict_data['不'])
print(dict_data['𩽾'])

file_list = ['8105.dict.yaml', '41448.dict.yaml', 'base.dict.yaml', 'ext.dict.yaml', 'others.dict.yaml']
for file_name in file_list:
    # File paths
    cn_dicts_path = os.path.expanduser("~/vscode/rime-frost/cn_dicts")
    yaml_file_path = os.path.join(cn_dicts_path, file_name)
    write_file_path = os.path.join('cn_dicts_tiger', file_name)

    print(yaml_file_path)
    # Update missing encodings in the file
    update_missing_encodings(yaml_file_path, write_file_path, dict_data)
