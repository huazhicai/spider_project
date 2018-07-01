# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DistrictUrlItem(scrapy.Item):
    url = scrapy.Field()


class IndustryUrlItem(scrapy.Item):
    url = scrapy.Field()


class Phone58Item(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    salary = scrapy.Field()
    company = scrapy.Field()
    company_type = scrapy.Field()
    company_scale = scrapy.Field()
    industry = scrapy.Field()
    contacts = scrapy.Field()
    phone = scrapy.Field()
    website = scrapy.Field()
    address = scrapy.Field()
    pass


