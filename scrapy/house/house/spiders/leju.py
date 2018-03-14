import scrapy
import re
from house import items
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig(filename='leju.log', filemode='w', level=logging.ERROR)


class LeJuSpider(scrapy.Spider):
    name = "leju"
    allowed_domains = ["house.leju.com"]
    start_urls = ['http://house.leju.com/sx/search/#wt_source=pc_sy_dh']

    def parse(self, response):
        # logging.info('=======================')
        for info in response.xpath('//*[@class="b_card"]'):
            name = info.xpath('div[2]/h2/a/text()').extract_first()
            link = info.xpath('div[2]/h2/a/@href').extract_first()
            url = re.search('(.+)#',
                            link).group(1) + 'xinxi/#wt_source=pc_nlpxx_dh'
            # huxing = re.search(('(.+)#'), link).group(1)+'huxing/#wt_source=pc_nlpxx_dh'

            status = info.xpath('div[2]/h2/span/text()').extract_first()
            
            region = info.xpath('div[2]/h3[1]/text()').extract_first()

            item = items.LeJuItem()
            
            item['name'] = str(name).strip()

            try:
                item['region'] = re.search('\[(\S+)\]', region).group(1)
            except Exception:
                item['region'] = "其他地区"

            item['status'] = status

            yield scrapy.Request(
                url=url, meta={'item': item}, callback=self.parse_house)
            # logging.error('{}--{}'.format(item['name'], url))

        next_page = response.xpath('//*[@class="next"]/@href').extract_first()

        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_house(self, response):
        item = response.meta['item']

        item['price'] = response.xpath(
            '//p[@class="price"]/em/text()').extract_first()

        item['tags'] = response.xpath(
            '//*[@class="tags_stat"]/text()').extract()
        # item['bedrooms'] = response.xpath(
        #     '//*[@class="fl zlhx"]/a/text()').extract()[1:]
        item['address'] = response.xpath(
            '/html/body/div[4]/div[1]/div/ul/li[6]/p/text()').extract_first()
        item['release'] = response.xpath(
            '/html/body/div[4]/div[1]/div/ul/li[1]/text()').extract_first()
        item['turn'] = response.xpath(
            '/html/body/div[4]/div[1]/div/ul/li[2]/p/text()').extract_first()
        yield item