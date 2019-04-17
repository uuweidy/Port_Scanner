# -*- coding: utf-8 -*-
"""
Created on 2019/3/19 16:46
生成程序的图形界面
"""
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import datetime
import time
import portscanner
import dbconnect
import threading
import win_set


method = [
    ("对单端口扫描", 1),
    ("对指定端口段扫描", 2),
    ("对默认端口进行扫描", 3),
    ("对全端口进行扫描(耗时较长)", 4)
]       # 包含四种扫描方法的列表


class Gui(object):
    def __init__(self):         # 生成GUI
        self.ps = portscanner.Portscanner()
        self.dbc = dbconnect.DBConnecter()

        self.root = tkinter.Tk()     # 生成主窗口，设定标题和窗口大小为不可变（防止出现奇怪的东西）
        self.root.title("端口扫描器")
        self.root.resizable(False, False)
        win_set.center_window(self.root, 400, 320)

        self.input_frame = Frame(self.root).pack(side=LEFT)  # 将窗口分为左右两边
        self.output_frame = Frame(self.root)
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

        self.check_button = tkinter.Button(self.root, text='确认', command=self.click_button).pack()
        self.frame3 = Frame(self.root, padx=5, pady=5)
        self.frame3.pack()
        self.ifout = IntVar()
        self.cb = Checkbutton(self.frame3, text='导入到数据库', variable=self.ifout, padx=5, pady=5)
        self.cb.pack()

        # 以下为生成输出栏的代码
        self.output = StringVar()
        self.label2 = Label(self.output_frame, text='扫描结果:             ', padx=15).pack()
        self.listbox = Listbox(self.output_frame, listvariable=self.output, height=14, width=15)
        self.listbox.pack()
        # TODO: 版本号需要修改
        self.info = Label(self.output_frame, text='version:2.2.4    制作者:杜雨威', padx=5, pady=5)
        self.info.pack(side=BOTTOM)

        # 对窗口中的默认参数进行设置
        self.init_args()

        # 进入循环
        self.root.mainloop()

    def init_args(self):        # 对窗口中的默认参数进行设置
        self.ip.set('127.0.0.1')
        self.startportnum.set('0')
        self.endportnum.set('0')
        self.v.set(3)
        self.change_method()
        self.ifout.set(0)

    def change_method(self):  # 变换方法时界面做出的响应
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

    def init_schedule(self):
        global pb
        root = Tk()
        win_set.center_window(root, 200, 20)
        pb = root
        root.title("进度条")
        p = ttk.Progressbar(root, length=200, mode="indeterminate", orient=HORIZONTAL)
        p.grid(row=1, column=1)
        p["maximum"] = 100
        p["value"] = 0
        p.start(10)
        root.mainloop()

    def click_button(self):     # 点击确定按钮时执行的程序
        global pb
        # 将参数传入scannner中并扫描
        self.ps.ip = self.ip.get()
        self.ps.start_port = int(self.startportnum.get())
        self.ps.end_port = int(self.endportnum.get())
        self.ps.method = self.v.get()
        start_time = time.time()
        # self.init_schedule()
        t = threading.Thread(target=self.init_schedule)
        t.start()
        self.ps.port_scan()
        pb.quit()
        end_time = time.time()
        ans = ['共'+str(len(self.ps.ans))+'个结果'] + self.ps.ans
        print(ans)
        # print(self.ps.ans)
        self.output.set(ans)
        t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')   # 生成时间戳
        if self.ifout.get() == 1:
            try:
                b = self.dbc.create_table()
                if not b:
                    tkinter.messagebox.showinfo(title='提示', message='未搜索到名为results的表格，已为您创建。')
                self.dbc.db_insert(self.ps.ip, self.ps.ans, t)         # 导入数据库
            except Exception as e:
                tkinter.messagebox.showerror(title='错误', message=e)
        tkinter.messagebox.showinfo(title='信息', message='搜索结束！耗时{0:.2f}秒'.format(end_time-start_time))    # 提示搜索结束


if __name__ == "__main__":
    app = Gui()
