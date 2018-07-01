# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import redis


class Phone58Pipeline(object):

    def __init__(self, host, db, user, passwd):
        self.connect = pymysql.connect(
            host=host,
            db=db,
            user=user,
            passwd=passwd,
            port=3306,
            charset='utf8'
        )
        self.cursor = self.connect.cursor()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            crawler.settings.get('MYSQL_HOST'),
            crawler.settings.get('MYSQL_DB'),
            crawler.settings.get('MYSQL_USER'),
            crawler.settings.get('MYSQL_PASSWD')
        )

    def process_item(self, item, spider):
        if type(item).__name__ == 'Phone58Item':
            select = self.cursor.execute("select id from district where website='%s'" % item['website'])
            insert_sql = """insert into district(title,salary,company,company_type,company_scale,industry,
                            contacts,phone,website,address) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            if not select:
                try:
                    spider.logger.info('*** Starting Insert %s' % item)
                    self.cursor.execute(insert_sql, (
                        item['title'], item['salary'], item['company'], item['company_type'], item['company_scale'],
                        item['industry'], item['contacts'], item['phone'], item['website'], item['address']
                    ))
                    self.cursor.connection.commit()
                    spider.logger.info('****** Insert Database Successfully!!! ******', item)
                except BaseException as err:
                    spider.logger.error("插入database失败 - ", err)
            else:
                spider.logger.info("The website already exists!!!")

    def close_spider(self, spider):
        self.connect.close()


class RedisDistrictUrlsPipeline(object):
    """
    把按区域划分的电话销售url存到redis中
    """
    def __init__(self, host, port, db):
        self.redis_client = redis.StrictRedis(
            host=host, port=port, db=db
        )

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get("REDIS_HOST"),
            port=crawler.settings.get("REDIS_PORT"),
            db=crawler.settings.get("REDIS_DB"),
        )

    def process_item(self, item, spider):
        # redis_key = 'district:start_urls'
        url = item['url']
        if url:
            self.redis_client.sadd(spider.redis_key, url)
            spider.logger.debug(
                '****** Success push to REDIS with {} ******'.format(url))
            return item