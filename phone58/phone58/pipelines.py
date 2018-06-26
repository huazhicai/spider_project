# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from . import settings


class Phone58Pipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DB,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            port=3306,
            charset='utf8'
        )
        self.cursor = self.connect.cursor()

    # @classmethod
    # def from_crawler(cls, crawler):
    #     return cls(
    #         crawler.settings.get('MYSQL_HOST'),
    #         crawler.settings.get('MYSQL_DB'),
    #         crawler.settings.get('MYSQL_USER'),
    #         crawler.settings.get('MYSQL_PASSWD')
    #     )

    # @classmethod
    # def from_settings(cls, settings):
    #     args = settings['MYSQL_HOST']

    def process_item(self, item, spider):
        if type(item).__name__ == 'Phone58Item':
            insert_sql = """insert into phone(title,salary,company,company_type,company_scale,industry,
                            contacts,phone,website,address) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            try:
                spider.logger.info('insert database %s' % item)
                self.cursor.execute(insert_sql, (
                    item['title'], item['salary'], item['company'], item['company_type'], item['company_scale'],
                    item['industry'], item['contacts'], item['phone'], item['website'], item['address']
                ))
                self.cursor.connection.commit()

            except BaseException as err:
                print("插入database失败 - ", err)

    def close_spider(self, spider):
        self.connect.close()
