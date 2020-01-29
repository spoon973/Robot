# 导入需要的包
# 爬取qq群的成员信息
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import json
import csv
import os

class demandMessage:
    # 开始登陆
    def login_spider(self):
        # 设置url
        url = 'https://qun.qq.com/'
        # 构建谷歌驱动器
        browser = webdriver.Chrome()
        # 请求url
        browser.get(url)
        # 模拟登陆，首先找到登陆的id，并点击
        browser.find_element_by_css_selector('#headerInfo p a').click()
        # 点击之后会弹出一个登陆框，这时候我们用显示等待来等待这个登陆框加载出来
        WebDriverWait(browser, 1000).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#loginWin iframe')))
        print('登陆框已加载')
        #提取iframe标签的src属性，访问url
        # 自动登陆
        # 找到iframe标签并获取
        iframe_url = browser.find_element_by_css_selector('#loginWin iframe').get_attribute('src')
        # 访问url
        browser.get(iframe_url)
        # 找到快捷登陆的头像并点击
        # 首先用显示等待这个头像已经加载完成
        WebDriverWait(browser, 1000).until(EC.presence_of_all_elements_located((By.ID, 'qlogin_list')))
        browser.find_element_by_css_selector('#qlogin_list a').click()
        print('登陆成功')
        return browser

    # 切换句柄操作
    def switch_spider(self,browser):
        # 登陆成功之后，找到群管理的标签并点击,等待这个元素加载完成
        WebDriverWait(browser, 1000).until(EC.presence_of_all_elements_located((By.XPATH, './/ul[@id="headerNav"]/li[4]')))
        browser.find_element_by_xpath('.//ul[@id="headerNav"]/li[4]').click()
        # 点击之后，找到成员管理标签并点击
        WebDriverWait(browser, 1000).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'color-tit')))
        browser.find_element_by_class_name('color-tit').click()
        browser.switch_to.window(browser.window_handles[1])
        return browser

    # 开始采集数据
    def start_spider(self,browser):
        # 删除文件夹的文件
        file_list = os.listdir('./data')
        for file_name in file_list:
            os.remove('./data/{}'.format(file_name))
        # 切换句柄之后，我们显示等待窗口出来
        WebDriverWait(browser, 1000).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'my-all-group')))
        # 筛选出我加入的群标签
        lis = browser.find_elements_by_xpath('.//div[@class="my-all-group"]/ul[2]/li')
        mes = len(lis)
        # 遍历
        num = 15
        while num < mes:
            try:
                # 声明一个列表存储字典
                data_list = []
                # 按顺序选择群并获取信息
                # 先点击该群获取成员信息
                lis[num].click()
                # 显示等待信息加载完成
                WebDriverWait(browser, 1000).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'list')))
                # 获取该群当前有多少人，后面翻页需要
                groupMemberNum = eval(browser.find_element_by_id('groupMemberNum').text)
                # 每一次翻页都会刷新21条信息，所以写个循环
                # 这里加1是因为假如一个群有36人，那么count=1，如果循环的话就不会翻页了
                count = groupMemberNum // 21 + 1
                # 每次循环都进行翻页
                while count:
                    count -= 1
                    browser.execute_script('document.documentElement.scrollTop=100000')
                    time.sleep(2)
                time.sleep(3)
                # 获取群号码
                for i in browser.find_elements_by_xpath('.//div[@class="group-tit"]/span'):
                    qun_num = i.text
                # 开始获取成员信息
                trs = browser.find_elements_by_class_name('mb')
                if trs:
                    #自定义id字段值
                    id = 1
                    # 遍历
                    for tr in trs:
                        tds = tr.find_elements_by_tag_name('td')[2:]
                        if len(tds) == 8:
                            # qq网名
                            # qq_name = tds[0].text
                            # 群名称
                            group_name = tds[1].text
                            # qq号
                            qq_number = tds[2].text
                            # 性别
                            gender = tds[3].text
                            # qq年龄
                            qq_year = tds[4].text
                            # 入群时间
                            join_time = tds[5].text
                            # 等级（积分）
                            # level = None
                            # 最后发言时间
                            end_time = tds[6].text

                            # 声明一个字典存储数据
                            data_dict = {}
                            data_dict['id'] = id
                            data_dict['qun_number'] = qun_num
                            # data_dict['qq_name'] = qq_name
                            data_dict['group_name'] = group_name
                            data_dict['qq_number'] = qq_number
                            data_dict['gender'] = gender
                            data_dict['qq_year'] = qq_year
                            data_dict['join_time'] = join_time
                            # data_dict['level'] = level
                            data_dict['end_time'] = end_time
                            id += 1
                            data_list.append(data_dict)

                        elif len(tds) == 9:
                            # qq网名
                            # qq_name = tds[0].text
                            # 群名称
                            group_name = tds[1].text
                            # qq号
                            qq_number = tds[2].text
                            # 性别
                            gender = tds[3].text
                            # qq年龄
                            qq_year = tds[4].text
                            # 入群时间
                            join_time = tds[5].text
                            # 等级（积分）
                            # level = tds[6].text
                            # 最后发言时间
                            end_time = tds[7].text

                            # 声明一个字典存储数据
                            data_dict = {}
                            data_dict['id'] = id
                            data_dict['qun_number'] = qun_num
                            # data_dict['qq_name'] = qq_name
                            data_dict['group_name'] = group_name
                            data_dict['qq_number'] = qq_number
                            data_dict['gender'] = gender
                            data_dict['qq_year'] = qq_year
                            data_dict['join_time'] = join_time
                            # data_dict['level'] = level
                            data_dict['end_time'] = end_time
                            id += 1
                            data_list.append(data_dict)

                browser.find_element_by_id('changeGroup').click()
                time.sleep(3)
                WebDriverWait(browser, 1000).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'ui-dialog')))
                lis = browser.find_elements_by_xpath('.//div[@class="my-all-group"]/ul[2]/li')

                # 将数据写入json文件
                with open('./data/data_json.json', 'w+', encoding='utf-8') as f:
                    json.dump(data_list, f)
                f.close()
                print('json文件写入完成')
                # 这里的编码格式不要写错了，不然会出现乱码，因为群里面的大神名字贼骚
                with open('./data/{}data.csv'.format(qun_num), 'w+', encoding='utf-8-sig', newline='') as f:
                    # 表头
                    title = data_list[0].keys()
                    # 声明writer
                    writer = csv.DictWriter(f, title)
                    # 写入表头
                    writer.writeheader()
                    # 批量写入数据
                    writer.writerows(data_list)
                f.close()
                print('{}csv文件写入完成'.format(qun_num))

                num += 1
            except Exception as e:
                print("代码出现问题，详细信息：",e)

    def main(self):
        browser = self.login_spider()
        browser = self.switch_spider(browser)
        self.start_spider(browser)

# if __name__ == '__main__':
#     demand = demandMessage()
#     demand.main()