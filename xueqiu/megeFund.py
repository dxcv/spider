# encoding: utf-8
import pandas as pd
import fundAnalysis


class megaFund:
    def __init__(self):
        self.fundDict = {'股票型': 'stock', '激进配置型': 'mix_radical', '灵活配置型': 'mix_flexible',
                             '标准混合型': 'mix_standard', '保守混合型': 'mix_keep',
                             '可转债': 'bond_convertible', '激进债券型': 'bond_radical',
                             '普通债券型': 'bond_general', '纯债基金': 'bond_pure', '短债基金': 'bond_short',
                             '市场基金': 'currency', '市场中性策略': 'market_neutral', '商品': 'commodities',
                             '保本基金': 'keep', '其它': 'other',
                             '指数型': 'index',
                             'ETF': 'etf',
                             'LOF': 'lof'}
        return

    def loadFundSet(self, fundCategory):
        #合并所有排名
        fileList = []
        fundRisk = pd.read_csv('fund/' + self.fundDict[fundCategory] + '-risk.csv', index_col='基金代码')
        if list(fundRisk.index) != []:
            fileList.append(fundRisk)
        fundOutstanding = pd.read_csv('fund/' + self.fundDict[fundCategory] + '-outstanding.csv', index_col='基金代码')
        if list(fundOutstanding.index) != []:
            fundOutstanding = fundOutstanding.drop('基金名称', axis=1)
            fileList.append(fundOutstanding)
        fundRanking = pd.read_csv('fund/'+self.fundDict[fundCategory]+'-ranking.csv', index_col='基金代码')
        if list(fundRanking.index) != []:
            fundRanking = fundRanking.drop('基金名称', axis=1)
            fileList.append(fundRanking)

        fundSet = pd.concat(fileList, axis=1)
        return fundSet

r = megaFund()
fundSet = r.loadFundSet('指数型')
fundSet = fundSet.dropna()

y = fundAnalysis.fundAnalysis()
fundSet = y.analyzeFund(fundSet)
fundSet.to_csv('result.csv')
