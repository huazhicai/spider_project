# -*- coding: utf-8 -*-
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
            link = i.xpath('.//div[@class="comp_name"]/a/@href').extract_first()
            if 'mq' in link:
                yield scrapy.Request(url=link, meta={'item': item}, callback=self.parse_detail_mq)
            else:
                yield scrapy.Request(url=link, meta={'item': item}, callback=self.parse_detail)

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
            item['phone'] = response.xpath('//div[@class="intro_down"]/table/tbody/tr[4]/td[3]/img/@src').extract_first()
            yield item

    def parse_detail(self, response):
        item = response.meta['item']
        item['company_type'] = response.xpath('//div[@class="basicMsg"]/ul/li[5]/text()').extract_first()
        item['company_scale'] = response.xpath('//div[@class="basicMsg"]/ul/li[7]/text()').extract_first()
        item['industry'] = response.xpath('//div[@class="basicMsg"]/ul/li[9]/text()').extract_first()
        item['contacts'] = response.xpath('//div[@class="basicMsg"]/ul/li[2]/text()').extract_first()
        url = response.xpath('//div[@class="basicMsg"]/ul/li[6]/text()').extract_first()
        item['website'] = url
        item['address'] = response.xpath('//div[@class="basicMsg"]/ul/li[8]/text()').extract_first()
        if '5858.com' in url:
            yield scrapy.Request(url, meta={'item': item}, callback=self.parse_phone)
        elif 'qy.58.com' in url:
            item['phone'] = response.xpath('//div[@class="basicMsg"]/ul/li[4]/@src').extract_first()
            yield item

    def parse_phone(self, response):
        item = response.meta['item']
        item['phone'] = response.xpath('//div[@class="hotline"]/em/text()')
        yield item


