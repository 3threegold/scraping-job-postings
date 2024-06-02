# 爬取百度百聘信息
# 引入库
import requests
# 导入bs4库解析html网页
from bs4 import BeautifulSoup

# 爬取的网站
url = 'https://yiqifu.baidu.com/g/aqc/joblist?q=python'
# 请求头
h = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}
# 发送请求
res = requests.get(url=url,headers=h)

# find?find_all
soup = BeautifulSoup(res.text,"html.parser")
# 要找的岗位是.job-info的类名  
jobs = soup.find_all(".job-info")
print(jobs)

# bs4前提的爬取网址返回的内容的html源代码