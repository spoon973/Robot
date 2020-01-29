import os
import re
import pymysql
import warnings
import pandas as pd

class insertData:
    # 配置数据库
    def __init__(self):
        self.db = pymysql.connect("localhost","root","123456",charset="utf8")
        self.cursor = self.db.cursor()
    # 读取文件信息
    def read_file(self):
        file_list = os.listdir("./data")[1:]
        self.shift_message(file_list)
    # 向旧表写入当前数据
    def shift_message(self,file_list):
        for i in file_list:
            pattern = re.compile(r'达内.*?群')
            r = pattern.findall(i)
            # print(r[0])
            u_db = "use tedu"
            d_odb = "delete from {}_old".format(r[0])
            i_db = "insert into {}_old select * from {}_new".format(r[0],r[0])
            d_ndb = "delete from {}_new".format(r[0])
            # 忽略警告信息
            warnings.filterwarnings("ignore")
            # 执行指令
            try:
                self.cursor.execute(u_db)
                self.cursor.execute(d_odb)
                self.cursor.execute(i_db)
                self.cursor.execute(d_ndb)
            except Warning:
                pass
        self.insert_message(file_list)

    # 定义读取文件并且导入数据库数据sql语句
    def insert_message(self,file_list):
        for i in file_list:
            pattern = re.compile(r'达内.*?群')
            r = pattern.findall(i)
            # 使用pandas 读取csv文件
            df = pd.read_csv('./data/{}'.format(i))
            # 使用for循环遍历df，是利用df.values，但是每条数据都是一个列表
            # 使用counts计数一下，方便查看一共添加了多少条数据
            for each in df.values:
                # 每一条数据都应该单独添加，所以每次添加的时候都要重置一遍sql语句
                sql = 'insert into ' + r[0] + '_new' + ' values('
                # 因为每条数据都是一个列表，所以使用for循环遍历一下依次添加
                for i, n in enumerate(each):
                    # 这个时候需要注意的是前面的数据可以直接前后加引号，最后加逗号，但是最后一条的时候不能添加逗号。
                    # 所以使用if判断一下
                    if i < (len(each) - 1):
                        # 因为其中几条数据为数值型，所以不用添加双引号
                        if i==0 or i == 3:
                            sql = sql + str(n) + ','
                        else:
                            sql = sql + '"' + str(n) + '"' + ','
                    else:
                        sql = sql + '"' + str(n) + '"'
                sql = sql + ');'
                # print(sql)
                # 当添加当前一条数据sql语句完成以后，需要执行并且提交一次
                self.cursor.execute(sql)
                # 提交sql语句执行操作
                self.db.commit()
        self.cursor.close()
        print("数据库数据更新完毕！")
        self.db.close()

    def main(self):
        self.read_file()

# if __name__ == "__main__":
#     insert = insertData()
#     insert.main()