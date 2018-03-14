# encoding: utf-8

from bs4 import BeautifulSoup
import requests
import json
import random
import csv


class fundAnalysis:
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
        self.url = 'http://cn.morningstar.com/handler/quicktake.ashx'
        self.webUrl = 'http://cn.morningstar.com/quicktake/'

        return

    def getWebSoup(self, url):
        source_code = requests.get(url, headers=random.choice(self.headers))
        plainTxt = source_code.text
        soup = BeautifulSoup(plainTxt, 'html.parser')
        return soup

    def getBaseInfo(self, fundId):
        soup = self.getWebSoup(self.webUrl+fundId)
        category = soup.find('span', {'class': 'category'}).get_text()  #基金类型
        inception = soup.find('span', {'class': 'inception'}).get_text()  #成立时间
        subscribe = soup.find('span', {'class': 'subscribe'}).get_text()  #申购状态
        redeem = soup.find('span', {'class': 'redeem'}).get_text()  #赎回状态
        sbdesc = soup.find('span', {'class': 'sbdesc'}).get_text()  #投资风格箱

        return category, inception, subscribe, redeem, sbdesc

    def getJsonData(self, fundId, command):
        postData = {'fcid': fundId,
                    'command': command}
        source_code = requests.get(self.url, headers=random.choice(self.headers),
                                   params=postData)
        plain_text = source_code.text
        jData = json.loads(plain_text)
        return jData

    def getPortfolio(self, fundId):
        portfolio={}
        jData = self.getJsonData(fundId, 'portfolio')  # 获取资产分布
        portfolio['cash'] = jData['Cash']  # 现金
        portfolio['stock'] = jData['Stock']  # 股票
        portfolio['bond'] = jData['Bond']  # 债券
        portfolio['other'] = jData['Other']  # 其他
        return portfolio

    def getBanchmark(self, fundId):
        banchmark = {}
        jData = self.getJsonData(fundId, 'banchmark')  # 获取基本信息
        banchmark['fundName'] = jData['FundName']
        return banchmark

    def getRating(self, fundId):
        rating = []
        RiskStats = []
        jData = self.getJsonData(fundId, 'rating')
        try:
            rating = jData['RiskAssessment']
            RiskStats = jData['RiskStats']
        except TypeError:
            rating = []
            RiskStats = []
        return rating, RiskStats

    def analyzeFund(self, fundSet):
        for fundIndex in list(fundSet.index):
            fundID = fundSet.ix[fundIndex, '晨星代码']
            category, inception, subscribe, redeem, sbdesc = self.getBaseInfo(fundID)
            rating, RiskStats = self.getRating(fundID)
            if rating == []:
                print('---->数据异常')
                continue
            fundSet.ix[fundIndex, '晨星分类'] = category
            fundSet.ix[fundIndex, '成立日期'] = inception
            fundSet.ix[fundIndex, '申购状态'] = subscribe
            fundSet.ix[fundIndex, '赎回状态'] = redeem
            fundSet.ix[fundIndex, '投资风格箱'] = sbdesc
            fundSet.ix[fundIndex, '三年平均回报率'] = rating[0]['Year3']
            fundSet.ix[fundIndex, '五年平均回报率'] = rating[0]['Year5']
            fundSet.ix[fundIndex, '十年平均回报率'] = rating[0]['Year10']
            fundSet.ix[fundIndex, '三年标准差'] = rating[1]['Year3']
            fundSet.ix[fundIndex, '五年标准差'] = rating[1]['Year5']
            fundSet.ix[fundIndex, '十年标准差'] = rating[1]['Year10']
            fundSet.ix[fundIndex, '三年晨星风险系数'] = rating[2]['Year3']
            fundSet.ix[fundIndex, '五年晨星风险系数'] = rating[2]['Year5']
            fundSet.ix[fundIndex, '十年晨星风险系数'] = rating[2]['Year10']
            fundSet.ix[fundIndex, '三年夏普比率'] = rating[3]['Year3']
            fundSet.ix[fundIndex, '五年夏普比率'] = rating[3]['Year5']
            fundSet.ix[fundIndex, '十年夏普比率'] = rating[3]['Year10']
            fundSet.ix[fundIndex, '阿尔法系数'] = RiskStats[0]['ToInd']
            fundSet.ix[fundIndex, '贝塔系数'] = RiskStats[1]['ToInd']
            fundSet.ix[fundIndex, 'R平方'] = RiskStats[2]['ToInd']
            print('---->%s处理完毕'%fundSet.ix[fundIndex, '基金名称'])
        return fundSet

    def writeIntoFile(self, fileContent):  # 写入CSV文件
        with open('fundList.csv', 'a+', newline='', encoding='utf-8') as csvfile:
            spamWriter = csv.writer(csvfile)
            for line in fileContent:
                spamWriter.writerow(line)
        return

    def readCsvFile(self):
        with open('starID.csv', encoding='utf-8') as csvFile:
            fileContent = csv.reader(csvFile)
            #for line in fileContent:
            #    print(line)
        return fileContent



