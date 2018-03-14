import json
import os
from getPage import GetPage, readProxy
from bs4 import BeautifulSoup
import pprint
import constant
import random
from pymongo import MongoClient
import time

client = MongoClient('mongodb://127.0.0.1/lagou')
db = client.lagou
collection = db.dataset


def parseJob(positionId):
    url = 'https://www.lagou.com/jobs/' + str(positionId) + '.html'
    successful = False
    proxy = readProxy('https.txt')
    while not successful:
        try:
            proxy = {'https': random.choice(readProxy('https.txt'))}

            my_requests = GetPage()
            soup = my_requests.get(url, proxy=proxy)

            #soup = BeautifulSoup(plain_text, 'html.parser')

            description = soup.find('dd', {'class': 'job_bt'}).get_text(
                strip=True)

            successful = True
        except Exception as e:
            #pprint.pprint(e)
            pass

    return description


def parseInfo(plain_text):
    last_page = False

    jdict = json.loads(plain_text)
    jdata = jdict['content']['positionResult']['result']
    if jdata == []:
        print('----------已经到达最后一页----------')

        last_page = True
        return last_page

    for each in jdata:
        if collection.find_one({'positionId': each['positionId']}): continue

        each['job_bt'] = parseJob(each['positionId'])
        time.sleep(5)

        insert_id = collection.insert_one(each)
        print('%s --> %s --> %s 写入完成' %
              (each['companyFullName'], each['positionName'],
               insert_id.inserted_id))

    return last_page


def parsePage(plain_text):
    jdict = json.loads(plain_text)
    jdata = jdict['content']['positionResult']
    print('\n一共有' + jdata['totalCount'] + '个职位\n')

    return
