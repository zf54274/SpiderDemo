# -*- coding: utf-8 -*-
import codecs
import json
import pymongo
import MySQLdb
import MySQLdb.cursors

from scrapy.conf import settings
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline(object):
    # 自定义Json文件的导出
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()


class JsonExporterPipeline(object):
    # 调用scrapy提供的json_export导出json文件
    def __init__(self):
        self.file = open('articleexport.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class MysqlPipeline(object):
    # 采用同步的机制写入mysql
    def __init__(self):
        self.conn = MySQLdb.connect('localhost', 'root', 'zf961118', 'spider', 3306, charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql, params = item.get_insert_sql()
        self.cursor.execute(insert_sql, params)
        self.conn.commit()


class MysqlTwistedPipeline(object):
    # 通过Twisted采用异步的机制写入mysql
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        # MySQL 相关配置参数
        dbparms = dict(
            host=settings['MYSQL_HOST'],
            port=settings['MYSQL_PORT'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)  # 处理异常

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print(failure)

    def do_insert(self, cursor, item):
        # 执行具体的插入
        # 根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)


class MongoDBPipeline(object):
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
        data = dict(item)
        self.sheet.insert(data)
        return item


# 继承scrapy.pipelines.images.ImagesPipeline类
class ArticleImagesPipeline(ImagesPipeline):
    # 重写item_completed,获取图片下载路径并保存到item
    def item_completed(self, results, item, info):
        if "img_url" in item:
            image_file_path = ""
            for ok, value in results:
                image_file_path = value["path"]
            item['img_path'] = image_file_path
        return item
