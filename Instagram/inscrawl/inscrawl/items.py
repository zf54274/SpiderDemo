# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose


def return_value(value):
    return value


class InsItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()


class InscrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # user = scrapy.Field()
    # content = scrapy.Field()
    # display_url = scrapy.Field(
    #     output_processor=MapCompose(return_value)
    # )
    # like = scrapy.Field()
    # comment = scrapy.Field()
    urls = scrapy.Field()
