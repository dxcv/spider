# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DuokanItem(scrapy.Item):
    # define the fields for your item here like:
    level_1_tag = scrapy.Field()
    level_2_tag = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    comment_counts = scrapy.Field()
    score = scrapy.Field()
    original_price = scrapy.Field()
    discount_price = scrapy.Field()
    paper_price = scrapy.Field()
    book_id = scrapy.Field()


