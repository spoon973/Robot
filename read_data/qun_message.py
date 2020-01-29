'''
此文件保存群名称及mysql数据库表的名字
'''
import os
import re
import numpy as np

class qun_message:
    #定义全局变量sql用来保存查询数据库语句
    def __init__(self):
        self.sql = []

    def read_file(self,qun_list):
        # path = os.path.dirname(os.getcwd())
        # print(path)
        file_list = os.listdir("./data")
        for i in file_list[1:]:
            pattern = re.compile(r'达内.*?群')
            r = pattern.findall(i)
            qun_list.append(r)
            qun_array = np.array(qun_list)
            qun_mes = qun_array[:, 0]
        self.query_message(qun_mes)

    def query_message(self,qun_mes):
        for i in qun_mes:
            # 查询加群学员
            sql_add = "SELECT * FROM {}_new WHERE NOT EXISTS (SELECT 1 FROM {}_old WHERE {}_new.qq_number = {}_old.qq_number)".format(i,i,i,i)
            self.sql.append(sql_add)
            # 查询退群学员
            sql_remove = "SELECT * FROM {}_old WHERE NOT EXISTS (SELECT 1 FROM {}_new WHERE {}_new.qq_number = {}_old.qq_number)".format(i,i,i,i)
            self.sql.append(sql_remove)

    def main(self):
        # 得到当前群信息
        self.read_file([])

if __name__ == "__main__":
    qun = qun_message()
    qun.main()