# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import logging


class HousePipeline(object):
    def __init__(self):
        self.client = MongoClient('mongodb://127.0.0.1')
        self.db = self.client.house

    def process_item(self, item, spider):
        if spider.name == 'anjuke':
            self.collection = self.db.anjuke
        elif spider.name == 'fang':
            self.collection = self.db.fang
        elif spider.name == 'leju':
            self.collection = self.db.leju
        elif spider.name == 'qq':
            self.collection = self.db.qq

        logging.info('---->{}'.format(item['name']))

        if self.collection.find_one({'name': item['name']}):
            pass
        else:
            self.collection.insert_one(dict(item))

        return item
