# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import datetime, re
import scrapy

from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from .settings import SQL_DATETIME_FORMAT, SQL_DATE_FORMAT


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def date_conver(value):
    match_re = re.match(".*?(\d+[/]\d+[/]\d+).*", value.strip())
    if match_re:
        value = match_re.group(1)
    try:
        create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()

    return create_date


def get_nums(value):
    match_re = re.match(".*(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums


def remove_comment_tags(value):
    # 去掉tag中提取的评论
    if "评论" in value:
        return ""
    else:
        return value


def return_value(value):
    return value


class ArticleItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()


class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field(
        # input_processor=MapCompose()  # Mapcompose能传递多个函数
    )
    create_date = scrapy.Field(
        input_processor=MapCompose(date_conver),
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    img_url = scrapy.Field(
        # 交给IamgesPipeline的参数是要list，用TakeFrist是str会报错
        output_processor=MapCompose(return_value)
    )
    img_path = scrapy.Field()
    praise_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    tags = scrapy.Field(
        input_processor=MapCompose(remove_comment_tags),
        output_processor=Join(",")
    )
    content = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                        insert into article_spider(title, create_date, url, url_object_id,img_url,img_path, praise_nums
                        , comment_nums, fav_nums, tags, content)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE content=VALUES(content)
                    """
        params = (
            self["title"], self["create_date"], self["url"], self["url_object_id"], self["img_url"], self["img_path"],
            self["praise_nums"], self["comment_nums"], self["fav_nums"], self["tags"], self["content"])

        return insert_sql, params


def handle_salary_min(value):
    match_re = re.match('(\d+).*', value)
    if match_re:
        value = int(match_re.group(1)) * 1000
    return value


def handle_salary_max(value):
    match_re = re.match('.*?(\d+)k $', value)
    if match_re:
        value = int(match_re.group(1)) * 1000
    return value


def handle_publish_date(value):
    match_re = re.match('(.*)\xa0 发布于拉勾网', value)
    if match_re:
        value = match_re.group(1)
    return value


def handle_job_city(value):
    # 去掉工作城市的斜线
    return value.replace("/", "")


def handle_work_years(value):
    match_re = re.match('经验(.*) /', value)
    if match_re:
        if match_re.group(1) == "1-3年":
            value = "3年及以下"
        else:
            value = match_re.group(1)
    return value


def handle_degree_need(value):
    match_re = re.match('(.{2}).*', value)
    if match_re:
        value = match_re.group(1)
    return value


def handle_job_addr(value):
    addr_list = value.split("\n")
    addr_list = [item.strip() for item in addr_list if item.strip() != "查看地图"]
    addr = ""
    for item in addr_list:
        match_re = re.match('.*?([\u4E00-\u9FA5]+)</a>', item)
        if match_re:
            if match_re.group(1) != "查看地图":
                addr += match_re.group(1)
        else:
            match_re = re.match('^- (.*)', item)
            if match_re:
                addr += match_re.group(1)
    return addr


tags_list = []


def handle_tags(value):
    global tag_list
    tags_list.clear()
    if len(value) > 0:
        tags_list.append(value)
    if len(tags_list) > 0:
        value = ",".join(tags_list)
        return value
    else:
        return None


class LagouJobItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()


class LagouJobItem(scrapy.Item):
    # 拉勾网职位信息
    title = scrapy.Field()  # 职位名称
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    salary_min = scrapy.Field(
        input_processor=MapCompose(handle_salary_min),
    )  # 薪资最小值
    salary_max = scrapy.Field(
        input_processor=MapCompose(handle_salary_max),
    )  # 薪资最大值
    job_city = scrapy.Field(
        input_processor=MapCompose(handle_job_city),
    )  # 工作城市
    work_years = scrapy.Field(
        input_processor=MapCompose(handle_work_years),
    )  # 工作年限
    degree_need = scrapy.Field(
        input_processor=MapCompose(handle_degree_need),
    )  # 学历要求
    job_type = scrapy.Field()  # 职位性质
    publish_time = scrapy.Field(
        input_processor=MapCompose(handle_publish_date),
    )  # 发布时间
    job_advantage = scrapy.Field()  # 职位诱惑
    job_desc = scrapy.Field()  # 职位描述
    job_addr = scrapy.Field(
        input_processor=MapCompose(handle_job_addr),
    )  # 工作地址
    company_name = scrapy.Field()  # 公司名称
    company_url = scrapy.Field()
    tags = scrapy.Field(
        input_processor=MapCompose(handle_tags)
    )  # 职位标签
    crawl_time = scrapy.Field()  # 爬取时间

    def get_insert_sql(self):
        insert_sql = """
                        insert into lagou_job(title, url, url_object_id, salary_min, salary_max, job_city, work_years
                        , degree_need, job_type, publish_time, job_advantage, job_desc, job_addr, company_name
                        , company_url, tags, crawl_time)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE salary_min=VALUES(salary_min), salary_max=VALUES(salary_max),
                        job_desc=VALUES(job_desc), crawl_time=VALUES(crawl_time)
                    """
        params = (
            self["title"], self["url"], self["url_object_id"], self["salary_min"], self["salary_max"], self["job_city"],
            self["work_years"], self["degree_need"], self["job_type"], self["publish_time"], self["job_advantage"],
            self["job_desc"], self["job_addr"], self["company_name"], self["company_url"], self["tags"],
            self["crawl_time"].strftime(SQL_DATETIME_FORMAT)
        )

        return insert_sql, params
