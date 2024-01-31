import copy
from tkinter import Label,Tk,Entry,Button,Text,SW,W,WORD,NORMAL,END,DISABLED
import numpy as ny
import time
import tkinter.messagebox
import re

# 匹配非数字字符
def has_non_numeric(string):
    pattern = r'[^0-9\s]'  # 使用 [^0-9\s] 匹配除了数字和空格之外的所有字符
    return bool(re.search(pattern, string))

def warshall_algorithm(matrix):
    result_matrix=copy.deepcopy(matrix)
    n = len(matrix)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                result_matrix[i][j] = result_matrix[i][j] or (result_matrix[i][k] and result_matrix[k][j])

    return result_matrix

#矩阵幂乘运算
def evaluate(matrix):
    new_matrix=ny.array(matrix)
    result_matrix=ny.array(matrix)
    while 1:
        _=ny.logical_or(result_matrix,result_matrix@new_matrix)
        if ny.array_equal(_,result_matrix):
            break
        result_matrix=_
    return ny.ndarray.tolist(ny.where(result_matrix!=0,1,0))

#显示矩阵
def show(t,matrix):#t=t1 OR t2 
    # 在 t 中显示用户输入的矩阵，并将其设置为不可编辑状态
    t.config(state=NORMAL)  # 将 t 的状态设置为可编辑
    t.delete('1.0', END)  # 清空文本框
    # 将矩阵输出成块状
    t.insert(END, "\n".join([" ".join(map(str, row)) for row in matrix]))
    t.config(state=DISABLED)  # 将 t 的状态设置为不可编辑

#确定数据
def confirm_matrix():
    global e1,e2,t1
    # 获取用户输入的矩阵 01001 10000 00001 01001 10010
    matrix_rows = e1.get()
    matrix_data = e2.get()
    #检查输入是否合格
    if not e1.get():
        tkinter.messagebox.showwarning("实验二","请输入矩阵行（列）数！")
        return
    elif not e1.get().isnumeric():
        tkinter.messagebox.showwarning("实验二","请用数字表示行（列）数")
        return
    elif not e2.get():
        tkinter.messagebox.showwarning("实验二","请输入矩阵数据！")
        return
    elif has_non_numeric(e2.get()):
        tkinter.messagebox.showwarning("实验二","矩阵中存在非法字符，请正确输入！")
        return
    # 将用户输入的矩阵数据转换成二维列表
    rows = int(matrix_rows)
    data = matrix_data.split()
    for item in data:
        if(len(item)!=rows):
            tkinter.messagebox.showwarning("实验二","矩阵元素数量有误，请正确输入！")
            return
     
    if rows!=len(data):
        tkinter.messagebox.showwarning("实验二","矩阵大小与行（列）数不符，请重新输入！")
        return
    global matrix
    matrix = [[int(ch) for ch in i if ch=='1'or'0']for i in data]    
    show(t=t1,matrix=matrix)

#传递性
def calculate():
    start=time.perf_counter()
     # 调用 Warshall 算法计算结果
    result_matrix = warshall_algorithm(matrix)
    print("warShell耗时：",time.perf_counter()-start)
    print(result_matrix)
    start=time.perf_counter()
    new_matrix=evaluate(matrix)
    print("闭包幂运算的耗时：",time.perf_counter()-start)
    print(new_matrix)

    if ny.array_equal(result_matrix,matrix):
         l4=Label(root,text="矩阵已经具有传递性了！",bg="#C0C0C0")
         l4.grid(row=4,column=2)
         return
    l4=Label(root,text="传递闭包：",bg="#C0C0C0")
    l4.grid(row=4,column=2)
    show(t=t2,matrix=result_matrix)

#自反性
def reflexivity():
    flag=1
    new_matrix=copy.deepcopy(matrix)
    for i in range(0,int(e1.get())):
        if not matrix[i][i]:
            new_matrix[i][i]=1
            flag=0 
    if flag:
        l4=Label(root,text="矩阵已经具有自反性了！",bg="#C0C0C0")
        l4.grid(row=4,column=2)
        return
    l4=Label(root,text="自反闭包：",bg="#C0C0C0")
    l4.grid(row=4,column=2)
    show(t=t2,matrix=new_matrix)

#对称性
def symmetry():
    for i in range(0,int(e1.get())):
        for j in range(i,int(e1.get())):
            if(matrix[i][j]!=matrix[j][i]):#一旦发现不对称，就进行矩阵的对称化操作
                new_matrix=ny.ndarray.tolist(ny.transpose(matrix)+ny.array(matrix))
                for i in range(0,int(e1.get())):
                    for j in range(0,int(e1.get())):
                        if(new_matrix[i][j]>1):
                            new_matrix[i][j]=1
                l4=Label(root,text="对称闭包：",bg="#C0C0C0")
                l4.grid(row=4,column=2)
                show(t=t2,matrix=new_matrix)
                return
    l4=Label(root,text="矩阵已经具有对称性了！",bg="#C0C0C0")
    l4.grid(row=4,column=2)
 

if __name__=="__main__":
    #主窗口
    root = Tk()
    root.geometry('500x400+500+200')
    root.title("实验二")
    root.resizable(0,0)
    root.config(background="#C0C0C0")
    #标签1
    l1 = Label(root,text="请输入矩阵的行（列）数：",width=20,height=1,padx=14,bg="#C0C0C0")
    l1.grid(row=0,column=0)
    #输入框1
    e1=Entry(root)
    e1.grid(row=0,column=1,sticky="w")
    #标签2
    l2 = Label(root,text="请输入矩阵（以行输入，行与行之间使用空格隔开，矩阵数据使用0和1）：",width=60,height=1,bg="#C0C0C0")
    l2.grid(row=1,column=0,columnspan=30,sticky="w")
    #输入框2
    e2=Entry(root,width=70)
    e2.grid(row=2,column=0,columnspan=30,sticky="w")
    #按钮1
    b1=Button(root,text="确定矩阵",activebackground='#00ff00',width=20,command=confirm_matrix)
    b1.grid(row=3,column=0)
    #按钮2
    b2=Button(root,text="传递性",activebackground='#00ff00',width=5,command=calculate)
    b2.place(anchor=W,x=450,y=82)
    #按钮3
    b3=Button(root,text="自反性",activebackground='#00ff00',width=5,command=reflexivity)
    b3.place(anchor=W,x=310,y=82)
    #按钮4
    b4=Button(root,text="对称性",activebackground='#00ff00',width=5,command=symmetry)
    b4.place(anchor=W,x=380,y=82)
    #标签3
    l3=Label(root,text="请确定你输入的矩阵：",bg="#C0C0C0")
    l3.grid(row=4,column=0)
    #标签4
    global l4
    l4=Label(root,text="提示区",bg="#C0C0C0")
    l4.grid(row=4,column=2)
    #文本框1
    t1=Text(root,width=25,height=20,setgrid=False,wrap=WORD)
    t1.place(anchor=SW,x=10,y=390)
    #文本框2
    global t2
    t2=Text(root,width=25,height=20,setgrid=False,wrap=WORD)
    t2.place(anchor=SW,x=310,y=390)

    root.mainloop()