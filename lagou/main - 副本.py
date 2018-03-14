#!/usr/bin/env python
# encoding: utf-8

import requests
import random
import json
from bs4 import BeautifulSoup
from pymongo import MongoClient
import pprint
import ippool

headers = {
    'Host':
    u'www.lagou.com',
    'User-Agent':
    u'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:u54.0) Gecko/20100101 Firefox/54.0',
    'Accept':
    u'application/json, text/javascript, */*; q=0.01',
    'Accept-Language':
    u'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding':
    u'gzip, deflate, br',
    'Referer':
    u'https:u//www.lagou.com/jobs/list_%E8%A5%BF%E5%AE%89?labelWords=&fromSearch=true&suginput=',
    'Content-Type':
    u'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With':
    u'XMLHttpRequest',
    'X-Anit-Forge-Token':
    u'None',
    'X-Anit-Forge-Code':
    u'0',
    'Content-Length':
    u'19',
    'Cookie':
    u'JSESSIONID=ABAAABAAAIAACBI54403B875C4101733BE49B9167420FC5; user_trace_token=20170725095533-0e2515f491f0475a834b8082dc9e6d72; _ga=GA1.2.492542911.1500947733; _gid=GA1.2.359578653.1500947733; LGRID=20170725150614-bf6d8cff-7107-11e7-b67d-5254005c3644; LGUID=20170725095533-589e2a8d-70dc-11e7-b534-525400f775ce; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1500948816,1500948887,1500964278,1500964281; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1500966374; index_location_city=%E5%85%A8%E5%9B%BD; TG-TRACK-CODE=index_search; SEARCH_ID=6988992079e148718256b0cd49941534; X_HTTP_TOKEN=c8b09df4706ba5e70a426e3bbd13cb1f; _putrc=""; login=false; unick=""; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; LGSID=20170725143118-de2c5446-7102-11e7-b82d-525400f775ce',
    'Connection':
    u'keep-alive'
}

companyHeader = {
    'Host':
    u'www.lagou.com',
    'User-Agent':
    u'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Accept':
    u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language':
    u'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding':
    u'gzip, deflate, br',
    'Referer':
    u'https://www.lagou.com/jobs/3395746.html',
    'Cookie':
    u'JSESSIONID=ABAAABAAAIAACBI54403B875C4101733BE49B9167420FC5; user_trace_token=20170725095533-0e2515f491f0475a834b8082dc9e6d72; _ga=GA1.2.492542911.1500947733; _gid=GA1.2.359578653.1500947733; LGRID=20170725160058-6485decc-710f-11e7-b697-5254005c3644; LGUID=20170725095533-589e2a8d-70dc-11e7-b534-525400f775ce; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1500948816,1500948887,1500964278,1500964281; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1500969658; index_location_city=%E5%85%A8%E5%9B%BD; TG-TRACK-CODE=search_code; SEARCH_ID=288d254bd789415385c0deff0d46980e; X_HTTP_TOKEN=c8b09df4706ba5e70a426e3bbd13cb1f; _putrc=""; login=false; unick=""; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; LGSID=20170725143118-de2c5446-7102-11e7-b82d-525400f775ce; _gat=1',
    'Connection':
    u'keep-alive',
    'Upgrade-Insecure-Requests':
    u'1',
    'Cache-Control':
    u'max-age=0'
}


class jobSpider:
    def __init__(self):

        self.postData = {
            'needAddtionalResult': 'false',
            'pn': 1,  # 'pn'表示第几页
            'city': '西安',
            'first': 'true',
            'kd': ''
        }

        self.siteurl = 'https://www.lagou.com/jobs/positionAjax.json'

    def getPage(self):

        url = self.siteurl

        #time.sleep(20)

        source_code = requests.post(url, headers=headers, data=self.postData)

        plain_text = source_code.text

        jdict = json.loads(plain_text)

        jdata = jdict['content']['positionResult']['result']

        if jdata == []:

            print('--------->已经到达最后一页<---------')
            os._exit(0)

        for each in jdata:
            position_info = {}
            try:
                position_info['positionId'] = each['positionId']

                if collection.find_one({
                        'positionId':
                        position_info['positionId']
                }):
                    continue
                else:
                    position_info['positionId'] = each['positionId']
                    position_info['companyID'] = each['companyId']
                    position_info['positionName'] = each['positionName']
                    position_info['workYear'] = each['workYear']
                    position_info['education'] = each['education']
                    position_info['jobNature'] = each['jobNature']
                    position_info['createTime'] = each['createTime']
                    position_info['salary'] = each['salary']
                    position_info['industryField'] = each['industryField']
                    position_info['financeStage'] = each['financeStage']
                    position_info['companySize'] = each['companySize']
                    position_info['companyFullName'] = each['companyFullName']
                    position_info['firstType'] = each['firstType']
                    position_info['secondType'] = each['secondType']
                    position_info['district'] = each['district']
                    #time.sleep(5)
                    #position_info['job_bt'] = self.getjobinfo(position_info['positionId'])
                    #writeIntoFile('job_bt', job_bt)
                    #time.sleep(5)
                    #datainfo = self.getCompany(companyID)
                    insert_id = collection.insert_one(position_info)
                    print('%s --> %s --> %s 写入完成' %
                          (position_info['companyFullName'],
                           position_info['positionName'],
                           insert_id.inserted_id))
            except KeyError:
                continue

            #companyList.append(tuple((companyID, positionName, workYear, education, jobNature, positionId,
            #                          createTime, salary, industryField, financeStage, companySize, companyFullName,
            #                          firstType, secondType, district, addrInfo,datainfo)))
        print('--->第 ' + str(self.postData['pn']) + ' 页读取完毕\n')

        #writeCSVFile('dataset', companyList)

        return

    def getjobinfo(self, positionID):

        url = 'https://www.lagou.com/jobs/' + str(positionID) + '.html'

        source_code = requests.get(url, headers=companyHeader)

        plain_text = source_code.text

        soup = BeautifulSoup(plain_text, "html.parser")
        #
        #work_addr = soup.find('div', {'class':'work_addr'})
        #
        #addrInfo = []
        #
        #for evera in work_addr.find_all('a', {'rel': 'nofollow'}):
        #    if evera.get_text().strip() != '查看地图':
        #        addrInfo.append(evera.get_text().strip())
        #        addrInfo.append('|')
        #    else:
        #        continue

        job_bt = soup.find('dd', {'class': 'job_bt'}).get_text().strip()

        return job_bt

    def getCompany(self, companyID):

        url = 'https://www.lagou.com/gongsi/' + str(companyID) + '.html'

        source_code = requests.get(url, headers=companyHeader)

        plain_text = source_code.text

        soup = BeautifulSoup(plain_text, "html.parser")

        companyData = soup.find('div', {'class': 'company_data'})

        dataInfo = []

        for ever in companyData.find_all('strong'):
            dataInfo.append(ever.get_text().strip())
            dataInfo.append('|')

        return dataInfo

client = MongoClient('mongodb://127.0.0.1/lagou')
db = client.lagou
collection = db.dataset

#proxy_list = ippool.get_proxies()
#proxy = random.choice(proxy_list)

lagou = jobSpider()
n = 1
while 1:
    print('正在读取第 ' + str(lagou.postData['pn']) + ' 页的公司')
    n += 1
    lagou.getPage()
    #time.sleep(10)
    lagou.postData['pn'] = n

# lagou.getCompany(companyList[3])
