# -*- coding: utf-8 -*-
"""
与数据库进行链接并将查询结果上传到数据库中
Created on 2018/10/24 10:44

"""
import pymysql
import datetime
from config import *


def db_insert(ip, port, time):
    db = pymysql.connect(getConfig('database', 'dbhost'), getConfig('database', 'dbuser'),
                         getConfig('database', 'dbpassword'), getConfig('database', 'dbname'))
    # 链接数据库

    cursor = db.cursor()

    for p in port:
        try:
            cursor.execute("INSERT INTO %s(ip,port,scan_time) VALUES(%s,%s,%s)"
                           % ('results', '\'' + ip + '\'', p, '\'' + time + '\''))
            db.commit()                 # 更新操作
        except:
            db.rollback()               # 之后应当尝试写入日志文件

    db.close()


def create_table():
    db = pymysql.connect(getConfig('database', 'dbhost'), getConfig('database', 'dbuser'),
                         getConfig('database', 'dbpassword'), getConfig('database', 'dbname'))
    cursor = db.cursor()
    cursor.execute("SHOW TABLES")
    db.commit()
    res = cursor.fetchall()             # 查询数据库中的所有表格
    print(res)
    controler = False
    for tables in res:                  # 判断数据库中是否已经有这个表了
        if 'results' in tables:
            controler = True
            break
    if not controler:
        cursor.execute("CREATE TABLE results(id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,port INT NOT NULL,"
                       "ip VARCHAR(255) NOT NULL,scan_time TIMESTAMP NOT NULL)")
        db.commit()
        db.close()
    return controler


if __name__ == '__main__':
    # 测试程序，将一条IP地址为本机、端口为22和23的信息放入数据库中
    create_table()
    db_insert('127.0.0.1', [22, 23], datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
