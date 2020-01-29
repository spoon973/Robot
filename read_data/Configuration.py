#导入模块
import re
from pymysql import *
from read_data import qun_message

#定义MysqlPython类
class MysqlPython:
    # 初始化一个方法
    def __init__(self,database,host="localhost",user="root",
                 password="123456",port=3306,charset="utf8"):
        self.result = ()
        self.store_result = []
        self.host = host
        self.user =user
        self.password = password
        self.port = port
        self.charset = charset
        self.database = database

    #定义链接数据库的方法
    def open(self):
        self.db = connect(host=self.host,user=self.user,port=self.port,
                          database=self.database,password=self.password,
                          charset=self.charset)
        self.cur = self.db.cursor()

    #定义关闭数据库的方法
    def close(self):
        self.cur.close()
        self.db.close()

    #定义查询数据库内容的方法
    def sql_query(self,sql):
        for i,n in enumerate(sql):
            if i == 0 or i % 2 == 0:
                pattern = re.compile(r'达内.*?群')
                r = pattern.findall(str(n))
                try:
                    self.open()
                    self.cur.execute(str(n))
                    self.result = (r[0]+'add',) + self.cur.fetchall()
                    self.store_result.append(self.result)
                except Exception as e:
                    print("Failed", e)
            else:
                pattern = re.compile(r'达内.*?群')
                r = pattern.findall(str(n))
                try:
                    self.open()
                    self.cur.execute(str(n))
                    self.result = (r[0]+'remove',) + self.cur.fetchall()
                    self.store_result.append(self.result)
                except Exception as e:
                    print("Failed", e)
            self.close()

    def main(self):
        qun = qun_message.qun_message()
        qun.main()
        self.sql_query(qun.sql)
