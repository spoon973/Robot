import os
import re
import pymysql
import warnings
import numpy as np

class storeDatabase:
    def __init__(self):
        self.db = pymysql.connect("localhost","root","123456",charset="utf8")
        self.cursor = self.db.cursor()

    # 得到爬取群的名称信息
    def read_file(self,qun_list):
        file_list = os.listdir("./data")
        for i in file_list[1:]:
            pattern = re.compile(r'达内.*?群')
            r = pattern.findall(i)
            qun_list.append(r)
        self.convert_data(qun_list)

    # 将得到的数据进行转化
    def convert_data(self,qun_list):
        # 将列表转化为数组
        qun_array = np.array(qun_list)
        #得到群名称
        qun_mes = qun_array[:,0]
        self.writeTomysql(qun_mes)

    # 建立数据库系统
    def writeTomysql(self, qun_mes):
        # 创建数据库
        c_db = "create database if not exists Tedu character set utf8"
        u_db = "use Tedu"
        # 循环创建数据库
        for qun_name in qun_mes:
            c_tab_new = "create table if not exists {}_new(\
                         id int primary key auto_increment,\
                         qun_number varchar(50),\
                         group_name varchar(50),\
                         qq_number bigint,\
                         gender varchar(2),\
                         qq_year varchar(5),\
                         join_time Date,\
                         end_time Date)charset=utf8".format(qun_name)

            c_tab_old = "create table if not exists {}_old(\
                         id int primary key auto_increment,\
                         qun_number varchar(50),\
                         group_name varchar(50),\
                         qq_number bigint,\
                         gender varchar(2),\
                         qq_year varchar(5),\
                         join_time Date,\
                         end_time Date)charset=utf8".format(qun_name)
            # 忽略警告信息
            warnings.filterwarnings("ignore")
            #执行指令
            try:
                self.cursor.execute(c_db)
                self.cursor.execute(u_db)
                self.cursor.execute(c_tab_new)
                self.cursor.execute(c_tab_old)
            except Warning:
                pass
        print("数据库配置成功")

    def main(self):
        self.read_file([])
