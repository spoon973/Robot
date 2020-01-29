from deploy_database import demandMessage
from deploy_database import storeDatabase
from deploy_database import insertData
from final_data import sendMessage
from final_data import save_final_data

# 程序执行
if __name__ == "__main__":
    # 开始爬取群与学员信息
    demand = demandMessage.demandMessage()
    demand.main()
    # 创建数据库(若群信息未发生变动，数据库保持不变)
    store = storeDatabase.storeDatabase()
    store.main()
    # 备份当前数据并向数据库表中插入最新数据
    insert = insertData.insertData()
    insert.main()
    # 查询加群成员与退群成员在保存文件过程中实现
    # 将从数据库查询出来的最终数据保存至文件
    final = save_final_data.final_data()
    final.main()
    # 给指定的qq发送消息
    send = sendMessage.sendMessage()
    send.main()
