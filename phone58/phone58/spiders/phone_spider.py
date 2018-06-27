# -*- coding: utf-8 -*-
import re
import urllib.request
from PIL import Image
import pytesseract

import scrapy
from ..items import Phone58Item


class PhoneSpiderSpider(scrapy.Spider):
    name = 'phone_spider'
    # allowed_domains = ['hz.58.com']
    start_urls = ['http://hz.58.com/dianhuaxiaoshou/']

    def parse(self, response):
        resp = response.xpath('//*[@id="list_con"]/li')
        for i in resp:
            item = Phone58Item()
            title = i.xpath('.//div[@class="job_name clearfix"]/a/span/text()').extract()
            item['title'] = title[0] + '|' + title[-1]
            item['salary'] = i.xpath('.//p/text()').extract_first()
            item['company'] = i.xpath('./div[@class="item_con job_comp"]/div/a/text()').extract_first()
            # 企业uid
            uid = i.xpath('.//div[@class="item_con job_comp"]/input/@uid').extract_first().split('_')[0]
            mingqi = i.xpath('.//div[@class="comp_name"]/i/@class').extract_first()
            if mingqi and 'mingqi' in mingqi:
                url = "http://qy.58.com/mq/" + uid + '/'
                yield scrapy.Request(url, meta={'item': item}, callback=self.parse_detail_mq)
            else:
                url = "http://qy.58.com/" + uid + '/'
                yield scrapy.Request(url, meta={'item': item}, callback=self.parse_detail)
        next_page = response.xpath('//div[@class="pagesout"]/a[class="next"]/@href').extract_first()
        if next_page is not None:
            self.logger.info("Start Crawl: %s" % next_page)
            # yield response.follow(next_page, callback=self.parse)
            url = response.urljoin(next_page)
            yield scrapy.Request(url, callback=self.parse)

    def parse_detail_mq(self, response):
        item = response.meta['item']
        item['company_type'] = response.xpath('//div[@class="intro_down"]/table/tbody/tr[2]/td[2]/text()').extract_first()
        item['company_scale'] = response.xpath('//div[@class="intro_down"]/table/tbody/tr[2]/td[3]/text()').extract_first()
        item['industry'] = response.xpath('//div[@class="intro_down"]/table/tbody/tr[4]/td[1]/a/text()').extract_first()
        item['contacts'] = response.xpath('//div[@class="intro_down"]/table/tbody/tr[4]/td[2]/text()').extract_first()
        url = response.xpath('//div[@class="intro_down"]/table/tbody/tr[6]/td[3]/a/@href').extract_first()
        item['website'] = url
        item['address'] = response.xpath('//div[@class="intro_down"]/table/tbody/tr[6]/td[1]/span/text()').extract_first()
        if '5858.com' in url:
            yield scrapy.Request(url, meta={'item': item}, callback=self.parse_phone)
        elif 'qy.58.com' in url:
            img_url = response.xpath('//div[@class="intro_down"]/table/tbody/tr[4]/td[3]/img/@src').extract_first()
            if img_url is not None:
                img_file = 'F:\Project\spider_project\phone58\phone58\spiders\images\%s.gif' % url.split('/')[-2]
                urllib.request.urlretrieve(img_url, img_file)
                item['phone'] = pytesseract.image_to_string(Image.open(img_file))
                yield item
            else:
                item['phone'] = None
                yield item
        else:
            yield scrapy.Request(url, meta={'item': item}, callback=self.parse_official)

    def parse_detail(self, response):
        item = response.meta['item']
        item['company_type'] = response.xpath('//div[@class="basicMsg"]/ul/li[5]/text()').extract_first()
        item['company_scale'] = response.xpath('//div[@class="basicMsg"]/ul/li[7]/text()').extract_first()
        item['industry'] = response.xpath('//div[@class="basicMsg"]/ul/li[9]/div/a/text()').extract_first()
        item['contacts'] = response.xpath('//div[@class="basicMsg"]/ul/li[2]/text()').extract_first()
        url = response.xpath('//div[@class="basicMsg"]/ul/li[6]/a/text()').extract_first()
        item['website'] = url
        item['address'] = response.xpath('//div[@class="basicMsg"]/ul/li[8]/div/var/text()').extract_first()
        if '5858.com' in url:
            yield scrapy.Request(url, meta={'item': item}, callback=self.parse_phone)
        elif 'qy.58.com' in url:
            img_url = response.xpath('//div[@class="basicMsg"]/ul/li[4]/img/@src').extract_first()
            if img_url is not None:
                img_file = 'F:\Project\spider_project\phone58\phone58\spiders\images\%s.gif' % url.split('/')[-2]
                urllib.request.urlretrieve(img_url, img_file)
                item['phone'] = pytesseract.image_to_string(Image.open(img_file))
                yield item
            else:
                item['phone'] = None
                yield item
        else:
            yield scrapy.Request(url, meta={'item': item}, callback=self.parse_official)

    def parse_phone(self, response):
        item = response.meta['item']
        item['phone'] = response.xpath('//div[@class="hotline"]/em/text()').extract_first()
        if not item['phone']:
            phone_obj = re.search(r'联系电话.*?<span>(.+?)</span>', response.text)
            if phone_obj is not None:
                item['phone'] = phone_obj.group(1)
                yield item
            else:
                yield item
        else:
            yield item

    # 解析公司官网
    def parse_official(self, response):
        item = response.meta['item']
        cellPhone = re.compile(r'\d{11}')
        phone = re.compile(r'''
                    (0571|\(0571\))?
                    (\s|-|\.)?
                    (\d{8}|\d{7})''')
        retval = cellPhone.search(response.text)
        retval2 = phone.search(response.text)
        if retval is not None:
            item['phone'] = retval.group()
            yield item
        elif retval2 is not None:
            item['phone'] = retval2.group(1)+retval2.group(2)+retval2.group(3)
            yield item
        else:
            item['phone'] = None
            yield item
