from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename

#root window
root = Tk()

#design
root.geometry("800x600")
root.title("Tambarduine IDE")

scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)

main_path = ''

def comp_run():
    text_output.configure(state='normal')
    text_output.delete('1.0', END)
    text_output.insert('1.0',"Hey! You ran and compiled the code :)")
    text_output.configure(state='disabled')

def comp():
    #global main_path
    #if main_path == '':
    #    save_warning = Toplevel()
    #    notice = Label(save_warning, text="Please save the file first")
    #    notice.pack()
    #    return
    text_output.configure(state='normal')
    text_output.delete('1.0', END)
    text_output.insert('1.0',"Woah buddy, you've just compiled your code!")
    text_output.configure(state='disabled')

def open_file():
    path = askopenfilename(filetypes=[('Text Files','*.txt')])
    if path != '':
        with open(path, 'r') as file:
            code = file.read()
            text_info.delete('1.0', END)
            text_info.insert('1.0', code)
            global main_path
            main_path = path

def save():
    global main_path
    if main_path == '':
        path = asksaveasfilename(filetypes=[('Text Files','*.txt')])
        main_path = path
    else:
        path = main_path
    if path != '':
        with open(path, 'w') as file:
            code = text_info.get('1.0', END)
            file.write(code)

def save_as():
    global main_path
    path = asksaveasfilename(filetypes=[('Text Files','*.txt')])
    if path != '':
        main_path = path
        with open(path, 'w') as file:
            code = text_info.get('1.0', END)
            file.write(code)

text_info = Text(root, yscrollcommand=scrollbar.set)
text_info.config(bg='#362f2e', fg='#d2ded1', insertbackground='white')
text_info.pack(fill=BOTH)
scrollbar.config(command=text_info.yview)

text_output = Text(root, height=7)
text_output.config(bg='#362f2e', fg='#1dd604')
text_output.configure(state='disabled')
text_output.pack(fill=BOTH)

menu_bar = Menu(root)

file_bar = Menu(menu_bar, tearoff=0)
file_bar.add_command(label='Open', command = open_file)
file_bar.add_command(label='Save', command = save)
file_bar.add_command(label='SaveAs', command = save_as)
file_bar.add_command(label='Exit', command = exit)
menu_bar.add_cascade(label='File', menu = file_bar)

run_bar = Menu(menu_bar, tearoff=0)
run_bar.add_command(label='Compile', command = comp)
run_bar.add_command(label='Compile and Run', command = comp_run)
menu_bar.add_cascade(label='Compile', menu = run_bar)

root.config(menu=menu_bar)
root.resizable(False,False)
root.mainloop()
