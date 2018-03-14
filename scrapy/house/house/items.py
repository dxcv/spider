# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# class HouseItem(scrapy.Item):
# define the fields for your item here like:
# name = scrapy.Field()
# pass


class FangItem(scrapy.Item):
    name = scrapy.Field()
    address = scrapy.Field()
    bedrooms = scrapy.Field()
    region = scrapy.Field()
    status = scrapy.Field()
    tags = scrapy.Field()
    price = scrapy.Field()
    score = scrapy.Field()
    release = scrapy.Field()


class AnJuKeItem(scrapy.Item):
    name = scrapy.Field()
    address = scrapy.Field()
    bedrooms = scrapy.Field()
    region = scrapy.Field()
    status = scrapy.Field()
    tags = scrapy.Field()
    price = scrapy.Field()
    release = scrapy.Field()
    turn = scrapy.Field()
    street = scrapy.Field()
    house_type = scrapy.Field()
    developer = scrapy.Field()


class LeJuItem(scrapy.Item):
    name = scrapy.Field()
    address = scrapy.Field()
    bedrooms = scrapy.Field()
    region = scrapy.Field()
    status = scrapy.Field()
    tags = scrapy.Field()
    price = scrapy.Field()
    release = scrapy.Field()
    turn = scrapy.Field()


class QQItem(scrapy.Item):
    name = scrapy.Field()
    address = scrapy.Field()
    bedrooms = scrapy.Field()
    region = scrapy.Field()
    status = scrapy.Field()
    tags = scrapy.Field()
    price = scrapy.Field()
    release = scrapy.Field()
    turn = scrapy.Field()
    house_type = scrapy.Field()