# -*- coding: utf-8 -*-

import os

# Scrapy settings for ArticleSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'ArticleSpider'

SPIDER_MODULES = ['ArticleSpider.spiders']
NEWSPIDER_MODULE = 'ArticleSpider.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'ArticleSpider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 10
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    #     'Cookie': '_ga = GA1.2.2038247551.1541130511;user_trace_token = 20181102114831 - 2aa5147d - de52 - 11e8 - 85a6 - 5254005c3644;LGUID = 20181102114831 - 2aa51a5d - de52 - 11e8 - 85a6 - 5254005c3644;hasDeliver = 0;index_location_city = % E5 % B9 % BF % E5 % B7 % 9E;sensorsdata2015jssdkcross = % 7B % 22distinct_id % 22 % 3A % 22166d28de19c5b - 0c6f4dc9e5973c - b79183d - 2073600 - 166d28de19d47a % 22 % 2C % 22 % 24device_id % 22 % 3A % 22166d28de19c5b - 0c6f4dc9e5973c - b79183d - 2073600 - 166d28de19d47a % 22 % 2C % 22props % 22 % 3A % 7B % 22 % 24latest_traffic_source_type % 22 % 3A % 22 % E7 % 9B % B4 % E6 % 8E % A5 % E6 % B5 % 81 % E9 % 87 % 8F % 22 % 2C % 22 % 24latest_referrer % 22 % 3A % 22 % 22 % 2C % 22 % 24latest_referrer_host % 22 % 3A % 22 % 22 % 2C % 22 % 24latest_search_keyword % 22 % 3A % 22 % E6 % 9C % AA % E5 % 8F % 96 % E5 % 88 % B0 % E5 % 80 % BC_ % E7 % 9B % B4 % E6 % 8E % A5 % E6 % 89 % 93 % E5 % BC % 80 % 22 % 7D % 7D;showExpriedIndex = 1;showExpriedCompanyHome = 1;showExpriedMyPublish = 1;_gid = GA1.2.831098786.1541467004;JSESSIONID = ABAAABAAAFCAAEG351AE73B4A30D5F6A897683FC271DDDB;Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6 = 1541130512, 1541467004, 1541555280;X_HTTP_TOKEN = a22d63c90d3c81f31331d615aee31d62;TG - TRACK - CODE = index_navigation;SEARCH_ID = c65951ebab2943309c5e94bf72137713;Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6 = 1541563538;LGRID = 20181107120539 - 633539f5 - e242 - 11e8 - 86f9 - 5254005c3644'
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'ArticleSpider.middlewares.ArticlespiderSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'ArticleSpider.middlewares.RandomUserAgentMiddleware': 543,
    # 'ArticleSpider.middlewares.RandomProxyMiddleware': 443,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'ArticleSpider.pipelines.MysqlTwistedPipeline': 3,
    # 'ArticleSpider.pipelines.JsonExporterPipeline': 2,
    # 'ArticleSpider.pipelines.ArticleImagesPipeline': 1,
}
# 图片保存路径的配置
IMAGES_URLS_FIELD = "img_url"
project_dir = os.path.abspath(os.path.dirname(__file__))  # 获取当前目录路径
IMAGES_STORE = os.path.join(project_dir, 'images')

# IMAGES_MIN_HEIGHT = 100
# IMAGES_MIN_WIDTH = 100

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'

RANDOM_UA_TYPE = "random"

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# MongoDB的配置信息
# MONGODB_HOST = '127.0.0.1'
# MONGODB_PORT = 27017
# MONGODB中数据库名称
# MONGODB_DBNAME = 'Spider'
# 数据库中存放数据的表名称
# MONGODB_SHEETNAME = "Article_Spider"

# MySQL的配置信息
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_DBNAME = "spider"
MYSQL_USER = "root"
MYSQL_PASSWORD = "zf961118"

SQL_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
SQL_DATE_FORMAT = "%Y-%m-%d"
