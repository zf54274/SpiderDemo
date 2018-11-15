# -*- coding: utf-8 -*-

# Scrapy settings for inscrawl project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import os
import random

BOT_NAME = 'inscrawl'

SPIDER_MODULES = ['inscrawl.spiders']
NEWSPIDER_MODULE = 'inscrawl.spiders'

# MONGODB主机名
MONGODB_HOST = '127.0.0.1'
# MONGODB端口号
MONGODB_PORT = 27017
# MONGODB中数据库名称
MONGODB_DBNAME = 'Instagram'
# 数据库B中存放数据的表名称
MONGODB_SHEETNAME = input("请输入要爬取的博主名：")

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'inscrawl (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
UA_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
]
DEFAULT_REQUEST_HEADERS = {
    "Accept": "*/*",
    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6",
    "User-Agent": random.choice(UA_LIST),
    'Referer': 'https://www.instagram.com/cherry_quahst/',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
    'Host': 'www.instagram.com',
    'Cookie': 'mid=W5cWRAALAAE04IdB4caqur09LC06; '
              'mcd=3; '
              'csrftoken=826V0WZoX104Lp5Yjek112Fe6yox8686; '
              'shbid=5257; '
              'rur=PRN; '
              'ds_user_id=2326545395; '
              'sessionid=IGSCf82cca765beab1ba64daf94cd3473ba1cd7b0add82297b92650e10ab2c71a925%3AXavCfY92G7SsxO9g4vZ8BALXbPN75LIB%3A%7B%22_auth_user_id%22%3A2326545395%2C%22_auth_user_backend%22%3A%22accounts.backends.CaseInsensitiveModelBackend%22%2C%22_auth_user_hash%22%3A%22%22%2C%22_platform%22%3A4%2C%22_token_ver%22%3A2%2C%22_token%22%3A%222326545395%3AGkWvFXXfR2V3fAT3tc59zGbmpqAEjITv%3A8c229e90505ceb3435d0e55f8dcac20a1006dcf6fb066a1c58fef4d5c680100e%22%2C%22last_refreshed%22%3A1540436821.0900797844%7D; '
              'shbts=1540435593.61274; '
              'urlgen="{\"103.116.47.253\": 40676}:1gFVg3:baLAIlQhR6mW_khxvZJIujjKi74"',

}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'inscrawl.middlewares.InscrawlSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'inscrawl.middlewares.InscrawlDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'inscrawl.pipelines.InscrawlPipeline': 300,
    # 'inscrawl.pipelines.InsImagesPipeline': 1,
    # 'scrapy.pipelines.images.ImagesPipeline': 1,
}

# 图片保存路径配置
# IMAGES_URLS_FIELD = "display_url"
# project_dir = os.path.abspath(os.path.dirname(__file__))  # 获取当前目录路径
# IMAGES_STORE = os.path.join(project_dir, '{user}'.format(user=MONGODB_SHEETNAME))

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
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
