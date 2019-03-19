# -*- coding: utf-8 -*-
"""
读取与当前文件在同一目录下的配置文件的信息
Created on 2018/10/24 9:33

"""

import configparser
import os
import sys
import tkinter.messagebox


def getConfig(section, key):
    config = configparser.ConfigParser()
    path = os.path.split(os.path.realpath(sys.argv[0]))[0] + '/dbcfg.txt'
    # 其中 os.path.split(os.path.realpath(__file__))[0] 得到的是当前文件模块的目录
    config.read(path)               # 读取配置文件
    try:
        v = config.get(section, key)
    except configparser.NoSectionError:
        tkinter.messagebox.showerror(title='警告', message='未找到配置文件，请确保配置文件的位置为:'
                                                         + os.path.split(os.path.realpath(sys.argv[0]))[0] + '!')
        # 输出错误信息，提示文件路径
    return v


if __name__ == '__main__':
    # 测试代码，输出配置文件中的信息
    # dbname = getConfig('database', 'dbname')
    print(getConfig('database', 'dbhost'), getConfig('database', 'dbuser'),
          getConfig('database', 'dbpassword'), getConfig('database', 'dbname'))
