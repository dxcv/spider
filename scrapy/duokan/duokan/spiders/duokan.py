import scrapy
import re
from duokan.items import DuokanItem
import logging

# logging.basicConfig(filename='test.log',level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
fh = logging.FileHandler('test.log')
# fh.setLevel(logging.INFO)
logger.addHandler(fh)


class duokanSpider(scrapy.Spider):
    name = 'duokan'

    start_urls = ['http://www.duokan.com/list/1-1']

    def __init__(self):
        logging.info(
            '------------------------开始读取网页信息------------------------')
        self.main_url = 'http://www.duokan.com'

    def parse(self, response):
        for info in response.xpath('//*[@class="level1"]'):
            item = DuokanItem()
            item['level_1_tag'] = info.xpath('div/a/span/text()').extract()[0]
            # logging.info(
            #     '------------------------开始抓取{}------------------------'.
            #     format(item['level_1_tag']))
            url = self.main_url + info.xpath('div/a/@href').extract()[0]

            yield scrapy.Request(url=url, callback=self.parse_tag, meta=item)

    def parse_tag(self, response):
        for info in response.xpath('//*[@class="level2"]/li'):
            item = response.meta
            item['level_2_tag'] = info.xpath('div/a/span/text()').extract()[0]
            self.logger.info(
                '------------------------开始抓取 {}-{}------------------------'.
                format(item['level_1_tag'], item['level_2_tag']))
            url = self.main_url + info.xpath('div/a/@href').extract()[0]
            yield scrapy.Request(url=url, callback=self.parse_page, meta=item)

    def parse_page(self, response):
        for info in response.xpath('//*[@class="info"]'):
            item = response.meta
            item['title'] = info.xpath(
                'div[@class="wrap"]/a[@class="title"]/text()').extract()[0]
            item['author'] = info.xpath(
                'div[@class="wrap"]/div[@class="u-author"]/span/text()'
            ).extract()[0]

            item['book_id'] = info.xpath(
                'div[@class="wrap"]/a[@class="title"]/@href').re_first(r'\d+')

            url = self.main_url + '/book/' + item['book_id']

            yield scrapy.Request(url=url, callback=self.parse_book, meta=item)

        if response.xpath('//a[@class="next "]'):
            url = self.main_url + response.xpath(
                '//a[@class="next "]/@href').extract()[0]

            yield scrapy.Request(url=url, callback=self.parse_page)

    def parse_book(self, response):
        if response.status == 404:
            logger.info(response.url)

        item = response.meta

        # 获取评分
        try:
            item['score'] = float(
                response.xpath('//em[@class="score"]/text()').extract()[0])
        except Exception:
            item['score'] = 0

        # 获取评论数量
        try:
            item['comment_counts'] = int(
                response.xpath('//span[@itemprop="reviewCount"]/text()')
                .extract()[0])
        except Exception:
            item['comment_counts'] = 0

        # 获取折扣价
        item['discount_price'] = response.xpath(
            '//div[@class="price"]/em/text()').extract()[0]

        # 获取原价
        try:
            item['original_price'] = response.xpath(
                '//div[@class="price"]/i[1]/del/text()').extract()[0]
        except Exception:
            item['original_price'] = 0

        # 获取纸书价格
        try:
            item['paper_price'] = response.xpath(
                '//div[@class="price"]/i[2]/del/text()').extract()[0]
        except Exception:
            item['paper_price'] = 0

        yield item
