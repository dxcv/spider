import scrapy
import re
from house import items
import logging
logging.basicConfig(filename='test.log', filemode='w', level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class QQSpider(scrapy.Spider):
    name = "qq"

    # start_urls = ['1']

    def __init__(self):
        self.url = 'http://db.house.qq.com/index.php?mod=search&act=newsearch&city=xian&showtype=1&page_no='
        self.house_url = 'http://db.house.qq.com/xian_'
        self.page_no = 1

    def start_requests(self):
        yield scrapy.Request(
            url=self.url + str(self.page_no), callback=self.parse_id)

    def parse_id(self, response):
        js = response.text
        house_id = re.findall(r"data-hid=\\\"(\d+)?\\\"", js)
        # logging.info(house_id)
        for x in house_id:
            yield scrapy.Request(
                url=self.house_url + str(x), callback=self.parse_house)

        if len(house_id) > 0:
            # logging.info(house_id)
            self.page_no += 1
            # logging.info('page number = {}'.format(self.page_no))
            yield scrapy.Request(
                url=self.url + str(self.page_no), callback=self.parse_id)

    def parse_house(self, response):
        # logging.info(response.xpath('//title'))
        item = items.QQItem()

        item['name'] = response.xpath(
            '//*[@class="name fl"]/div[1]/h2/text()').extract_first()

        price = response.xpath(
            '//*[@class="price"]/strong/text()').extract_first()
        if price == None:
            item['price'] = response.xpath(
                '//*[@class="price"]/text()').extract_first()
        else:
            item['price'] = price

        item['tags'] = response.xpath(
            '//*[@class="tag fl"]/div/ul/li/em/text()').extract()

        item['address'] = response.xpath(
            '//*[@class="itemContent itemContent3 pr"]/li[1]/text()'
        ).extract_first()

        item['release'] = response.xpath(
            '//*[@class="itemContent itemContent3 pr"]/li[2]/text()'
        ).extract_first()

        item['turn'] = response.xpath(
            '//*[@class="itemContent itemContent3 pr"]/li[3]/text()'
        ).extract_first()

        item['house_type'] = response.xpath(
            '//*[@class="itemContent itemContent3 pr"]/li[4]/text()'
        ).extract_first()

        item['region'] = response.xpath(
            '//*[@class="hdl ft"]/li[1]/p/text()').extract_first()
        yield item
