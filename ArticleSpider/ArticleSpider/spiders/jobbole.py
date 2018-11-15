# -*- coding: utf-8 -*-
import scrapy
import re
import datetime

from ..items import JobBoleArticleItem, ArticleItemLoader
from ..utils.common import get_md5
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

'''
通过css选择器提取节点
title = response.css(".entry-header h1::text").extract()   # ::伪类选择器
create_data = response.css(".entry-meta-hide-on-mobile::text")
praise_nums = response.css(".vote-post-up h10::text").extract()[0]
fav_nums = response.css(".bookmark-btn::text").extract()[0]
match_re = re.match(".*(\d+).*", fav_nums)
if match_re:
    fav_nums = match_re.group(1)
    
comment_nums = response.css("a[href='#article-comment'] span::text").extract()[0]
match_re = re.match(".*(\d+).*", comment_nums)
if match_re:
    comment_nums = match_re.group(1)

content = response.css("div.entry").extract()[0]

tags = response.css("p.entry-meta-hide-on-mobie a::text").extract()
tags = [element for element in tags if not element.strip().endswith("评论")] 
tags = ",".join(tags)
'''


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    # 收集伯乐在线所有404的url以及404页面数
    handle_httpstatus_list = [404]

    def __init__(self, **kwargs):
        super(JobboleSpider, self).__init__()
        self.fail_urls = []
        dispatcher.connect(self.handle_spider_closed, signals.spider_closed)

    def handle_spider_closed(self, spider, reason):
        self.crawler.stats.set_value("failed_urls", ",".join(self.fail_urls))

    def parse(self, response):
        """
        1、获取文章列表页中的文章url并交给scrapy下载后并进行解析
        2、获取下一页的URL并交给scrapy进行下载并交给parse解析
        """
        # 解析列表页中的所有文章url并交给scrapy下载后并进行解析
        if response.status == 404:
            self.fail_urls.append(response.url)
            self.crawler.stats.inc_value("failed_url")

        articles = response.xpath('//div[@class="grid-8"]/div[@class="post floated-thumb"]')

        for each in articles:
            img_url = each.xpath('./div[@class="post-thumb"]/a/img/@src').extract()[0]
            page_url = each.xpath('./div[@class="post-meta"]//a[@class="archive-title"]/@href').extract()[0]
            yield scrapy.Request(url=page_url, callback=self.article_parse, meta={"img_url": img_url})
        # 获取下一页的URL并交给scrapy进行下载并交给parse解析
        next_url = response.xpath('//a[@class="next page-numbers"]/@href').extract()[0]
        if next_url is not None:
            yield scrapy.Request(url=next_url, callback=self.parse)

    def article_parse(self, response):
        # 通过item loader加载item
        img_url = response.meta.get("img_url", "")  # 文章封面图
        item_loader = ArticleItemLoader(item=JobBoleArticleItem(), response=response)
        item_loader.add_css("title", ".entry-header h1::text")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("create_date", ".entry-meta-hide-on-mobile::text")
        item_loader.add_value("img_url", [img_url])
        item_loader.add_css("praise_nums", ".vote-post-up h10::text")
        item_loader.add_css("fav_nums", ".bookmark-btn::text")
        item_loader.add_css("comment_nums", "a[href='#article-comment'] span::text")
        item_loader.add_css("tags", "p.entry-meta-hide-on-mobile a::text")
        item_loader.add_css("content", "div.entry")

        article_item = item_loader.load_item()

        yield article_item
