# encoding: utf-8

from bs4 import BeautifulSoup
import csv
import random
import requests
import re

class getAllFund:
# 从晨星获得基金排名，包括业绩汇总和排名
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

        self.fundCategory = {'股票型': 'stock', '激进配置型': 'mix_radical', '灵活配置型': 'mix_flexible',
                             '标准混合型': 'mix_standard', '保守混合型': 'mix_keep',
                             '可转债': 'bond_convertible', '激进债券型': 'bond_radical',
                             '普通债券型': 'bond_general', '纯债基金': 'bond_pure', '短债基金': 'bond_short',
                             '市场基金': 'currency', '市场中性策略': 'market_neutral', '商品': 'commodities',
                             '保本基金': 'keep', '其它': 'other',
                             '指数型': 'index',
                             'ETF': 'etf',
                             'LOF': 'lof'}
        self.postData = {'date': '2017-02-10',
                         'fund': '',
                         'rating': '',
                         'company': '',
                         'cust': '',
                         'sort': 'Return5YearRank',
                         'direction': 'asc',
                         'tabindex': '2',
                         'pageindex': '1',
                         'pagesize': '10000'}
        self.url = 'http://cn.morningstar.com/handler/fundranking.ashx'
        return

    def getWebSoup(self, url, postData):
        source_code = requests.get(url, headers=random.choice(self.headers), params=postData)
        plainTxt = source_code.text
        soup = BeautifulSoup(plainTxt, 'html.parser')
        return soup

    def getOutStanding(self, soup, fundCategory):
        #生成表头
        fileContents = []
        fileContents.append(tuple(('基金代码', '基金名称',
                                   '一年回报率',
                                   '两年回报率',
                                   '三年回报率',
                                   '五年回报率',
                                   '总回报率')))

        tbody = soup.find('table', {'class': 'fr_tablecontent'})
        for fundBody in tbody.find_all('tr'):
            if not fundBody.find('td', {'class': 'fr_tablefooter'}):
                fundInfo = [fundContent for fundContent in fundBody.stripped_strings]
                if '-' in fundInfo[8:12]:
                    continue
                fileContents.append(tuple((fundInfo[1], fundInfo[2],
                                           fundInfo[8], fundInfo[9],
                                           fundInfo[10], fundInfo[11],
                                           fundInfo[13])))
        print('---->正在写入csv文件')
        self.writeIntoFile(fundCategory+'-outstanding', fileContents)
        return

    def getRanking(self, soup, fundCategory):
        #生成表头
        fileContents = []
        fileContents.append(tuple(('基金代码', '基金名称',
                          '一年排名', '一年百分比排名',
                          '两年排名', '两年百分比排名',
                          '三年排名', '三年百分比排名',
                          '五年排名', '五年百分比排名')))
        try:
            tbody = soup.find('table', {'class': 'fr_tablecontent'})
            for fundBody in tbody.find_all('tr'):
                if not fundBody.find('td', {'class': 'fr_tablefooter'}):
                    fundInfo = [fundContent for fundContent in fundBody.stripped_strings]
                    if '-' in fundInfo[5:13]:
                        continue
                    fileContents.append(tuple((fundInfo[1], fundInfo[2],
                                               fundInfo[5], fundInfo[6],
                                               fundInfo[7], fundInfo[8],
                                               fundInfo[9], fundInfo[10],
                                               fundInfo[11], fundInfo[12])))
        except AttributeError:
            pass

        print('---->正在写入csv文件')
        self.writeIntoFile(fundCategory+'-ranking', fileContents)
        return

    def getRisk(self, soup, fundCategory):
        #生成表头
        fileContents = []
        fileContents.append(tuple(('基金代码', '基金名称', '晨星代码',
                          '三年评级', '五年评级',
                          '波动幅度', '波动幅度评价',
                          '晨星风险系数', '晨星风险系数评价',
                          '夏普比率', '夏普比率评价')))
        try:
            tbody = soup.find('table', {'class': 'fr_tablecontent'})
            for fundBody in tbody.find_all('tr'):
                if not fundBody.find('td', {'class': 'fr_tablefooter'}):

                    fundInfo = [fundContent for fundContent in fundBody.stripped_strings]
                    starID = fundBody.find('td', {'sort': 'Default'}).a['href']
                    pattern = re.compile('(/quicktake/)(\w+)')
                    fundInfo.insert(3, re.search(pattern, starID).group(2))
                    starRating3 = fundBody.find('td', {'sort': 'StarRating3'}).img['src']
                    pattern = re.compile('(/common/images/smallstar)(\d)(\.gif)')
                    fundInfo.insert(5, re.search(pattern, starRating3).group(2))
                    starRating5 = fundBody.find('td', {'sort': 'StarRating5'}).img['src']
                    pattern = re.compile('(/common/images/smallstar)(\d)(\.gif)')
                    fundInfo.insert(6, re.search(pattern, starRating5).group(2))
                    if '-' in fundInfo[7:13]:
                        continue
                    fileContents.append(tuple((fundInfo[1], fundInfo[2],
                                               fundInfo[3],
                                               fundInfo[5], fundInfo[6],
                                               fundInfo[7], fundInfo[8],
                                               fundInfo[9], fundInfo[10],
                                               fundInfo[11], fundInfo[12])))
        except AttributeError:
            print('读取结束')

        print('---->正在写入csv文件')
        self.writeIntoFile(fundCategory+'-risk', fileContents)
        return

    def getTopFrame(self):
        categoryList = list(self.fundCategory.keys())

        for fundCategory in categoryList:
            self.postData['sort'] = 'Return5YearRank'
            self.postData['category'] = self.fundCategory[fundCategory]
            print(fundCategory)
            self.postData['tabindex'] = '2'
            soup = self.getWebSoup(self.url, postData=self.postData)
            print('%s正在处理'%fundCategory)
            self.getRanking(soup, self.fundCategory[fundCategory])
            self.postData['tabindex'] = '1'
            soup = self.getWebSoup(self.url, postData=self.postData)
            self.getOutStanding(soup, self.fundCategory[fundCategory])
            self.postData['tabindex'] = '0'
            self.postData['sort'] = 'ReturnYTD'
            soup = self.getWebSoup(self.url, postData=self.postData)
            self.getRisk(soup, self.fundCategory[fundCategory])
        return

    def writeIntoFile(self, filename, fileContent):  # 写入CSV文件
        with open('fund/'+filename+'.csv', 'a+', newline='', encoding='utf-8') as csvfile:
            spamWriter = csv.writer(csvfile)
            for line in fileContent:
                spamWriter.writerow(line)
        return

fundList = getAllFund()
fundList.getTopFrame()