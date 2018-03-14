# encoding: utf-8

import requests
import random
from bs4 import BeautifulSoup
import os
import re
import json
from math import ceil
import time
import csv

'''
从雪球上获取所有开放型基金的基金代码，转换为晨星对应的代码
'''

class xueqiu:
    def __init__(self):
        self.headers = [
            {'User-Agent':
                 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0)'
                 'Gecko/20100101 Firefox/34.0'},
            {'User-Agent':
                 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6)'
                 'Gecko/20091201 Firefox/3.5.6'},
            {'User-Agent':
                 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11'
                 '(KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
            {'User-Agent':
                 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
            {'User-Agent':
                 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0)'
                 'Gecko/20100101 Firefox/40.0'},
            {'User-Agent':
                 'Mozilla/5.0 (X11; Linux x86_64)'
                 'AppleWebKit/537.36 (KHTML, like Gecko)'
                 'Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'}
        ]
        self.cookies = {}
        self.startPage = 1
        self.postData = {'parent_type': 13,
                         'order': 'asc',
                         'orderBy': 'symbol',
                         'page': self.startPage,
                         'size': 30
                         }
        self.url = 'https://xueqiu.com/fund/quote/list.json'
        self.urlMorningStar = 'http://cn.morningstar.com/handler/fundsearch.ashx'
        self.postMorningStar ={'limit': 15}

        self.writeIntoFile('starID', [('雪球代码', '基金代码', '基金名称', '晨星代码')])

        return

    def getCookies(self):
        self.cookies={}
        url = 'https://xueqiu.com/user/login'
        postData = {'username': 'greatshieh',
                    'areacode': 86,
                    'telephone': 13186187279,
                    'remember_me': 0,
                    'password': 'great182137'}
        sourceCode = requests.post(url, headers=random.choice(self.headers), data=postData)

        for item in sourceCode.cookies:
            self.cookies[item.name] = item.value

        return

    def getPage(self):
        source_code = requests.get(self.url,
                                   headers=random.choice(self.headers),
                                   params=self.postData,
                                   cookies=self.cookies)
        plain_text = source_code.text
        self.jData= json.loads(plain_text)
        return

    def getMorningStarID(self, fundID):
        self.postMorningStar['q']=fundID
        source_code = requests.get(self.urlMorningStar,
                                   headers=random.choice(self.headers),
                                   params=self.postMorningStar)
        plain_text = source_code.text
        self.morningStarData= json.loads(plain_text)
        return

    def analyzeJdata(self):
        self.getCookies()
        self.getPage()
        fundNum = float(self.jData['count'])
        pageNum = ceil(fundNum/self.postData['size'])
        print('共%d支开放式基金, 共%d页'%(fundNum, pageNum))
        for x in range(self.startPage, pageNum+1):
            fileContent = []
            self.postData['page'] = x
            self.getPage()
            print('==========开始读取第%d页=========='%x)
            jStocks = self.jData['stocks']
            for i in range(len(jStocks)):
                symbol = jStocks[i]['symbol']
                fundID = jStocks[i]['code']
                fundName = jStocks[i]['name']
                self.getMorningStarID(fundID)
                try:
                    fundClassId=self.morningStarData[0]['FundClassId']
                except IndexError:
                    time.sleep(1)
                    continue
                print('%s\t%s\t%s\t%s'%(symbol, fundID, fundName, fundClassId))
                fileContent.append(tuple((symbol, fundID, fundName, fundClassId)))

            self.writeIntoFile('starID', fileContent)
        return

    def writeIntoFile(self, fileName, fileContent):  # 写入CSV文件
        fileName += '.csv'
        with open('IDs/'+fileName, 'a+', newline='') as csvfile:
            spamWriter = csv.writer(csvfile)
            for line in fileContent:
                spamWriter.writerow(line)
        return

    def createDir(self, path):  # 生成文件夹
        path = path.strip()
        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists = os.path.exists(path)
        # 判断结果
        if not isExists:
            # 创建目录操作函数
            os.makedirs(path)
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            print(path + '已经创建成功')
            return False

r = xueqiu()
r.analyzeJdata()

