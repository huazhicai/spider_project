# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import CompanyUrlItem


class CompanySpider(CrawlSpider):
    """Follow categories and extract links."""
    name = 'company_url'
    start_urls = ['http://hz.58.com/zptaobaokefu/']

    rules = [
        Rule(LinkExtractor(restrict_xpaths=('//*[@id="filterArea"]/ul/li[position()>1]',)),
             callback='parse_directory')
    ]

    def parse_directory(self, response):
        self.logger.info("Crawling: %s" % response.url)
        base_url = 'http://qy.58.com/'
        urls = response.xpath('//*[@id="list_con"]/li')
        for url in urls:
            item = CompanyUrlItem()
            uid = url.xpath('.//div[@class="item_con job_comp"]/input/@uid').extract_first().split('_')[0]
            mingqi = url.xpath('.//div[@class="comp_name"]/i/@class').extract_first()
            if mingqi and 'mingqi' in mingqi:
                item['url'] = base_url + 'mq/' + uid + '/'
                yield item
            else:
                item['url'] = base_url + uid + '/'
                print(item)
                yield item
        next_page = response.xpath('//div[@class="pagesout"]/a[@class="next"]/@href').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_directory)
