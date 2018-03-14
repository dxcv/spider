import scrapy
import re
from house import items
import logging
# logging.basicConfig(filename='test.log', filemode='w', level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig(filename='fang.log', filemode='w', level=logging.ERROR)


class FangSpider(scrapy.Spider):
    name = "fang"
    start_urls = [
        'http://newhouse.xian.fang.com/house/s/?ctm=1.xian.xf_search.page.1'
    ]

    def parse(self, response):
        # logging.info(response.text)
        for info in response.xpath('//div[@class="nlc_details"]'):
            name = info.xpath('div[1]/div[1]/a/text()').extract_first()
            link = info.xpath('div[1]/div[1]/a/@href').extract_first()
            region = info.xpath('div[3]/div[1]/a/span/text()').re_first(
                u"[\u4e00-\u9fa5]+")
            status = info.xpath('div[4]/span/text()').extract_first()
            item = items.FangItem()
            item['name'] = str(name).strip()
            item['region'] = region
            item['status'] = status
            # logger.info(item['name'])
            yield scrapy.Request(
                url=link,
                meta={
                    'item': item,
                    'proxy': 'http://122.114.31.177:808'
                },
                callback=self.parse_house)

        page = 1
        while page < 37:
            page += 1
            next_page = 'http://newhouse.xian.fang.com/house/s/b9' + str(page)
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_house(self, response):
        item = response.meta['item']

        item['score'] = response.xpath(
            '//div[@class="inf_left1 "]/div/a/text()').extract_first()
        item['price'] = response.xpath(
            '//*[@class="prib cn_ff"]/text()').extract_first()

        item['tags'] = response.xpath(
            '//*[@class="biaoqian1"]/a/text()').extract()

        item['bedrooms'] = list()
        bedrooms = response.xpath('//*[@class="fl zlhx"]/a/text()').extract()[
            1:]
        for x in bedrooms:
            temp = re.search(r"(\S+)\(", x).group(1)
            item['bedrooms'].append(temp.replace('居', '室'))

        item['address'] = response.xpath(
            '/html/body/div[3]/div[3]/div[2]/div[1]/div[10]/div[1]/span/text()'
        ).extract_first()
        item['release'] = response.xpath(
            '//*[@class="kaipan"]/text()').extract_first()
        yield item