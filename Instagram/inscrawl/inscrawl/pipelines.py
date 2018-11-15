# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import requests
import hashlib, os
import pymongo

from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.conf import settings
from .settings import MONGODB_SHEETNAME


class InscrawlPipeline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbname = settings['MONGODB_DBNAME']
        sheetname = settings['MONGODB_SHEETNAME']

        # 创建数据库连接
        client = pymongo.MongoClient(host, port)
        # 指定数据库
        mydb = client[dbname]
        # 存放数据的数据库表明
        self.sheet = mydb[sheetname]

    def process_item(self, item, spider):
        urls = item['urls']
        user = MONGODB_SHEETNAME
        # path = 'D:\\python_work\爬虫\Instagram\cherry_quasht'
        path = 'D:\\python_work\爬虫\Instagram\{user}'.format(user=user)
        floder = os.path.exists(path)
        if not floder:
            os.makedirs(path)

        for url in urls:
            h = hashlib.md5()
            h.update(url.encode('utf-8'))
            name = h.hexdigest()
            filename = path + '\{0}.{1}'.format(name, url[-3:])
            print(filename)
            response = requests.get(url=url)
            content = response.content
            print(content)
            with open(filename, 'wb') as f:
                f.write(content)
            f.close()

        return item


# # 继承scrapy.pipelines.images.ImagesPipeline类
# class InsImagesPipeline(ImagesPipeline):
#     def get_media_requests(self, item, info):
#         for display_url in item['display_url']:
#             yield Request(display_url, headers=DEFAULT_REQUEST_HEADERS)
#
#     # 重写item_completed,获取图片下载路径并保存到item
#     def item_completed(self, results, item, info):
#         if "display_url" in item:
#             image_file_path = ""
#             for ok, value in results:
#                 image_file_path = value["path"]
#             item['img_path'] = image_file_path
#         return item
