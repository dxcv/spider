# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import logging

# def dbHandle():

#     return collection


class DuokanPipeline(object):
    def __init__(self):
        self.client = MongoClient('mongodb://127.0.0.1')
        self.db = self.client.duokan
        self.collection = self.db.dataset

    def process_item(self, item, spider):
        # collection = dbHandle()
        if self.collection.find_one({'book_id': item['book_id']}):
            pass
        else:
            logging.info('---->{}'.format(item['title']))
            self.collection.insert_one(dict(item))

        return item
