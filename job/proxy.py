import requests
import random
from bs4 import BeautifulSoup
import re
import pprint
import constant
from getPage import GetPage
import tqdm

https_url = 'http://www.xicidaili.com/wn'
http_url = 'http://www.xicidaili.com/wt'


class GetProxy:
    def __init__(self, target_url='http://51job.com/', target_title=None):
        self.user_agent = constant.User_Agent

        self.target_url = target_url

        self.target_title = target_title

        # self.verification = GetPage()

        return

    def verification(self, url, proxy):
        source_code = requests.get(
            url,
            headers=self.user_agent[-1],
            proxies=proxy,
            timeout=10)
        status_code = source_code.status_code
        source_code.encoding = 'gbk'
        source_code.content.decode('gbk', 'replace').encode('utf-8', 'replace')
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, 'html.parser')

        return soup, status_code

    def get_xici(self, proxy_type='https'):
        if proxy_type == 'https':
            url = [https_url]
        elif proxy_type == 'http':
            url = [http_url]
        else:
            url = [https_url, http_url]

        for site in url:
            source_code = requests.get(
                site, headers=random.choice(self.user_agent))
            plain_text = source_code.text
            soup = BeautifulSoup(plain_text, 'html.parser')
            result = self.getDetail(soup, proxy_type)

        return

    def getDetail(self, soup, proxy_type='https'):
        proxy_http = []
        proxy_https = []

        all_proxy = soup.find_all('tr', {'class': 'odd'})

        with tqdm.tqdm(total=len(all_proxy)) as pbar:

            for listItem in all_proxy:
                ip_info = listItem.find_all('td')

                proxy = 'http://' + ip_info[1].get_text(
                ) + ':' + ip_info[2].get_text()

                if proxy_type != 'both':
                    proxies = {proxy_type: proxy}
                else:
                    proxies = {ip_info[5].get_text(): proxy}
                # print(ip_info[5].get_text() + ': ' + proxy + '\t', end='')
                try:
                    r, status_code = self.verification(self.target_url,
                                                       proxies)
                except Exception as e:
                    pbar.update()
                    continue

                # soup = BeautifulSoup(r.text, 'html.parser')

                try:
                    title_tag = r.title.get_text()
                    # print(title_tag)
                except AttributeError:
                    pbar.update()
                    continue

                if status_code == 200 and re.search(
                        re.compile(self.target_title), title_tag):
                    if proxy_type == 'http':
                        proxy_http.append(proxy)
                    elif proxy_type == 'https':
                        proxy_https.append(proxy)
                    elif ip_info[5].get_text() == 'HTTP':
                        proxy_http.append(proxy)
                    else:
                        proxy_https.append(proxy)

                pbar.update()
            pbar.close()

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

        with open(fileName, 'w', errors='ignore', encoding='utf-8') as f:
            for line in fileContent:
                f.write(line)
                f.write('\n')

        f.close()
        return


def getlist():
    proxy = GetProxy(target_title='招聘网_人才网_找工作_求职_上前程无忧')
    proxy.get_xici(proxy_type='http')


if __name__ == '__main__':
    proxy = GetProxy(target_title='招聘网_人才网_找工作_求职_上前程无忧')
    proxy.get_xici(proxy_type='http')
