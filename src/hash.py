import os
import hashlib
import docx
from pypdf import PdfReader 
from alive_progress import alive_bar
import logging
import json


test_path = None
extentions_list= ['pdf', 'txt', 'docx', 'md']
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ⓘ ")

def dir_dict(path):
    lits_of_files = []
    logger.info(f"Processing of folder: {path}")
    with os.scandir(path) as it:
        for entry in it:
            if not entry.name.startswith(".") and entry.is_file:
                print(f'❖   File {entry.name} processed')
                lits_of_files.append(entry.name)
    logger.info("Processing end")
    sorted_list= list_sort(lits_of_files)
    directory_dict = { 'path': path, 
                    'content':sorted_list}
    logger.info("Dictinary created")
    return directory_dict

def list_sort(lits_of_files):
    sorted_list= []
    with alive_bar(len(lits_of_files), title= "Sorting files") as bar:
        for i in lits_of_files:
            file =i.split('.')
            if len(file) ==2:
                file_ext = file[1]
                if file_ext.lower() in extentions_list:
                    sorted_list.append(dict(name = i, extention= file_ext))
                    print(f'🟢   File {i} added')
                else:
                    print(f'🔴   File {i} denied')    
            else:
                print(f'⛔   Incorrect naming: {i} ')
            bar()
    return sorted_list

def hash_encoder(dir_dict):
    path = dir_dict['path']
    content = dir_dict['content']
    hash_list = []
    for i in content:
        name = i['name']
        ext=i['extention']
        if ext.lower() in ['txt', 'md']:
            with open(f"{path}//{name}", "r") as file:
                text = file.read() 
            hash_object = hashlib.md5(text.encode())
            hash_list.append(dict(name = name, hash_sum= hash_object.hexdigest()))
        elif ext.lower() == 'docx':
            file = docx.Document(f'{path}//{name}')
            text_list = []
            for para in file.paragraphs:
               text_list.append(para.text)
            text = '\n'.join(text_list)   
            hash_object = hashlib.md5(text.encode())
            hash_list.append(dict(name = name, hash_sum= hash_object.hexdigest()))
        elif ext.lower() == 'pdf':
            reader = PdfReader(f"{path}//{name}")
            text_list = []
            for page in range(len(reader.pages)):
                page = reader.pages[page]
                text_list.append(page.extract_text())
            text = '\n'.join(text_list)
            hash_object = hashlib.md5(text.encode())
            hash_list.append(dict(name = name, hash_sum= hash_object.hexdigest()))
    return hash_list

def json_creator(path):   
    hash_list= hash_encoder(dir_dict(path))
    with open(f"{path}//hash.json", "w") as f:
        json.dump(hash_list, f, indent=4)
    logger.info("JSON created")
    return "JSON created"

def json_reader(path):
    try:
        with open(f"{path}//hash.json", "r") as f:
            json_data= json.load(f)   
        hash_list= hash_encoder(dir_dict(path))
        result_list= []
        for file in hash_list:
            for json_file in json_data:
                if file["name"] == json_file["name"]:
                    if file["hash_sum"] == json_file["hash_sum"]:
                        name = file["name"]
                        text = f"✔️   {name} ok"
                        print(text)
                        result_list.append(text)
                    else:
                        name = file["name"]
                        text = f"❌   {name} has been changed"
                        print(text)
                        result_list.append(text)
        return result_list
    except FileNotFoundError:
        print("👀   File with hash not found")


def main():
    pass 


if __name__ == "main":
    main()




