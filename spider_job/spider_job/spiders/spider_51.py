import scrapy
import json
from copy import deepcopy
from spider_job.items import SpiderJobItem
import re


class QianChengSpider(scrapy.Spider):
    name = "spider_51"
    start_urls = []

    def __init__(self):
        city = "西安"

        with open(
                "./data/start_urls_by_city.json", "r", encoding="utf-8") as f:
            locations = json.load(f)

        if isinstance(locations[city], list):
            self.start_urls.extend(locations[city])
        else:
            self.start_urls.append(locations)

        self.start_urls = [self.start_urls[-1]]

    def parse(self, response):
        selector = response.xpath("//*[@id='resultList']/*[@class='el']")

        for queryset in selector:
            item = SpiderJobItem()
            item['pid'] = queryset.xpath(
                "*[@class='t1 ']/input/@value").extract_first()
            item['title'] = queryset.xpath(
                "*[@class='t1 ']/span/a/@title").extract_first()
            href = queryset.xpath(
                "*[@class='t1 ']/span/a/@href").extract_first()

            if item['title'] is None:
                item['title'] = queryset.xpath(
                    "*[@class='t1 tg1']/span/a/@title").extract_first()
                href = queryset.xpath(
                    "*[@class='t1 tg1']/span/a/@href").extract_first()

            if item['title'] is None:
                item['title'] = queryset.xpath(
                    "*[@class='t1 tg2']/span/a/@title").extract_first()
                href = queryset.xpath(
                    "*[@class='t1 tg2']/span/a/@href").extract_first()

            if "https://jobs.51job.com" not in href:
                # 跳过具有独立页面的职位
                continue

            item['company'] = queryset.xpath(
                "*[@class='t2']/a/@title").extract_first()
            item['address'] = queryset.xpath(
                "*[@class='t3']/text()").extract_first()
            item['salary'] = queryset.xpath(
                "*[@class='t4']/text()").extract_first()
            item['create_gmt'] = queryset.xpath(
                "*[@class='t5']/text()").extract_first()

            yield scrapy.Request(
                url=href,
                callback=self.parse_detail,
                meta={'item': deepcopy(item)})

        page = response.xpath("//div[@class='p_in']/ul/*[@class='bk']/a")

        for dw in page:
            if dw.xpath("text()").extract_first() == "下一页":
                next_page = dw.xpath("@href").extract_first()
                yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_detail(self, response):
        item = response.meta['item']

        selector = re.sub(
            r"\s", "",
            response.xpath("//*[@class='msg ltype']/@title").
            extract_first()).split("|")

        item['experience'] = selector[1]
        item['education'] = selector[2]

        item['welfares'] = ",".join(
            response.xpath(
                "//div[@class='jtag']/div[@class='t1']/span/text()").extract())

        item['job_description'] = re.sub(
            r"\s|\<.*?\>|微信分享", "",
            response.xpath("//div[@class='bmsg job_msg inbox']").extract_first())

        selector = response.xpath(
            "//div[@class='tCompany_sidebar']/div[1]/div[@class='com_tag']/p/@title"
        ).extract()
        item['company_type'] = selector[0]
        item['company_size'] = selector[1]
        item['company_industry'] = selector[2]

        info = response.xpath(
            "//div[@class='tCompany_main']/div[2]/h2/span/text()").extract_first()

        if info == "联系方式":
            item['contact'] = re.sub(
                r"上班地址：|\s", "",
                response.xpath(
                    "string(//div[@class='tCompany_main']/div[2]/div/p)").
                extract_first())
        else:
            item['contact'] = ""

        print(item)
