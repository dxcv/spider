import scrapy
import logging
from zhihu.items import ZhihuItem

logging.basicConfig(filename='test.log', level=logging.INFO)


class zhihuSpider(scrapy.Spider):
    name = 'zhihu'

    def start_requests(self):
        url = 'https://www.zhihu.com/search?'
        params = {'q': '机器学习', 'type': 'topic'}
        for key, values in params.items():
            url += key + '=' + values + '&'

        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for info in response.xpath('//*[@class="ContentItem-title"]'):
            item = ZhihuItem()
            title = info.xpath(
                'div/a/div/div/span')
            item['title'] = title.xpath('string(.)').extract()[0]

            yield item
