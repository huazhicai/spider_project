# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class CompanyUrlItem(Item):
    url = Field()


class Kefu58Item(Item):
    # define the fields for your item here like:
    title = Field()
    salary = Field()
    company = Field()
    scale = Field()
    industry = Field()
    contacts = Field()
    phone = Field()
    website = Field()
    address = Field()
    pass
