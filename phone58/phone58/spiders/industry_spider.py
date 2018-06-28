# -*- coding: utf-8 -*-
import scrapy
from ..items import IndustryUrlItem


class IndustrySpiderSpider(scrapy.Spider):
    name = 'industry_spider'
    allowed_domains = ['hz.58.com']
    start_urls = ['http://hz.58.com/job.shtml']
    custom_settings = {
        'REDIS_HOST': '127.0.0.1',
        'REDIS_PORT': '6379',
        'REDIS_DB': '2',
        'ITEM_PIPELINES': {
            'phone58.pipelines.RedisStartUrlsPipeline': 301,
        },
        'DOWNLOADER_MIDDLEWARES': {
          # 'phone58.middlewares.ProxyMiddleware': 543
        },
    }

    def parse(self, response):
        """
        采集各个行业的电话销售链接
        :param response:
        :return:
        """
        prefix_url = 'http://hz.58.com/dianhuaxiaoshou'
        for data in response.xpath('//*[@id="divIndCate"]/ul/li[position()>1]'):
            item = IndustryUrlItem()
            suffix_url = data.xpath('./a/@href').extract_first()
            url = prefix_url + suffix_url
            item['url'] = url
            yield item


