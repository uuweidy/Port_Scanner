# -*- coding: utf-8 -*-
"""
生成程序主界面并运行程序
Created on 2018/10/17 18:52

"""

from tkinter import *
import tkinter.messagebox
import portScanner
from dbconnect import *

method = [
    ("对单端口扫描", 1),
    ("对指定端口段扫描", 2),
    ("对默认端口进行扫描", 3),
    ("对全端口进行扫描(耗时较长)", 4)
]       # 包含四种扫描方法的列表


class ScannerGUI(object):

    def __init__(self):         # 生成GUI
        self.scanner = portScanner.Portscanner()

        root = tkinter.Tk()     # 生成主窗口，设定标题和窗口大小为不可变（防止出现奇怪的东西）
        root.title("端口扫描器")
        root.resizable(False, False)

        self.input_frame = Frame(root).pack(side=LEFT)  # 将窗口分为左右两边
        self.output_frame = Frame(root)
        self.output_frame.pack(side=RIGHT)

        # 以下为生成输入栏的代码
        self.frame1 = Frame(self.input_frame, padx=5, pady=15)
        self.frame1.pack(padx=10)
        self.frame2 = Frame(self.input_frame, padx=5)
        self.frame2.pack(side=TOP)
        self.label = Label(self.frame1, text='ip地址:').pack(side=LEFT)
        self.ip = StringVar()
        self.e1 = Entry(self.frame1, textvariable=self.ip, width=20).pack(side=RIGHT)

        self.label1 = Label(self.frame2, text='起始端口号:').pack(side=LEFT)
        self.startportnum = StringVar()
        self.e2 = Entry(self.frame2, textvariable=self.startportnum, width=5)
        self.e2.pack(side=LEFT)
        self.endportnum = StringVar()
        self.e3 = Entry(self.frame2, textvariable=self.endportnum, width=5)
        self.e3.pack(side=RIGHT)
        self.label2 = Label(self.frame2, text='结束端口号:', padx=5).pack(side=RIGHT)

        self.lf = LabelFrame(self.input_frame, text='扫描方法', padx=5, pady=5)
        self.lf.pack(padx=10, pady=10)
        self.v = tkinter.IntVar()
        for i, j in method:
            b = tkinter.Radiobutton(self.lf, text=i, variable=self.v, value=j, command=self.change_method)
            b.pack(anchor='w')

        self.check_button = tkinter.Button(root, text='确认', command=self.click_button).pack()
        self.frame3 = Frame(root, padx=5, pady=5)
        self.frame3.pack()
        self.ifout = IntVar()
        self.cb = Checkbutton(self.frame3, text='导入到数据库', variable=self.ifout, padx=5, pady=5)
        self.cb.pack()

        # 以下为生成输出栏的代码
        self.output = StringVar()
        self.label2 = Label(self.output_frame, text='扫描结果:             ', padx=15).pack()
        self.listbox = Listbox(self.output_frame, listvariable=self.output, height=14, width=15)
        self.listbox.pack()

        self.info = Label(self.output_frame, text='version:2.2.4    制作者:杜雨威', padx=5, pady=5)
        self.info.pack(side=BOTTOM)

        # 对窗口中的默认参数进行设置
        self.init_args()

        # 进入循环
        root.mainloop()

    def init_args(self):        # 对窗口中的默认参数进行设置
        self.ip.set('127.0.0.1')
        self.startportnum.set('0')
        self.endportnum.set('0')
        self.v.set(3)
        self.change_method()
        self.ifout.set(0)

    def click_button(self):     # 点击确定按钮时执行的程序
        # 将参数传入scannner中并扫描
        self.scanner.ip = self.ip.get()
        self.scanner.start_port = int(self.startportnum.get())
        self.scanner.end_port = int(self.endportnum.get())
        self.scanner.method = self.v.get()
        self.scanner.port_scan()
        ans = ['共'+str(len(self.scanner.ans))+'个结果'] + self.scanner.ans
        print(ans)
        print(self.scanner.ans)
        self.output.set(ans)
        t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')   # 生成时间戳
        if self.ifout.get() == 1:
            b = create_table()
            if not b:
                tkinter.messagebox.showinfo(title='提示', message='未搜索到名为results的表格，已为您创建。')
            db_insert(self.scanner.ip, self.scanner.ans, t)         # 导入数据库
        tkinter.messagebox.showinfo(title='信息', message='搜索结束！')    # 提示搜索结束

    def change_method(self):      # 变换方法时界面做出的响应
        selection = int(self.v.get())
        if selection == 1:
            self.e2['state'] = 'normal'
            self.e3['state'] = 'disabled'
        elif selection == 2:
            self.e2['state'] = 'normal'
            self.e3['state'] = 'normal'
        else:
            self.e2['state'] = 'disabled'
            self.e3['state'] = 'disabled'


if __name__ == "__main__":
    # 主程序入口
    app = ScannerGUI()
