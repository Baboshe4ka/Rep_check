import os

test_path = "D:\\Strong Coding\\Python\\Rep_check\\src\\"
extentions_list= ['pdf', 'txt', 'doc', 'docx', 'py']

def dir_list(path):
    lits_of_files = []
    with os.scandir(path) as it:
        for entry in it:
            if not entry.name.startswith(".") and entry.is_file:
                print(f'[!]{entry.name}')
                lits_of_files.append(entry.name)
    return lits_of_files

def list_sort(lits_of_files):
    sorted_list= []
    for i in lits_of_files:
        file =i.split('.')
        if file[1] in extentions_list:
            sorted_list.append(i)
            print(f'[+]{i}')
    return sorted_list

lst = dir_list(test_path)
sorted_lst=(list_sort(lst))
print(lst, '\n',sorted_lst)


