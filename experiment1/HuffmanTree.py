# coding=utf-8
from PIL import Image, ImageTk
import pygraphviz as pgv
import tkinter as tk
import tkinter.messagebox
 
Index = 0
 
 
#  二叉树
class BTree_Node:
    # 再来个x和y坐标，在确定孩子的时候同时给定位，x左孩子=x父-50,之类的。然后canvas根据横纵坐标连线，但是可能会出现重叠，没办法自适应宽度
    # 根据每一层的节点数量确定坐标的变化量吗？
    lchild = None
    rchild = None
    code = ''
    weight = 0
    index = 0
 
    def __init__(self, weight, index):
        self.weight = weight
        self.index = index
        return
 
    def getchild(self, lc, rc):
        self.lchild = lc
        self.rchild = rc
        return
 
 
#  其中bt是哈夫曼树的根结点，dot = pgv.AGraph(directed=False, strict=True)
def node_edge(bt, dot, sig="", parent_code=""):
    if bt is None:
        return
    # 传入根节点的索引、权值,下面递归把所有点都加进去
    if bt.lchild is None:
        if sig == 'l':
            bt.code = parent_code + '0'
        elif sig == 'r':
            bt.code = parent_code + '1'
        dot.add_node(bt.index, label=str(bt.weight), xlabel=bt.code, color='green', style='filled')
    else:  # 添加分支节点
        if sig == 'l':
            bt.code = parent_code + '0'
        elif sig == 'r':
            bt.code = parent_code + '1'
        dot.add_node(bt.index, label=str(bt.weight), color='grey', style='filled')
 
    node_edge(bt.lchild, dot, "l", bt.code)  # 递归调用，先把左孩子都dot.add_node进去。再把从头开始的右孩子add进去
    node_edge(bt.rchild, dot, "r", bt.code)
 
    # 得先添加完左右孩子，才能把它和左右孩子连起来。所以把连线部分放在添加点的后面
    # 添加边，把父亲和左孩子连起来。没有while循环，他是怎么全部连起来的？
    # 答案：因为这个函数是被递归调用的，所以每个结点都会去跟它的孩子连起来。
    if bt.lchild is not None:
        dot.add_edge(bt.index, bt.lchild.index, label="0", color="green", fontcolor="red")
    if bt.rchild is not None:
        dot.add_edge(bt.index, bt.rchild.index, label="1", color="green", fontcolor="red")
    return
 
 
def Node_InList(hl_weight):  # H_N_L=['13', '54', '7', '43']
    global Index
    ht = []
    for x in range(len(hl_weight)):
        ht.append(BTree_Node(int(hl_weight[x]), Index))  # 往列表里传一个个二叉树结点，初始化权值和索引
        Index += 1
    return ht
 
 
#  对数据进行连接形成二叉树。传入的是装有一个个二叉树结点【对象】的列表H_N_L，每个结点有有权值和编号。想想他是如何处理2 3 4 5这种输入的
def TransFromHuffTree(H_N_L):
    global Index
    # while循环出来之后，结点之间的父子关系都指定了，H_N_L中只剩下一个结点，就是最上面那个
    if len(H_N_L) == 0:
        print("未输入数值")
        return
    while len(H_N_L) > 1:
        H_N_L = sorted(H_N_L, key=lambda x: x.weight)  # 按照每个结点的weight排序，从小到大
        hf = BTree_Node(H_N_L[0].weight + H_N_L[1].weight, Index)  # 最小的两个加成一个结点，这个时候的index应该是最大的
        Index += 1
        hf.getchild(H_N_L[0], H_N_L[1])  # 指定孩子
        # 最小的两个结点移出List，合成的那个进去
        H_N_L.pop(0)
        H_N_L.pop(0)
        H_N_L.append(hf)
 
    return H_N_L[0]  # 返回哈夫曼树最上面那个结点
 
 
def resize(w, h, w_box, h_box, pil_image):
    """
    resize a pil_image object so it will fit into
    a box of size w_box times h_box, but retain aspect ratio
    对一个pil_image对象进行缩放，让它在一个矩形框内，还能保持比例
    """
    f1 = 1.0 * w_box / w  # 1.0 forces float division in Python2
    f2 = 1.0 * h_box / h
    factor = min([f1, f2])
    # use best down-sizing filter
    width = int(w * factor)
    height = int(h * factor)
    return pil_image.resize((width, height), Image.LANCZOS)
 
 
