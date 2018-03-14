import os
import re

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

from proxy import getlist

client = MongoClient('mongodb://127.0.0.1')
db = client.job
collection = db.dataset

headers = [{
    'User-Agent':
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0)'
    'Gecko/20100101 Firefox/34.0'
}, {
    'User-Agent':
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6)'
    'Gecko/20091201 Firefox/3.5.6'
}, {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11'
    '(KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'
}, {
    'User-Agent':
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'
}, {
    'User-Agent':
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0)'
    'Gecko/20100101 Firefox/40.0'
}, {
    'User-Agent':
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36\
    (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}]

siteUrl = 'http://search.51job.com/list/200200,000000,0000,00,9,99,%2520,2,1.html'

params = {
    'lang': 'c',
    'postchannel': '0000',
    'workyear': '99',
    'cotype': '99',
    'degreefrom': '99',
    'jobterm': '99',
    'companysize': '99',
    'providesalary': '99',
    'lonlat': '0,0',
    'radius': '-1',
    'ord_field': '0',
    'confirmdate': '9',
    'dibiaoid': '0',
    'specialarea': '00'
}


def readProxy(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    f.close()

    return [line.strip() for line in lines]


def getPageSoup(url, proxy_list, params):
    successful = False

    while not successful:
        try:
            # proxy = {'http': random.choice(readProxy('http.txt'))}
            if len(proxy_list) < 1:
                print('重新获取代理列表')
                getlist()
                proxy_list = readProxy('http.txt')
            proxy = {'http': proxy_list[0], 'https': proxy_list[0]}
            session = requests.Session()
            source_code = session.get(
                url,
                headers=headers[-1],
                proxies=proxy,
                params=params,
                timeout=60)
            source_code.encoding = 'gbk'
            source_code.content.decode('gbk', 'replace').encode(
                'utf-8', 'replace')
            plain_text = source_code.text
            soup = BeautifulSoup(plain_text, 'html.parser')
            successful = True
        except Exception as e:
            print('发生错误，{}'.format(e))
            print('更换代理重试')
            del proxy_list[0]
            # pass

    return soup, proxy_list


def getDetail(soup, proxy_list):
    for i, listItem in enumerate(soup.find_all('div', {'class': 'el'})):
        # time.sleep(3)
        if listItem['class'] != ['el'] or listItem.has_attr('id'):
            continue

        span = listItem.find_all('span')

        area = span[2].get_text(strip=True)
        if area == '异地招聘':
            continue

        pos_url = span[0].a['href']
        if not re.search('(jobs.51job.com)', pos_url):
            continue

        position = span[0].a['title']
        if collection.find_one({'position': position}):
            continue
        pos_info, proxy_list = get_position(pos_url, proxy_list)
        if pos_info == 0:
            continue
        company = span[1].a['title']

        salary = span[3].get_text(strip=True)

        pos_info['company'] = company
        pos_info['url'] = pos_url
        pos_info['salary'] = salary
        pos_info['position'] = position
        collection.insert_one(pos_info)
        print(position)
    return proxy_list


def get_position(url, proxy_list):
    pos_info = {}
    params = None
    soup, proxy_list = getPageSoup(url, proxy_list, params)

    try:
        ltype = soup.find('p', {'class': 'msg ltype'})
        company = ltype.string.split('|')
        company_type = company[0].strip()
        company_size = company[1].strip()
        company_business = company[2].strip()

        jtag = soup.find('div', {'class': 'jtag inbox'})
        workYear = jtag.find_all('span')[0].get_text(strip=True)
        education = jtag.find_all('span')[1].get_text(strip=True)

        job_msg = soup.find('div', {'class': 'bmsg job_msg inbox'})
        job_msg_text = ''
        for text in job_msg.stripped_strings:
            if text == '职能类别：':
                break
            job_msg_text += text.strip()

        response = ''
        for info in job_msg.find_all('p', {'class': 'fp'}):
            text = [text for text in info.stripped_strings]
            if text[0] == '职能类别：':
                for x in text[1:]:
                    response += ('/' + x)

        bmsg = soup.find('div', {'class': 'bmsg inbox'}).p.get_text(strip=True)

        pos_info['workYear'] = workYear
        pos_info['education'] = education
        pos_info['bmsg'] = bmsg
        pos_info['company_type'] = company_type
        pos_info['company_size'] = company_size
        pos_info['company_business'] = company_business
        pos_info['response'] = response
        pos_info['job_msg_text'] = job_msg_text

        return pos_info, proxy_list

    except Exception:
        return 0, proxy_list


def writeIntoFile(fileName, fileContent):  # 生成文本文件
    fileName += '.txt'
    ftxt = open(fileName, 'w', errors='ignore', encoding='utf-8')
    ftxt.write(fileContent)
    ftxt.close()
    return


if __name__ == '__main__':
    next_page = True
    if os.path.exists('http.txt'):
        proxy_list = readProxy('http.txt')
    else:
        print('代理文件不存在，获取代理列表')
        getlist()
        proxy_list = readProxy('http.txt')
    while next_page:
        soup, proxy_list = getPageSoup(siteUrl, proxy_list, params)
        proxy_list = getDetail(soup, proxy_list)
        next_page = False
        try:
            for items in soup.find_all('li', {'class': 'on'}):
                if items.has_attr('onclick'):
                    continue
                else:
                    siteUrl = items.next_sibling.a['href']
                    next_page = True
                    break
        except Exception:
            break
