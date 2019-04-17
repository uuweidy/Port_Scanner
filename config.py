# -*- coding: utf-8 -*-
"""
Created on 2019/3/19 15:45
读取当前目录下的配置文件

"""
import configparser
import os
import sys
import tkinter.messagebox


def getConfig(ini, section, key):
    config = configparser.ConfigParser()
    path = os.path.split(os.path.realpath(sys.argv[0]))[0] + ini
    # 其中 os.path.split(os.path.realpath(sys.argv[0]))[0] 得到的是当前文件模块的目录
    config.read(path)               # 读取配置文件
    v = -1
    try:
        v = config.get(section, key)
    except configparser.NoSectionError:
        if len(config.sections()) == 0:
            tkinter.messagebox.showerror(title='错误', message='未找到配置文件，请确保配置文件的位置为:'
                                                             + os.path.split(os.path.realpath(sys.argv[0]))[0] + '!')
        else:
            tkinter.messagebox.showerror(title='错误', message='未找到Section: {}，请修改配置文件'.format(section))
    except configparser.NoOptionError:
        tkinter.messagebox.showerror(title='错误', message='未找到Option: {}，请修改配置文件'.format(key))
    return v


if __name__ == '__main__':
    # 测试代码，输出配置文件中的信息
    ini = '/dbcfg.txt'
    print(getConfig(ini, 'database', 'dbhost'), getConfig(ini, 'database', 'dbuser'),
          getConfig(ini, 'database', 'dbpassword'), getConfig(ini, 'database', 'dbname'))

