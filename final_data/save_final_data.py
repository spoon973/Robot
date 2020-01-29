# 清空文本文件
import os
from read_data import Configuration

class final_data:
    # 将从数据库查询到的方法保存至txt文件
    def save_data(self,mysql):
        # path = os.path.dirname(os.getcwd())
        with open('./reault_data/information.txt', 'w', encoding="utf-8") as f:
            pass
        # 将查询到的数据保存到txt文件当中
        # print(mysql.store_result)
        for i in mysql.store_result:
            with open('./reault_data/information.txt','a+',encoding="utf-8") as f:
                f.write('{}:{}'.format(i[0],len(i[1:])) + "\n")

    def main(self):
        # 查询加群成员与退群成员
        mysql = Configuration.MysqlPython("tedu")
        mysql.main()
        self.save_data(mysql)

# if __name__ == '__main__':
#     final = final_data()
#     final.main()