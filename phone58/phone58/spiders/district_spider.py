# -*- coding: utf-8 -*-
import scrapy
from ..items import DistrictUrlItem


class DistrictSpiderSpider(scrapy.Spider):
    name = 'district_spider'
    allowed_domains = ['hz.58.com']
    start_urls = ['http://hz.58.com/dianhuaxiaoshou/']

    def parse(self, response):
        pass