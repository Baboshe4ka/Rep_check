import os
import hashlib
import docx
from pypdf import PdfReader 
from alive_progress import alive_bar
import logging
import json
from pyfiglet import Figlet 
 
#test_path = 'G:\Мой диск\Obsidian\Полка с книгами\Програмирование'


extentions_list= ('.pdf', '.TXT', '.docx', '.md')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ⓘ ")

def dir_dict(path):
    lits_of_files = []
    logger.info(f"Processing of folder: {path}")
    try:
        with alive_bar(len(os.listdir(path)), title= "Listing files") as bar:
            for file in os.listdir(path):
                if file.endswith(extentions_list):
                    print(f'🟢   File {file} processed')
                    lits_of_files.append(file)
                else:
                    print(f'🔴   File {file} denied')
                bar()
        logger.info("Processing end")
        sorted_list= list_sort(lits_of_files)
        directory_dict = { 'path': path, 
                        'content':sorted_list}
        logger.info("Dictinary created")
        return directory_dict
    except FileNotFoundError:
        print("⛔   Invalid path")
        return 1

def list_sort(lits_of_files):
    sorted_list= []
    with alive_bar(len(lits_of_files), title= "Sorting files") as bar:
        for file in lits_of_files:
            if file.endswith("pdf"):
                sorted_list.append(dict(name= file, extention = "pdf"))
            elif file.endswith("TXT"):
                sorted_list.append(dict(name= file, extention = "txt"))
            elif file.endswith(".docx"):
                sorted_list.append(dict(name= file, extention = "docx"))
            elif file.endswith(".md"):
                sorted_list.append(dict(name= file, extention = "md"))    
            bar()
    return sorted_list

def hash_encoder(dir_dict):
    if dir_dict != 1:    
        path = dir_dict['path']
        content = dir_dict['content']
        hash_list = []
        with alive_bar(len(content), title= "Encoding files") as bar:
            for i in content:
                name = i['name']
                ext=i['extention']
                try:
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
                    print(f'✅   File {name} encoded')
                except Exception:
                    print(f"⛔   Faild to encode: {name}")
                bar()
            return hash_list
    else:
        return 1

def json_creator(path):   
    hash_list= hash_encoder(dir_dict(path))
    if hash_list != 1:
        with open(f"{path}//hash.json", "w") as f:
            json.dump(hash_list, f, indent=4)
        logger.info("JSON created")
        return "JSON created"
    else:
        return 1

def json_reader(path):
    try:
        with open(f"{path}//hash.json", "r") as f:
            json_data= json.load(f)   
        hash_list= hash_encoder(dir_dict(path))
        result_list= []
        with alive_bar(len(hash_list), title= "Checking files") as bar:
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
                bar()
        return result_list
    except FileNotFoundError:
        print("👀   File with hash not found")
        return 1

def main():
    f = Figlet(font='isometric1')
    print (f.renderText('Rep Check'))
    action_text="What would you like to do?\n１ Create JSON\n２ Check Json\n❕ To stop type 'q'\n"
    action= input(action_text)
    while True:
        if action == "1":
            path = input("Path to foldet:\n")
            print(json_creator(path))
            action= input(action_text)
        elif action =="2":
            path = input("Path to foldet:\n")
            print(json_reader(path))
            action= input(action_text)
        elif action.lower() == "q":
            answ= input("❔ Are you sure (y/n)?\n")
            if answ.lower() =="y":
                return
            else:
                action= input(action_text)
        else:
            print("⛔   Incorrect input")
            action= input()
    
    
if __name__== "__main__":
    main()