def show():
    # 期望图像显示的大小
    w_box = 500
    h_box = 600
 
    # 以一个PIL图像对象打开
    pil_image = Image.open("c.png")
 
    # 获取图像的原始大小
    w, h = pil_image.size
 
    # 缩放图像让它保持比例，同时限制在一个矩形框范围内
    pil_image_resized = resize(w, h, w_box, h_box, pil_image)
 
    # 把PIL图像对象转变为Tkinter的PhotoImage对象
    tk_image = ImageTk.PhotoImage(pil_image_resized)
 
    # 新建图片Label
    label = tk.Label(root)
    label.image = tk_image
    label.configure(image=tk_image)
    label.place(x=400, y=0)
 
 
def GetValue():
    global values, HuffTreelist, v2,v1
    num=0
    values = v2.get()
    values = values.split()  # 获取用户输入的数的列表values
    if not v1.get():
        tkinter.messagebox.showwarning('huffman', '总数为空，请输入总数')
        return
    else:
        if v1.get().isnumeric():
            num=int(v1.get())
        else:
            tkinter.messagebox.showwarning('huffman', '总数输入有误，请重新输入')
            return
    if values:
        flag=True
        if(len(values)!=num):
            tkinter.messagebox.showwarning('huffman','输入的权值与总数不相符，请重新输入')
            flag=False
        else:    
            for x in range(len(values)):
                if not values[x].isnumeric():
                    tkinter.messagebox.showwarning('huffman', '权值输入有误，请重新输入')
                    flag = False
                    break
        if flag:
            tkinter.messagebox.showwarning('huffman', '输入权值成功')
    else:
        tkinter.messagebox.showwarning('huffman', '权值为空，请输入权值')
    return
 
 
def birth():
    global values, HuffTreelist, v2
    # 把用户输入的values=['13', '54', '7', '43']传入，返回装有一个个二叉树结点【对象】的列表，每个结点有有权值和编号
    HuffTreelist = Node_InList(values)
    HuffTree = TransFromHuffTree(HuffTreelist)  # 得到哈夫曼树最上面的那个结点，此时所有结点之间的父子关系都有了
    
    dot = pgv.AGraph(directed=False, strict=True)  # AGraph是个类，这是创建类的对象，构造函数。  PyGraphviz (几何图形可视化工具)
    # directed:指定要不要画出有向线;
    # ranksep:指定连线长度,int类型
    # landscape="true":变成横向的树
    #stirct:指定图的严格性质，True：图不能存在回路和平行边
    node_edge(HuffTree, dot)  # 把结点塞到dot里面，并且连线
    dot.layout('dot')  # 还有其他的参数，画出来就不是个二叉树形态
    dot.draw('c.png')
    show()
 
 
if __name__ == "__main__":
    root = tk.Tk()  # 创建窗口
    root.title("Huffman算法实现最优树")
    # 画竖线
    canvas = tk.Canvas(root, height=1000)  # 画布的大小还得自定义。。。初始值大概是200
    canvas.create_line(90, 0, 90, 2000, fill='black')
    canvas.place(x=290, y=0)
    root.geometry("900x600")  # 第一个是宽，第二个是高
    # 图片
    tk_image = ImageTk.PhotoImage(file="tree.png")
    title_image = tk.Label(root, image=tk_image, width=350, height=240)
    title_image.place(x=10, y=20)
 
    values = ""
 
    # 输入部分
    l1 = tk.Label(root, text='输入总数 :', font=('Times', 13)).place(x=10, y=280)
    l2 = tk.Label(root, text='输入权值 :', font=('Times', 13)).place(x=10, y=380)
    v1 = tk.StringVar()
    v2 = tk.StringVar()
    e1 = tk.Entry(root, textvariable=v1)  # 就是input框 ，输入n
    e1.grid(row=0, column=1, padx=10, pady=5)
    e1.place(x=110, y=280)
    e2 = tk.Entry(root, textvariable=v2)  # 就是input框 ，输入权
    e2.grid(row=1, column=1, padx=10, pady=5)
    e2.place(x=110, y=380)
 
    # 按钮部分
    b1 = tk.Button(root, text='确认', width=10, command=GetValue)
    b1.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
    b1.place(x=40, y=450)
    b2 = tk.Button(root, text='退出', width=10, command=root.quit)
    b2.grid(row=2, column=1, sticky=tk.E, padx=10, pady=5)
    b2.place(x=220, y=450)
    b3 = tk.Button(root, text='生成哈夫曼树', width=10, command=birth)
    b3.grid(row=2, column=2, sticky=tk.E, padx=10, pady=5)
    b3.place(x=280, y=330)
 
    tk.mainloop()  # 让窗口一直保持运行，下面的代码被暂停。当窗口退出后，开始建树、画图
    root.destroy()