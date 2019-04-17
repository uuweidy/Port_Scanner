# -*- coding: utf-8 -*-
"""
Created on 2019/3/19 16:05
与数据库进行链接并将查询结果上传到数据库中

"""

import pymysql
import datetime
from config import getConfig


class DBConnecter(object):
    def __init__(self, filename="/dbcfg.txt"):
        self.ini = filename

    def db_insert(self, ip, port, time):
        db = pymysql.connect(getConfig(self.ini, 'database', 'dbhost'), getConfig(self.ini, 'database', 'dbuser'),
                             getConfig(self.ini, 'database', 'dbpassword'), getConfig(self.ini, 'database', 'dbname'))
        # 链接数据库

        cursor = db.cursor()

        for p in port:
            try:
                cursor.execute("INSERT INTO %s(ip,port,scan_time) VALUES(%s,%s,%s)"
                               % ('results', '\'' + ip + '\'', p, '\'' + time + '\''))
                db.commit()  # 更新操作
            except:
                db.rollback()  # 之后应当尝试写入日志文件

        db.close()

    def create_table(self):
        db = pymysql.connect(getConfig(self.ini, 'database', 'dbhost'), getConfig(self.ini, 'database', 'dbuser'),
                             getConfig(self.ini, 'database', 'dbpassword'), getConfig(self.ini, 'database', 'dbname'))
        cursor = db.cursor()
        cursor.execute("SHOW TABLES")
        db.commit()
        res = cursor.fetchall()  # 查询数据库中的所有表格
        print(res)
        controler = False
        for tables in res:  # 判断数据库中是否已经有这个表了
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
    c = DBConnecter()
    c.create_table()
    c.db_insert('127.0.0.1', [22, 23], datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
