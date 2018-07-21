# -*- coding: utf-8 -*-
import json
import os
import random
import re
import time
import urllib.request

import scrapy
from PIL import Image
from pytesseract import pytesseract
from redis import StrictRedis, ConnectionPool
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import Kefu58Item


class KefuSpider(scrapy.Spider):
    name = 'kefu'
    # redis_key = "company_url:items"
    start_urls = ['http://qy.58.com/49312589047318/']

    # def __init__(self):
    #     redis_config = {
    #         "host": "localhost", #redis ip
    #         "port": 6379,
    #         "db": 0,
    #     }
    #     pool = ConnectionPool(**redis_config)
    #     self.pool = pool
    #     self.redis = StrictRedis(connection_pool=pool)
    #     self.key = "company_url:items"
    #
    # def redis_pop(self):
    #     item = self.redis.lpop(self.key)
    #     yield json.loads(item)
    #

    # def start_requests(self):
    #     start_urls = [i.get('url', None) for i in self.redis_pop()]
    #     for url in start_urls:
    #         yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        if 'mq' in response.url:
            self.parse_detail_mq(response)
        else:
            self.parse_detail(response)

    def parse_detail_mq(self, response):
        self.logger.info("Crawling Mq Detail: {}".format(response.url))
        item = Kefu58Item()
        item['company'] = response.xpath('//div[@class="intro_middle"]/h3/text()').extract_first()
        item['scale'] = response.xpath('//div[@class="intro_down"]/table/tbody/tr[2]/td[3]/text()').extract_first()
        item['industry'] = response.xpath('//div[@class="intro_down"]/table/tbody/tr[4]/td[1]/a/text()').extract_first()
        item['contacts'] = response.xpath('//div[@class="intro_down"]/table/tbody/tr[4]/td[2]/text()').extract_first()
        item['phone'] = None
        url = response.xpath('//div[@class="intro_down"]/table/tbody/tr[6]/td[3]/a/@href').extract_first()
        item['website'] = url
        item['address'] = response.xpath(
            '//div[@class="intro_down"]/table/tbody/tr[6]/td[1]/span/text()').extract_first()
        if url and '5858.com' in url:
            time.sleep(random.randint(1, 3))
            yield scrapy.Request(url, meta={'item': item}, callback=self.parse_phone)
        elif url and 'qy.58.com' in url:
            img_url = response.xpath('//div[@class="intro_down"]/table/tbody/tr[4]/td[3]/img/@src').extract_first()
            if img_url is not None:
                item['phone'] = self.download_read_phone(img_url, url)
            yield item
        elif url == None:
            self.logger("Mq website is not exits")
        else:
            yield scrapy.Request(url, meta={'item': item}, callback=self.parse_official)

    # 下载并读取图片上的电话号码
    def download_read_phone(self, img_url, url):
        # 图片下载保存路径要用绝对路径
        img_file = os.path.dirname(os.path.abspath(__file__)) + '\images\%s.gif' % url.split('/')[-2]
        if not os.path.exists(img_file):
            urllib.request.urlretrieve(img_url, img_file)
        text = pytesseract.image_to_string(Image.open(img_file))
        return text

    def parse_detail(self, response):
        self.logger.info("Crawling Detail: {}".format(response.url))
        item = Kefu58Item()
        item['company'] = response.xpath('//div[@class="compT"]/h1/a/@title').extract_first()
        item['scale'] = response.xpath('//div[@class="basicMsg"]/ul/li[7]/text()').extract_first()
        item['industry'] = response.xpath('//div[@class="basicMsg"]/ul/li[9]/div/a/text()').extract_first()
        item['contacts'] = response.xpath('//div[@class="basicMsg"]/ul/li[2]/text()').extract_first()
        item['phone'] = None
        url = response.xpath('//div[@class="basicMsg"]/ul/li[6]/a/text()').extract_first()
        item['website'] = url
        item['address'] = response.xpath('//div[@class="basicMsg"]/ul/li[8]/div/var/text()').extract_first()
        if url and '5858.com' in url:
            time.sleep(random.randint(1, 2))
            yield scrapy.Request(url, meta={'item': item}, callback=self.parse_phone)
        elif url and 'qy.58.com' in url:
            img_url = response.xpath('//div[@class="basicMsg"]/ul/li[4]/img/@src').extract_first()
            if img_url is not None:
                item['phone'] = self.download_read_phone(img_url, url)
            yield item
        elif url == None:
            self.logger.info('website is not exists!')
        else:
            yield scrapy.Request(url, meta={'item': item}, callback=self.parse_official)

    def parse_phone(self, response):
        self.logger.info("Parse T page:{}".format(response.url))
        item = response.meta['item']
        item['phone'] = response.xpath('//div[@class="hotline"]/em/text()').extract_first()
        if not item['phone']:
            phone_obj = re.search(r'联系电话.*?<span>(.+?)</span>', response.text)
            if phone_obj is not None:
                item['phone'] = phone_obj.group(1)
        yield item

    # 解析公司官网
    def parse_official(self, response):
        self.logger.info("Parse official: {}".format(response.url))
        item = response.meta['item']
        phone_pattern = re.compile(r'(1\d{10})|(0571-\d{7,8})')
        phone_obj = phone_pattern.search(response.text)
        if phone_obj is not None:
            item['phone'] = phone_obj.group(1) or phone_obj.group(2)
        yield item
