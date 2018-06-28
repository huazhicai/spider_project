# -*- coding: utf-8 -*-
import scrapy

from ..items import GanjiItem


class GanjiSpiderSpider(scrapy.Spider):
    name = 'ganji_spider'
    allowed_domains = ['3g.ganji.com']
    start_urls = ['https://3g.ganji.com/']

    def parse(self, response):
        for data in response.xpath('//div[@class="inforBox"]/div[@class="infor"]'):
            item = GanjiItem()
            item['title'] = data.xpath('.//div[@class="i-job"]/span[1]/text()').extract_first()
            item['salary'] = data.xpath('.//p[@class="i-salary"]/text()').extract_first()
            item['company'] = data.xpath('.//div[@class="i-else2"]/p/text()').extract_first()

