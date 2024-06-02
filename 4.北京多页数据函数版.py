# 
# 引入库
import requests
import json
from bs4 import BeautifulSoup
import time
import pandas
# 请求头
h = {
    'Referer':'https://yiqifu.baidu.com/g/aqc/joblist?q=python', #反反爬措施
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}
# 封装三个函数
# 1. 每一页的url地址
# 页码函数的规律：只有page的页码在变化
def get_url():
    url_list = []
    for i in range(1,35):
        u = f'https://yiqifu.baidu.com/g/aqc/joblist/getDataAjax?q=python&page={i}&pagesize=20&district=110000&salaryrange='
        # 上面的每个u就是每页的地址，将他添加到url_list里
        url_list.append(u)
    return url_list

# 2.发送请求的方法
def get_job():
    url_list = get_url()
    jobList = [] #存放所有信息的列表
    # 循环每一页的地址来发送请求
    n = 0
    for i in url_list[:1]:
        n += 1
        print(f"当前爬的是第{n}页")
        res = requests.get(url=i,headers=h)
        data = json.loads(res.text)
        lists = data['data']['list']
        # 此时lists就是每一页的20个岗位
        for L in lists:
             # i就是每个岗位信息，用一个字典来接受
            job = {}
            job['城市'] = L['city']
            job['公司名称'] = L['company']
            job['学历'] = L['edu']
            job['工作经验'] = L['exp']
            job['岗位名称'] = L['jobName']
            job['薪资'] = L['salary']
            # 获取岗位详情
            job['岗位描述'] = get_detail(L["detailUrl"])
            # 每一个job添加到列表里
            jobList.append(job)
    time.sleep(.3)
    return jobList

# 3.封装岗位详情的函数
def get_detail(detail_url):
    detail_text = requests.get(url=detail_url,headers=h)
    # print(detail_text.text)  #岗位职责的内容在scrip标签里面
    # 返回网页源代码，内容在script标签里面  因为网页有多个script，所以用find_all
    soup = BeautifulSoup(detail_text.text,"html.parser")
    scripts = soup.find_all("script")
    # print(scripts) 遍历多个script标签去判定我需要的内容
    for s in scripts:
        if "window.pageData" in s.text:
            text = s.text
            # 这个大字符串很乱，不能直接用json转，需要切片，只保留字典再用json转
            star = text.find('window.pageData = ')+len("window.pageData = ")
            end = text.find(" || {}")
            # 收尾索引切片，保留需要的字符串，转为字典
            details = text[star:end]
            # 用json转为字典
            d = json.loads(details)
    time.sleep(.3)
    return  d['desc']

# get_job()是发请求存数据的函数

datas = get_job()
# 导出表格
df = pandas.DataFrame(datas)
df.to_excel("job.xlsx",index=False)





