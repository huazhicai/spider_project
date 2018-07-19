# -*- coding: utf-8 -*-
import os
import random
import re
import time
import urllib.request

import scrapy
from PIL import Image
from pytesseract import pytesseract
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import Kefu58Item


class KefuSpider(CrawlSpider):
    name = 'kefu'
    # allowed_domains = ['hz.58.com/job/']
    start_urls = ['http://hz.58.com/zptaobao/?key=%E5%AE%A2%E6%9C%8D&final=1&jump=1']

    rules = [
        Rule(LinkExtractor(restrict_xpaths=('//*[@id="filterArea"]/ul/li[position()>1]',)),
             callback='parse_item'),
    ]

    def parse_item(self, response):
        self.logger.info("Start Crawl Index: %s" % response.url)
        resp = response.xpath('//*[@id="list_con"]/li')
        for i in resp:
            item = Kefu58Item()
            title = i.xpath('.//div[@class="job_name clearfix"]/a/span/text()').extract()
            item['title'] = title[0] + '|' + title[-1]
            item['salary'] = i.xpath('.//p[@class="job_salary"]/text()').extract_first()
            item['company'] = i.xpath('.//div[@class="comp_name"]/a/text()').extract_first()
            item['phone'] = None
            uid = i.xpath('.//div[@class="item_con job_comp"]/input/@uid').extract_first().split('_')[0]
            mingqi = i.xpath('.//div[@class="comp_name"]/i[@class="comp_icons mingqi"]')
            if mingqi:
                url = "http://qy.58.com/mq/" + uid + '/'
                yield scrapy.Request(url, meta={'item': item}, callback=self.parse_detail_mq)
            else:
                url = "http://qy.58.com/" + uid + '/'
                yield scrapy.Request(url, meta={'item': item}, callback=self.parse_detail)
        next_page = response.xpath('//div[@class="pagesout"]/a[@class="next"]/@href').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_item)

    def parse_detail_mq(self, response):
        self.logger.info("Crawling Mq Detail: {}".format(response.url))
        item = response.meta['item']
        item['scale'] = response.xpath('//div[@class="intro_down"]/table/tbody/tr[2]/td[3]/text()').extract_first()
        item['industry'] = response.xpath('//div[@class="intro_down"]/table/tbody/tr[4]/td[1]/a/text()').extract_first()
        item['contacts'] = response.xpath('//div[@class="intro_down"]/table/tbody/tr[4]/td[2]/text()').extract_first()
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
        item = response.meta['item']
        item['scale'] = response.xpath('//div[@class="basicMsg"]/ul/li[7]/text()').extract_first()
        item['industry'] = response.xpath('//div[@class="basicMsg"]/ul/li[9]/div/a/text()').extract_first()
        # /html/body/div[4]/div[1]/div[2]/div[2]/ul/li[2]
        item['contacts'] = response.xpath('//div[@class="basicMsg"]/ul/li[2]/text()').extract_first()
        # /html/body/div[4]/div[1]/div[2]/div[2]/ul/li[6]/a
        url = response.xpath('//div[@class="basicMsg"]/ul/li[6]/a/text()').extract_first()
        item['website'] = url
        item['address'] = response.xpath('//div[@class="basicMsg"]/ul/li[8]/div/var/text()').extract_first()
        if url and '5858.com' in url:
            time.sleep(random.randint(1, 2))
            yield scrapy.Request(url, meta={'item': item}, callback=self.parse_phone)
        elif url and 'qy.58.com' in url:
            time.sleep(random.randint(1, 2))
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
