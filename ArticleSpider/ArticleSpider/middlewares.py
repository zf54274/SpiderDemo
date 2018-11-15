# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import time

from scrapy import signals
from fake_useragent import UserAgent
# from .tools.crawl_xici_ip import GetIP
from scrapy.http import HtmlResponse


class ArticlespiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ArticlespiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


# class JSpageMiddleware(object):
#     # 通过Chrome进行模拟登录知乎
#     def process_request(self, request, spider):
#         if spider.name == "zhihu":
#             spider.browser.get(request.url)
#             time.sleep(3)
#             spider.browser.find_element_by_css_selector(".SignFlow-account input[name='username']") \
#                 .send_keys("177244220115")
#             time.sleep(1)
#             spider.browser.find_element_by_css_selector(".SignFlow-password input[name='password']") \
#                 .send_keys("zifeng961118.")
#             time.sleep(1)
#             spider.browser.find_element_by_css_selector(".SignFlow-submitButton").click()


class RandomUserAgentMiddleware(object):
    cookies = {
        '_ga': 'GA1.2.2038247551.1541130511',
        'user_trace_token': '20181102114831-2aa5147d-de52-11e8-85a6-5254005c3644',
        'LGUID': '20181102114831-2aa51a5d-de52-11e8-85a6-5254005c3644',
        'hasDeliver': '0',
        'index_location_city': '%E5%B9%BF%E5%B7%9E',
        'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%22166d28de19c5b-0c6f4dc9e5973c-b79183d-2073600-166d28de19d47a%22%2C%22%24device_id%22%3A%22166d28de19c5b-0c6f4dc9e5973c-b79183d-2073600-166d28de19d47a%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D',
        'showExpriedIndex': '1',
        'showExpriedCompanyHome': '1',
        'showExpriedMyPublish': '1',
        '_gid': 'GA1.2.831098786.1541467004',
        'JSESSIONID': 'ABAAABAAAFCAAEG351AE73B4A30D5F6A897683FC271DDDB',
        'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1541130512,1541467004,1541555280',
        'X_HTTP_TOKEN': 'a22d63c90d3c81f31331d615aee31d62',
        'LGSID': '20181107165216-6d43a6e1-e26a-11e8-9044-525400f775ce',
        'TG-TRACK-CODE': 'index_navigation',
        'SEARCH_ID': 'b70c8c20cded490b9e9a09081208d290',
        'login': 'false',
        'unick': '',
        '_putrc': '',
        'LG_LOGIN_USER_ID': '',
        '_gat': '1',
        'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1541583354',
        'LGRID': '20181107173555-86ac4c10-e270-11e8-9045-525400f775ce',
    }

    # 随机更换user-agent
    def __init__(self, crawler):
        super(RandomUserAgentMiddleware, self).__init__()
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", "random")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)
    
    def process_request(self, request, spider):
        def get_ua():
            return getattr(self.ua, self.ua_type)
        
        # spider是lagou, 则添加cookies
        if spider.name == "lagou":
            request.headers.setdefault('User-Agent', get_ua())
            request.cookies = self.cookies
        else:
            request.headers.setdefault('User-Agent', get_ua())


# class RandomProxyMiddleware(object):
#     # 动态设置ip代理
#     def process_request(self, request, spider):
#         get_ip = GetIP()
#         request.meta["proxy"] = get_ip.get_random_ip()
