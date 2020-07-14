from pykeyboard import *
import time
import tkinter as tk
from tkinter import filedialog
import re
import os
#k=PyKeyboard()
#time.sleep(5)
#k.type_string('11111')

def select_file():
    global name
    #default_dir=r"文件路径"
    #file_path = tk.filedialog.askopenfilename(title=u'选择文件', initialdir=(os.path.expanduser(default_dir)))
    name =filedialog.askopenfilename(filetypes=[("文本",".txt"),("python",".py")])
    f=open(name)
    var.set(name)


def handle(command):
    sign=False#表示是否延迟10秒按回车
    length=len(command)
    end_length=length
    if length>=2:
        if command[length-2]=='#':
            end_length=end_length-1
            sign=True
    if command[length-1]=='\n':
        end_length=end_length-1
        
        
    for i in range(0,end_length):
        k.type_string(command[i])
    if sign:
        time.sleep(atime[1])
    k.press_key(k.enter_key)
    time.sleep(atime[2])
    
    
        

def start():
    shell=[]
    file=open(name,'r')
    while 1:
        line=file.readline()
        if not line:
            break 
        shell.append(line)
    file.close()
    time.sleep(atime[0])
    for command in shell:
        handle(command)



    
def get_save_file():
    time_list=[]
    if os.path.exists('config.txt'):
        p=open('./config.txt','r')
        time_list.append(int(p.readline()))
        time_list.append(int(p.readline()))
        time_list.append(int(p.readline()))
        p.close()
        #print(str(time_list[0])+"  "+str(time_list[1]))
        return time_list
    else:
        #print('no ok')
        p = open("./config.txt",'w')
        p.write('10\n10')
        p.close()
        time_list.append(10)
        time_list.append(10)
        time_list.append(1)
        return time_list
    

def change_time():
    atime[0]=int(input_1.get())
    atime[1]=int(input_2.get())
    atime[2]=int(intput_3.get())
    #print(str(time[0])+'  '+str(time[1]))
    p=open('./config.txt','w')
    p.write(str(atime[0])+'\n')
    p.write(str(atime[1])+'\n')
    p.write(str(atime[2]))
    p.close()

if __name__=="__main__":
    global root

    global var

    global atime

    global k
    k=PyKeyboard()
    
    root=tk.Tk()
    root.title('快速脚本')
    root.geometry('300x400+500+500')
    b = tk.Button(root, text='选择文件', font=('Arial', 12), width=10, height=1, command=select_file)
    go=tk.Button(root,text="运行脚本",font=('Arial',12) ,width=10,height=1,command=start)
    change=tk.Button(root,text="修改时间",font=('Arial',12) ,width=10,height=1,command=change_time)

    
    var = tk.StringVar() 
    l = tk.Label(root,text='文件:',width=5, height=1)
    l1=tk.Label(root, textvariable=var,width=40, height=1)

    time_1 = tk.Label(root,text='等待运行时间:',width=12, height=1)
    input_1 = tk.Entry(root, font=('Arial', 8))

    time_2 = tk.Label(root,text='输入等待时间:',width=12, height=1)
    input_2= tk.Entry(root,font=('Arial', 8))

    time_3 = tk.Label(root,text='命令间隔:',width=12, height=1)
    input_3= tk.Entry(root,font=('Arial', 8))
    l.place(x=14,y=10)
    l1.place(x=5,y=30)
    b.place(x=100,y=100)
    go.place(x=100,y=150)
    change.place(x=100,y=200)
    time_1.place(x=10,y=230)
    time_2.place(x=10,y=280)
    time_3.place(x=5,y=330)
    
    input_1.place(x=70,y=250)
    input_2.place(x=70,y=300)
    input_3.place(x=70,y=350)



    atime=get_save_file()
    input_1.insert('end',str(atime[0]))
    input_2.insert('end',str(atime[1]))
    input_3.insert('end',str(atime[2]))
   






    
root.mainloop()
