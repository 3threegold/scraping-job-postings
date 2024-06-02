# 引入库
import requests
import json
from bs4 import BeautifulSoup
# 北京招聘数据
url = 'https://yiqifu.baidu.com/g/aqc/joblist/getDataAjax?q=python&page=1&pagesize=20&district=110000&salaryrange='

'https://yiqifu.baidu.com/g/aqc/joblist/getDataAjax?q=python&page=1&pagesize=20&district=110000&salaryrange='
# 请求头
h = {
    'Referer':'https://yiqifu.baidu.com/g/aqc/joblist?q=python', #反反爬措施
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

res = requests.get(url=url,headers=h)
# print(type(res.text)) #字符串还是字典？ json格式的字符串，转为python的字典

# 找到list列表的招聘数据
data = json.loads(res.text)

# 查找list列表
lists = data['data']['list']

# 准备一个空列表获取招聘岗位信息
job_list = []

# 循环爬取的数据
for i in lists[3:5]:
    # i就是每个岗位信息，用一个字典来接受
    job = {}
    job['城市'] = i['city']
    job['公司名称'] = i['company']
    job['学历'] = i['edu']
    job['工作经验'] = i['exp']
    job['岗位名称'] = i['jobName']
    job['薪资'] = i['salary']
    # 还要岗位详情 url地址就在每一个i里面  
    detail_url = i['detailUrl']
    # print(detail_url)
    # 又对详情地址发送请求获得相应内容，拿到岗位详情内容
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
            # print(d['desc'])
            job['岗位描述'] = d['desc']
    # 将每个岗位信息存在列表
    job_list.append(job)
# 上面这些内容还不够，还需要找到每个岗位的详情信息，
# 1.找到岗位详情页的url地址

print(job_list)