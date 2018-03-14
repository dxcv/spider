import scrapy
import re
from house import items
import logging
# 获取logger实例，如果参数为空则返回root logger
logger = logging.getLogger(__name__)

# 文件日志
file_handler = logging.FileHandler("anjuke.log", encoding='utf-8', mode='w')

# 为logger添加的日志处理器
logger.addHandler(file_handler)

# 指定日志的最低输出级别，默认为WARN级别
logger.setLevel(logging.INFO)


class AnJuKeSpider(scrapy.Spider):
    name = "anjuke"
    start_urls = ['https://xa.fang.anjuke.com/?from=navigation']

    def parse(self, response):
        for info in response.xpath('//div[@class="infos"]'):
            name = info.xpath('a[1]/h3/span/text()').extract_first()
            link = info.xpath('a[1]/@href').extract_first()
            house_id = re.search(r"\d+", link).group()
            url = "https://xa.fang.anjuke.com/loupan/canshu-" + \
                str(house_id) + ".html?from=loupan_tab"

            yield scrapy.Request(url=url, callback=self.parse_house)

        # next_page = response.xpath(
        #     '//a[@class="next-page next-link"]/@href').extract_first()
        # if next_page:
        #     yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_house(self, response):
        item = items.AnJuKeItem()

        for info in response.xpath('/html/body/div[2]/div[1]/div[1]/div[1]/div[2]/ul/li'):
            name = info.xpath('div[1]/text()').extract_first()
            if name == u"楼盘名称":
                value = info.xpath('div[2]/a/text()').extract_first()
                item['name'] = value
                item['status'] = info.xpath('div[2]/i/text()').extract_first()
            elif name == u"楼盘特点":
                value = info.xpath('div[2]/a/text()').extract()
                item['tags'] = value
            elif name == u"物业类型":
                value = re.sub(r"\s", "", info.xpath(
                    'div[2]/text()').extract_first())
                item['house_type'] = value
            elif name == u"开发商":
                value = info.xpath('div[2]/a/text()').extract_first()
                item['developer'] = value
            elif name == u"楼盘地址":
                value = info.xpath('div[2]/text()').extract_first()
                item['address'] = value
            elif name == u"区域位置":
                value = re.sub(r"\s", "", info.xpath(
                    'div[2]').xpath('string(.)').extract_first())
                try:
                    item['region'] = re.search(
                        r"(\S+)-(\S+)-(\S+)", value).group(2)
                    item['street'] = re.search(
                        r"(\S+)-(\S+)-(\S+)", value).group(3)
                except Exception:
                    item['region'] = re.search(r"(\S+)-(\S+)", value).group(1)
                    item['street'] = re.search(r"(\S+)-(\S+)", value).group(2)
            elif name == u"参考单价":
                value = re.sub(r"\s", "", info.xpath('div[2]').xpath(
                    'string(.)').extract_first().replace(u"[价格走势]", ""))
                item['price'] = value

        for info in response.xpath('/html/body/div[2]/div[1]/div[1]/div[2]/div[2]/ul/li'):
            name = info.xpath('div[1]/text()').extract_first()
            if name == u"楼盘户型":
                value = info.xpath('div[2]/a/text()').extract()
                item['bedrooms'] = value
            elif name == u"最新开盘":
                value = re.sub(r"\s", "", info.xpath(
                    'div[2]/text()').extract_first())
                item['release'] = value
            elif name == u"交房时间":
                value = re.sub(r"\s", "", info.xpath(
                    'div[2]/text()').extract_first())
                item['turn'] = value
        # logger.info(item)
        yield item
