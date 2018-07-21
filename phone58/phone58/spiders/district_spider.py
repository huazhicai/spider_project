# -*- coding: utf-8 -*-
import scrapy
from ..items import DistrictUrlItem


class DistrictSpiderSpider(scrapy.Spider):
    name = 'district_spider'
    redis_key = "district:start_urls"
    # allowed_domains = ['hz.58.com']
    start_urls = ['http://hz.58.com/dianhuaxiaoshou/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'phone58.pipelines.RedisDistrictUrlsPipeline': 301,
        },
    }

    def parse(self, response):
        for url in response.xpath('//*[@id="filterArea"]/ul/li'):
            item = DistrictUrlItem()
            item['url'] = url.xpath('./a/@href').extract_first()
            yield item