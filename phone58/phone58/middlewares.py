# -*- coding: utf-8 -*-

# Define here the models for your spiders middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random

from scrapy import signals


class Phone58SpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spiders middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spiders
        # middleware and into the spiders.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spiders or process_spider_input() method
        # (from other spiders middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spiders, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RandomUserAgentMiddleware(object):
    # 随机更换用户代理
    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        agent = crawler.settings.getlist('USER_AGENTS')
        return cls(agent)

    def process_request(self, request, spider):
        request.headers.setdefault("User-Agent", random.choice(self.agents))


# class RandomProxyMiddleware(object):
#     # 随机更换ip
#     def __init__(self, ip):
#         self.ip = ip
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         ip_pool = crawler.settings.getlist("IP_POOL")
#         return cls(ip_pool)
#
#     def process_request(self, request, spiders):
#         this_ip = random.choice(self.ip)
#         request.meta["proxy"] = "http://" + this_ip["ipaddr"]