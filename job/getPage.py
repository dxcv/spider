'''
调用requests，获取页面信息
'''

import requests
import random
import constant
from bs4 import BeautifulSoup


class GetPage():
    def __init__(self):
        # 定义请求头，用于获取拉勾信息
        self.header = constant.requests_header

        # 定义浏览器，用于获取IP地址
        self.user_agent = constant.User_Agent

        return

    def get(self, url, proxy=None):
        '''
        通过get方式发送请求，完全调用requests.get，此处是专门用于获取代理ip
        返回soup
        参数：
        url: 要抓取的网页地址
        '''
        header = self.header
        header[
            'Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'

        source_code = requests.get(
            url, headers=random.choice(self.user_agent), proxies=proxy, timeout=15)

        status_code = source_code.status_code
        source_code.encoding = 'gbk'
        source_code.content.decode('gbk', 'replace').encode('utf-8', 'replace')
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, 'html.parser')

        return soup, status_code

    def post(self, url, para):
        source_code = requests.post(url, headers=self.header, data=para)

        plain_text = source_code.text

        return plain_text


def readProxy(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    f.close()

    return [line.strip() for line in lines]

# r = GetPage()
# soup = r.get('https://www.baidu.com/')
# print(soup.prettify())