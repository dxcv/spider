'''
对安居客中获取的数据进行处理,包括：
1. 户型的处理
2. 价格的处理
'''
from pymongo import MongoClient
from pprint import pprint
import re
import pandas as pd


def bedrooms(item):
    for x in range(len(item)):
        item[x] = re.sub(r"\(\d+\)", "", item[x])
   
    return item

def price(item):
    item = re.sub(r"元/㎡", "", item)
    item = re.sub(r"\(\S+\)", "", item)
    return item


client = MongoClient("127.0.0.1")
db = client.house
set_anjuke = db.anjuke

if __name__ == "__main__":
    for post in set_anjuke.find():
        print('\n%s:'%(post['name']), end='')
        if 'bedrooms' in post.keys() and len(post['bedrooms']) > 0:
            post['bedrooms'] = bedrooms(post['bedrooms'])

        post['price'] = price(post['price'])
        
        set_anjuke.update({'name': post['name']}, post)
        
