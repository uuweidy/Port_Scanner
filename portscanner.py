# -*- coding: utf-8 -*-
"""
Created on 2019/3/19 16:35
扫描某个ip地址的某个端口是否开放

"""
from multiprocessing.pool import ThreadPool
import socket
import time

all_num = 1
complete = 0


class Portscanner(object):
    def __init__(self):             # 初始化对象
        self.ip = ''
        self.start_port = 0
        self.end_port = 0
        self.method = 0
        self.ans = []

    def scan_one_port(self, ip, port):      # 对某个端口进行tcp扫描
        global complete
        complete += 1
        try:
            s = socket.socket()
            s.settimeout(2)
            s.connect((ip, int(port)))      # 与这个端口进行TCP链接，若链接成功则说明端口开放
            self.ans.append(str(port))      # 若端口不开放，则会在 timeout 过后抛出超时异常，
            s.recv(1024)                    # 通过 pass 语句跳过接下来的语句，结束处理。
            s.close()
        except Exception:
            pass

    def port_scan(self):                    # 获取界面中的数据并进行相应的配置
        global all_num
        self.ans = []
        pool = ThreadPool(processes=500)    # 开启500个线程，提高程序运行速率

        if self.method == 1:                # 根据选择的方法确定要扫描的端口
            self.end_port = self.start_port
        elif self.method == 4:
            self.start_port = 1
            self.end_port = 65535

        if self.method == 3:
            default = [80, 8080, 3128, 8081, 9080, 1080, 21, 23, 443, 69, 22, 25, 110, 7001, 9090, 3389, 1521, 1158,
                        2100, 1433]     # 网上找到的常使用的端口号
            all_num = 20
            for port_num in default:
                pool.apply_async(self.scan_one_port, args=(self.ip, port_num))
        else:
            all_num = self.end_port + 1 - self.start_port
            for port_num in range(self.start_port, self.end_port + 1):
                pool.apply_async(self.scan_one_port, args=(self.ip, port_num))

        pool.close()
        pool.join()             # 阻塞主线程


if __name__ == "__main__":
    # 测试程序，扫描本机端口号在20-443内的所有开放端口并输出耗费的时间
    test_ps = Portscanner()
    test_ps.ip = '127.0.0.1'
    test_ps.method = 2
    test_ps.start_port = 20
    test_ps.end_port = 443
    start_time = time.time()
    test_ps.port_scan()
    print("测试ip：", test_ps.ip)
    print("测试端口：", test_ps.start_port, '-', test_ps.end_port)
    print("测试结果：", test_ps.ans)
    print("花费时间：", time.time() - start_time, 's')
