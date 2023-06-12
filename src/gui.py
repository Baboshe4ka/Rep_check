import customtkinter
import tkinter
import hash

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("500x300")
root.title("Rep Check")

#funcs
def create_json():
    if len(path_entry.get()) != 0:
        resp= hash.json_creator(path_entry.get())
        if resp !=1:
            output_text.configure(text = resp)
        else:
            output_text.configure(text = "⛔   Invalid path")
    

def check_json():
    if len(path_entry.get()) != 0:
        resp= hash.json_reader(path_entry.get())
        if resp !=1:
            text = "\n".join(resp)
            output_text.configure(text = text)
        else:
            output_text.configure(text = "👀   File with hash not found")    

#output
output_frame = customtkinter.CTkFrame(master=root)
output_frame.pack(padx = 60, pady=20)

output_label= customtkinter.CTkLabel(master=output_frame, text="Output\n", width=350 ,height=20)
output_label.pack(padx=10, pady=12)

output_text = customtkinter.CTkLabel(master=output_frame, text=None, justify="left", width=350 ,height=50)
output_text.pack(anchor=tkinter.SW)

#input
input_frame= customtkinter.CTkFrame(master=root)
input_frame.pack(padx = 60, pady=20)

entry_label = customtkinter.CTkLabel(master=input_frame, text="Path to folder:\n")
entry_label.pack(anchor=tkinter.SW)

path_entry = customtkinter.CTkEntry(master=input_frame, width=350 ,height=20)
path_entry.pack()

create_json_button = customtkinter.CTkButton(master=input_frame, text= "Create JSON", command = create_json)
create_json_button.pack()

check_json_button = customtkinter.CTkButton(master=input_frame, text= "Check JSON", command = check_json)
check_json_button.pack()

root.mainloop()
