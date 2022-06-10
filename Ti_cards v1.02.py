import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import *
import webbrowser
import os

def get_scale(event):
    global position
    position=round(scale1.get())
    show_side()
    
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def _hide():
    global df_visible
    global position
    if openBd:
        if df_visible.shape[0] == 0:
            return
        df.at[df_visible.index[position],'hide'] = True
        df_visible = df[df['hide'] != True]
        if position > df_visible.shape[0] - 1:
            position = df_visible.shape[0] - 1
        show_side()

def _open():
#     file type
    filetypes = (
        ('csv files', '*.csv'),
        ('All files', '*.*')
    )
    # show the open file dialog
    f = fd.askopenfilename(filetypes=filetypes)
    global df
    global df_visible
    global openBd
    global position
    # read a csv
    if f:
        df = pd.read_csv(f, sep = ";", encoding='utf-8', index_col=False)
        # adjust column names
        df.columns = df.columns.str.replace('\s+','_').str.lower()
        df = pd.DataFrame(df, columns=['eng', 'rus', 'hide'])
        df = df.astype({'hide': object})
        df_visible = df[df['hide'] != True]
        position_df = df_visible.index[position]
        fm.entryconfigure(2, state = 'normal')
        openBd = True
        show_side()

def _save():
    filetypes = (
        ('csv files', '*.csv'),
        ('All files', '*.*')
    )
    sa = fd.asksaveasfilename(filetypes=filetypes)
    letter = df.to_csv(sa, sep = ";", index = False)
    
def menu_about():
    s = root.geometry()
    s = s.split('+')
    s[0] = s[0].split('x')
    x = str(int(s[1]) + round(int(s[0][0])/2 - 200/2 + 6))
    y = str(int(s[2]) + round(int(s[0][1])/2 - 200/2 + 23))
#     print(s, x, y)
    a = tk.Toplevel(root)
    a.geometry('200x200+{}+{}'.format(x, y))
    a['bg'] = 'green'
    a.overrideredirect(True)    
    img = PhotoImage(file=resource_path('Icon_TiCards_50x50.png'))
    label = Label(a, image=img)
    label.image_ref = img
    label.pack()
    Label(a, bg="green", text="Ti Cards 1.02", font='arial 24').pack(expand=0)
    Label(a, bg="green", text="The easiest way to work with flash cards", font='arial 10', wraplength=180).pack(expand=0)
    Label(a, bg="green", text="(c)Alexander Tiunov, 2022", font='arial 10', wraplength=180).pack(expand=0)
    url = 'https://ko-fi.com/tialex'
    Button(a, bg="red", text="Donate", command=lambda aurl=url:webbrowser.open('https://ko-fi.com/tialex', new=0)).pack(expand=1)
    a.after(5000, lambda: a.destroy())

def update_btn_text():
    global side_face
    side_face = not side_face
    if openBd:
        if (df_visible.shape[0] == 0):
            btn_text.set("Congratulation! You run out of words!")
            return
        if side_face:
            btn_text.set(str(df_visible['eng'][df_visible.index[position]]))
        else:
            btn_text.set(str(df_visible['rus'][df_visible.index[position]]))
    else:
        _open()
    
def add_position():
    global position
    if openBd:
        if (position < df_visible.shape[0] - 1) and (df_visible.shape[0] >0):
            position = position+1
    show_side()
    
def decrement_position():
    global position
    if (position > 0) and (df_visible.shape[0] >0):
        position = position-1
    show_side()
    
def show_side():
    if openBd:
        currentValue = round((df.shape[0] - df_visible.shape[0])/df.shape[0]*100,1)
        count_words.set("Total: " + str(df.shape[0]) + \
        '           Learning: ' + str(df_visible.shape[0])+\
        '           Progress: ' + str(currentValue)\
                       +'%')
        progressbar["value"]=currentValue
        progressbar["maximum"]=100
        scale1.configure(from_=0,to=df_visible.shape[0]-1,value=position, command=get_scale)
        if (df_visible.shape[0] == 0):
            btn_text.set("Congratulation! You run out of words!")
            return
        if side_face:
            btn_text.set(str(df_visible['eng'][df_visible.index[position]]))
        else:
            btn_text.set(str(df_visible['rus'][df_visible.index[position]]))
    else:
        _open()

# Root window
root = tk.Tk()
btn_text = StringVar(value="Open data\n Открыть файл")
count_words = StringVar(value='\(◕‿◕)／')
position=0
side_face = True
openBd = False
root.title('Cards Learner')
root.geometry('600x280')

m = tk.Menu(root)
root.config(menu=m)
fm = tk.Menu(m, tearoff=0)
m.add_cascade(label="File", menu=fm)
fm.add_command(label="Open...", command=_open)
fm.add_command(label="Save...", state= 'disabled', command=_save)
hm = Menu(m, tearoff=0) 
m.add_cascade(label="?", menu=hm)
hm.add_command(label="About", command=menu_about)
label1 = Label(root)
label1.configure(textvariable=count_words)
label1.pack(anchor='w')
progressbar=ttk.Progressbar(root, orient="horizontal",mode="determinate")
progressbar.pack(side=tk.TOP,fill=tk.X)
scale1 = ttk.Scale(root,orient=HORIZONTAL,from_=1,to=1)
scale1.pack(side=BOTTOM, fill=X)
button1 = tk.Button(bg="red", text="<-\nprev", height=50, width=7,command=decrement_position)
button1.pack(side=LEFT)
button3 = tk.Button(bg="red", text="->\nnext", height=50, width=7,command=add_position)
button3.pack(side=RIGHT)

button4 = tk.Button(bg="yellow",text="don't show/ скрыть", command=_hide)
button4.pack(side=BOTTOM, fill=X)

button2 = tk.Button(width=50, height=50, font='arial 23', wraplength=470)
button2.configure(textvariable=btn_text, command=update_btn_text)
button2.pack()

root.bind('<Right>',lambda x: button3.invoke())
root.bind('<Left>',lambda x: button1.invoke())
root.bind('<Up>',lambda x: button2.invoke())
root.bind('<Down>',lambda x: button2.invoke())
root.bind('<space>',lambda x: button4.invoke())

root.iconbitmap(resource_path('favicon.ico'))
root.mainloop()
