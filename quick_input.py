from pykeyboard import *
import time
import tkinter as tk
from tkinter import filedialog
import re
import os
#k=PyKeyboard()
#time.sleep(5)
#k.type_string('11111')
#模拟输入
#version 1.1
#author kengkeng

def handle(command):
    sign=False#表示是否延迟10秒按回车
    length=len(command)
    end_length=length

    if command[length-1]=='\n':
        end_length=end_length-1
        
        
    for i in range(0,end_length):
        k.type_string(command[i])


  
    
    
        

def start():
    shell=[]
    shell.append(txt_input.get())
    time.sleep(atime[0])
    for command in shell:
        handle(command)



    
def get_save_file():
    time_list=[]
    if os.path.exists('config.txt'):
        p=open('./config.txt','r')
        time_list.append(int(p.readline()))
        p.close()
        #print(str(time_list[0])+"  "+str(time_list[1]))
        return time_list
    else:
        #print('no ok')
        p = open("./config.txt",'w')
        p.write('3')
        p.close()
        time_list.append(3)
   
        return time_list
    

def change_time():
    atime[0]=int(input_1.get())

    #print(str(time[0])+'  '+str(time[1]))
    p=open('./config.txt','w')
    p.write(str(atime[0])+'\n')

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
    #b = tk.Button(root, text='选择文件', font=('Arial', 12), width=10, height=1, command=select_file)
    go=tk.Button(root,text="模拟输入",font=('Arial',12) ,width=10,height=1,command=start)
    change=tk.Button(root,text="修改时间",font=('Arial',12) ,width=10,height=1,command=change_time)

    
    var = tk.StringVar() 
    #l = tk.Label(root,text='文件:',width=5, height=1)
    #l1=tk.Label(root, textvariable=var,width=40, height=1)

    time_1 = tk.Label(root,text='等待运行时间:',width=12, height=1)
    input_1 = tk.Entry(root, font=('Arial', 8))

    txt_label = tk.Label(root,text='输入框:',width=12, height=1)
    txt_input = tk.Entry(root,font=('Arial', 18))

    txt_label.place(x=14,y=70)
    txt_input.place(x=18,y=100)
    #l.place(x=14,y=10)
    #l1.place(x=5,y=30)
    #b.place(x=100,y=100)
    go.place(x=100,y=150)
    change.place(x=100,y=200)
    time_1.place(x=10,y=230)

    
    input_1.place(x=70,y=250)



    atime=get_save_file()
    input_1.insert('end',str(atime[0]))






    
root.mainloop()
