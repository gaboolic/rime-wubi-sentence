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

    # Process each line
    for line in lines:
        if '\t' not in line or line.startswith("#"):
            updated_content += line + '\n'
            continue

        frequency = None
         # 检查分割出的值是否足够
        if len(line.split('\t')) == 3:
            character, encoding, frequency = line.split('\t')
        else:
            character, encoding = line.split('\t')
        
        
        if "tencent" in file_path :
            updated_line = f"{character}\t99"
            updated_content += updated_line + '\n'
            continue
        else:
            if encoding == "100":
                updated_content += line + '\n'
                continue

        pinyin_list = encoding.split(" ")
        double_list = ""
        pinyin_index = 0
        for pinyin in pinyin_list:
            
            encode = pinyin[3:]
            
            encode_left = encode[0:2]
            encode_right = encode[2:]
                
                
            clean_character = character.replace("·", "")
            character_encoding_pre = clean_character[pinyin_index]
            # character_encoding_pre = character[pinyin_index]
            encoding_post = dict_data.get(character_encoding_pre, "[")
            double_list += f"{encode_left}[{encode_right} "
            pinyin_index += 1
        
        double_list = double_list[:-1]

        if "[[" in double_list:
            # updated_content += line + '\n'
            pass

        if "tencent" in file_path :
            updated_line = f"{character}\t99"
        else:
            if frequency is not None:
                updated_line = f"{character}\t{double_list}\t{frequency}"
            else :
                updated_line = f"{character}\t{double_list}"
        updated_content += updated_line + '\n'

    # Write the updated content back to the file
    write_file(write_file_path, updated_content)

dict_data = {}
file_list = ['8105.dict.yaml', '41448.dict.yaml', 'base.dict.yaml', 'ext.dict.yaml', 'others.dict.yaml']
# file_list = [ 'tencent.dict.yaml']
# Load the dict data from the provided file
with open('./program/wubi.dict.yaml', 'r', encoding='utf-8') as dict_file:
    for line in dict_file:
        if "\t" in line:
            line = line.strip()
            #print(line)
            params = line.strip().split('\t')
            character = params[0]
            encoding = params[1]
            if "'" not in encoding:
                encoding_pre = encoding[:2]
                encoding_post = encoding[2:]
                # if character in '去我而人他有是出哦配啊算的非个和就可了在小从这吧你吗':
                #     if len(encoding_post) == 2:
                #         encoding_post = encoding_post[0] + encoding_post[1].upper()
                # if character not in dict_data:
                #     dict_data[character] = encoding
                dict_data[character] = encoding


# print("巴 " + dict_data['巴'])
# print("𬱖 " + dict_data['𬱖'])

for file_name in file_list:
    # File paths
    cn_dicts_path = "cn_dicts_wb"
    yaml_file_path = os.path.join(cn_dicts_path, file_name)
    write_file_path = os.path.join('cn_dicts_xh', file_name)

    print(yaml_file_path)
    # Update missing encodings in the file
    update_missing_encodings(yaml_file_path, write_file_path, dict_data)
