import requests
import random
from bs4 import BeautifulSoup
import re
import pprint
import constant
from getPage import GetPage

https_url = 'http://www.xicidaili.com/wn/'
http_url = 'http://www.xicidaili.com/wt/'


class GetProxy:
    def __init__(self, target_url='http://www.baidu.com', target_title=None):
        self.user_agent = constant.User_Agent

        self.target_url = target_url

        self.target_title = target_title

        self.verification = GetPage()

        return

    def get_xici(self, proxy_type='https'):
        if proxy_type == 'https':
            url = [https_url]
        elif proxy_type == 'http':
            url = [http_url]
        else:
            url = [https_url, http_url]

        for site in url:
            source_code = requests.get(url, headers=random.choice(headers))
            plain_text = source_code.text
            soup = BeautifulSoup(plain_text, 'html.parser')
            result = self.getDetail(soup, proxy_type)

        return

    def getDetail(self, soup, proxy_type='https'):
        proxy_http = []
        proxy_https = []

        for listItem in soup.find_all('tr', {'class': 'odd'}):
            ip_info = listItem.find_all('td')

            proxy = 'http://' + ip_info[1].get_text(
            ) + ':' + ip_info[2].get_text()

            if proxy_type != 'both':
                proxies = {proxy_type: proxy}
            else:
                proxies = {ip_info[5].get_text(): proxy}
            print(ip_info[5].get_text() + ': ' + proxy + '\t', end='')
            try:
                r = self.verification.get(self.target_url)
            except Exception as e:
                print('无效')
                continue

            soup = BeautifulSoup(r.text, 'html.parser')

            try:
                title_tag = soup.find('title').string
            except AttributeError:
                print('无效')
                continue

            if r.status_code == 200 and re.search(
                    re.compile(self.target_title), title_tag):
                print('有效')
                if proxy_type == 'http':
                    proxy_http.append(proxy)
                elif proxy_type == 'https':
                    proxy_https.append(proxy)
                elif ip_info[5].get_text() == 'HTTP':
                    proxy_http.append(proxy)
                else:
                    proxy_https.append(proxy)
            else:
                print('无效')

        if len(proxy_http) != 0:
            self.writeIntoFile(proxy_type, proxy_http)

        if len(proxy_https) != 0:
            self.writeIntoFile(proxy_type, proxy_https)

        if proxy_type == 'http':
            print('共获得有效代理 %d 个' % len(proxy_http))
            return proxy_http
        elif proxy_type == 'https':
            print('共获得有效代理 %d 个' % len(proxy_https))
            return proxy_https
        else:
            print('共获得 http 类型代理 %d 个' % len(proxy_http))
            print('共获得 https 类型代理 %d 个' % len(proxy_https))
            return proxy_http, proxy_https

    def writeIntoFile(self, fileName, fileContent):  # 生成文本文件
        fileName += '.txt'

        with open(fileName, 'a+', errors='ignore', encoding='utf-8') as f:
            for line in fileContent:
                f.write(line)
                f.write('\n')

        f.close()
        return
'''
    def get_kxdaili(self):
        proxy_https = []

        print('正在获取开心代理！')
        for n in range(1, 11):
            url = 'http://www.kxdaili.com/dailiip/1/' + str(n) + '.html#ip'
            print(url)
            proxy = {}
            soup = getPageSoup(url)
            tbody = soup.find('tbody')

            for tr in tbody.find_all('tr'):
                content = [x for x in tr.stripped_strings]
                if content[3] == 'HTTPS' or content[3] == 'HTTP,HTTPS':
                    proxy = 'http://' + content[0] + ':' + content[1]
                    proxies = {'https': proxy}
                else:
                    continue

                print('http://' + content[0] + ':' + content[1] + '\t', end='')
                try:
                    r = requests.get(
                        TARGET_URL,
                        headers=random.choice(headers),
                        proxies=proxies,
                        timeout=10)
                except Exception as e:
                    print('无效')
                    continue

                soup = BeautifulSoup(r.text, 'html.parser')

                try:
                    title_tag = soup.find('title').string
                except AttributeError:
                    print('无效')
                    continue

                if r.status_code == 200 and re.search(
                        re.compile('拉勾'), title_tag):
                    print('有效')
                    proxy_https.append(proxy)
                else:
                    print('无效')

        if len(proxy_https) != 0:
            writeIntoFile('https', proxy_https)

        return

    def get_ip181():
        proxy_https = []

        url = 'http://www.ip181.com/'

        print('正在获取ip181代理！')

        proxy = {}
        soup = getPageSoup(url)
        tbody = soup.find('tbody')
        for tr in tbody.find_all('tr'):
            content = [x for x in tr.stripped_strings]
            if content[3] == 'HTTPS' or content[3] == 'HTTP,HTTPS':
                proxy = 'http://' + content[0] + ':' + content[1]
                proxies = {'https': proxy}
            else:
                continue
            print('http://' + content[0] + ':' + content[1] + '\t', end='')
            try:
                r = requests.get(
                    TARGET_URL,
                    headers=random.choice(headers),
                    proxies=proxies,
                    timeout=10)
            except Exception as e:
                print('无效')
                continue

            soup = BeautifulSoup(r.text, 'html.parser')

            try:
                title_tag = soup.find('title').string
            except AttributeError:
                print('无效')
                continue

            if r.status_code == 200 and re.search(re.compile('拉勾'), title_tag):
                print('有效')
                proxy_https.append(proxy)
            else:
                print('无效')

        if len(proxy_https) != 0:
            writeIntoFile('https', proxy_https)

        return
'''
