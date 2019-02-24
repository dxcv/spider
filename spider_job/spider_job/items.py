# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderJobItem(scrapy.Item):
    pid = scrapy.Field()
    title = scrapy.Field()
    href = scrapy.Field()
    company = scrapy.Field()
    address = scrapy.Field()
    salary = scrapy.Field()
    create_gmt = scrapy.Field()
    experience = scrapy.Field()
    education = scrapy.Field()
    welfares = scrapy.Field()
    job_description = scrapy.Field()
    contact = scrapy.Field()
    company_type = scrapy.Field()
    company_size = scrapy.Field()
    company_industry= scrapy.Field()
    # company_introduction = scrapy.Field()
