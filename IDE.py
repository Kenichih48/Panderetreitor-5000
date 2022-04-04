from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
import threading
import time
from analizadorSintactico import *

#root window
root = Tk()

#design
root.geometry("800x600")
root.title("Tambarduine IDE")


main_path = ''
errors_names = []


def comp_run():
    global errors_names
    
    
    
    for i in errors_names:
        print("erasing error: "+i)
        text_lineNum.tag_delete(i)
    
    #errorFound([1,10,25])
    error_list = []
    if not errorFound(error_list):
        
        #text_output.configure(state='normal')
        #text_output.delete('1.0', END)
        #text_output.insert('1.0',"Hey! You ran and compiled the code :)")
        #text_output.configure(state='disabled')

        with open('temp.pl0', 'w') as file:
            code = text_info.get('1.0', END)
            file.write(code)
        
        run()

        if len(errorList) > 0:
            errorList.reverse()
            for i in errorList:
                text_output.configure(state='normal')
                text_output.insert('1.0', i[0])
                text_output.insert('1.0', "\n")
                text_output.configure(state='disabled')
        else:
            printList.reverse()

            for i in printList:
                text_output.configure(state='normal')
                text_output.insert('1.0', i)
                text_output.insert('1.0', "\n")
                text_output.configure(state='disabled')

    else:
        text_output.configure(state='normal')
        text_output.delete('1.0', END)
        text_output.insert('1.0',"Errors found")
        text_output.configure(state='disabled')


    
def comp():
    global errors_names
    #global main_path
    #if main_path == '':
    #    save_warning = Toplevel()
    #    notice = Label(save_warning, text="Please save the file first")
    #    notice.pack()
    #    return

    for i in errors_names:
        text_lineNum.tag_delete(i)

    error_list = [0,7,12, 25 ,45]
    if not errorFound(error_list):
        text_output.configure(state='normal')
        text_output.delete('1.0', END)
        text_output.insert('1.0',"Woah buddy, you've just compiled your code!")
        text_output.configure(state='disabled')
    else:
        text_output.configure(state='normal')
        text_output.delete('1.0', END)
        text_output.insert('1.0',"Errors found")
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


def multipleview(*args):
    text_info.yview(*args)
    text_lineNum.yview(*args)
    print(*args)



def on_mousewheel(event):
    return 'break'



canvas = Canvas(root)
canvas.pack(fill = X)

text_scroll = Scrollbar(canvas)
text_scroll.pack(side=RIGHT, fill = BOTH)


text_info = Text(canvas, yscrollcommand = text_scroll.set, wrap="none")
text_info.config(bg='#362f2e', fg='#d2ded1', insertbackground='white')
text_info.pack(fill=BOTH, side = RIGHT, expand= True)
text_info.bind('<MouseWheel>', on_mousewheel)


text_lineNum = Text(canvas, width=2, yscrollcommand = text_scroll.set, wrap="none")
text_lineNum.config(bg='#362f2e', fg='#d2ded1', insertbackground='white')
text_lineNum.pack(fill=BOTH, side = LEFT)
text_lineNum.bind('<MouseWheel>', on_mousewheel)


text_scroll.config(command=multipleview)

scrollbarErrors = Scrollbar(root)
scrollbarErrors.pack( side = RIGHT, fill = Y)


text_output = Text(root, yscrollcommand = scrollbarErrors.set, height=7)
text_output.config(bg='#362f2e', fg='#1dd604')
text_output.configure(state='disabled')
text_output.pack(fill=BOTH, expand= True)


scrollbarErrors.config(command = text_output.yview )


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

    
line_num = "1"

def line_jump_checker():
    current_lines = 1;
    current_text = ""
    line_num = "1"
    update_lineNums(line_num)
    while True:
        if len(current_text) < len(text_info.get('1.0', 'end-1c')):
            current_text_temp = text_info.get('1.0', 'end-1c')
            char_diff = current_text_temp[len(current_text_temp)-1]
            for i in range(len(current_text)):
                if current_text[i] != current_text_temp[i]:
                    char_diff = current_text_temp[i]
                    break

            current_text = current_text_temp
            if char_diff == '\n':
                print("nueva linea")
                current_lines += 1
                line_num += "\n"+str(current_lines)
                update_lineNums(line_num)
            text_lineNum.yview(END)
            text_info.yview(END)
                
        elif len(current_text) > len(text_info.get('1.0', 'end-1c')):
            current_text_temp = text_info.get('1.0', 'end-1c');
            char_diff = current_text[len(current_text)-1]
            for i in range(len(current_text_temp)):
                if current_text[i] != current_text_temp[i]:
                    char_diff = current_text[i]
                    break
                
            current_text = current_text_temp
            if char_diff == '\n':
                current_lines -= 1
                line_num = line_num[0:len(line_num)-2]
                update_lineNums(line_num)
            text_lineNum.yview(END)
            text_info.yview(END)

        
        time.sleep(0.001)
    

def update_lineNums(line_num):
    
    text_lineNum.configure(state='normal')
    text_lineNum.delete('1.0', END)
    text_lineNum.insert('1.0', line_num)
    text_lineNum.configure(state='disabled')



def errorFound(lineErrors):
    global errors_names
    current_program = text_info.get('1.0', 'end-1c')
    line_counter = 0
    errors_names =[]
    found = False
    temp = text_lineNum.get('1.0', 'end-1c')
    for j in range(len(current_program)):
        
        if current_program[j] == "\n":
                line_counter += 1
                
        if j in lineErrors:
            
            text_lineNum.tag_add("E"+str(line_counter+1), str(line_counter+1)+".0", str(line_counter+1)+".5")
            text_lineNum.tag_config("E"+str(line_counter+1), background= "red", foreground= "white")
            errors_names += ["E"+str(line_counter+1)]
            found = True

    return found
                
            
                
    print(errors_names)




line_thread = threading.Thread(target=line_jump_checker)
line_thread.start()



root.config(menu=menu_bar)
root.resizable(False,False)
root.mainloop()

