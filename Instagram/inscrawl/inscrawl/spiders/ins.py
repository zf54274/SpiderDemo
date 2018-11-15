# -*- coding: utf-8 -*-
import scrapy
import json
import re, hashlib, random, time
from ..settings import DEFAULT_REQUEST_HEADERS, UA_LIST, MONGODB_SHEETNAME
from ..items import InscrawlItem, InsItemLoader


class InsSpider(scrapy.Spider):
    name = 'ins'
    allowed_domains = ['www.instagram.com']
    item = InscrawlItem()

    def __init__(self):
        super(InsSpider, self).__init__()
        self.user = MONGODB_SHEETNAME
        self.start_urls = ['https://www.instagram.com/{user}/'.format(user=self.user)]

    def parse(self, response):
        # with open('cherry.html', 'w', encoding='utf-8') as f:
        #     f.write(str(response.body, encoding='utf-8'))
        # f.close()
        scripts = response.xpath('//script[@type="text/javascript"]/text()').extract()

        url_base = "https://www.instagram.com/graphql/query/?query_hash=5b0222df65d7f6659c9b82246780caa7" \
                   "&variables=%7B%22id%22%3A%22{user_id}%22%2C%22first%22%3A12%2C%22" \
                   "after%22%3A%22{cursor}%22%7D"

        urls = []
        for each in scripts:
            if each.startswith('window._sharedData'):
                user_id = re.findall('"profilePage_([0-9]+)"', each, re.S)[0]
                # print(user_id)
                rhx_gis = re.findall('"rhx_gis":"([0-9a-z]+)"', each, re.S)[0]

                js_data = json.loads(each[21:-1], encoding='utf-8')
                page_info = js_data['entry_data']['ProfilePage'][0]['graphql']['user']["edge_owner_to_timeline_media"][
                    'page_info']
                edges = js_data['entry_data']['ProfilePage'][0]['graphql']['user']["edge_owner_to_timeline_media"][
                    'edges']
                cursor = page_info['end_cursor']
                flag = page_info['has_next_page']

                for edge in edges:
                    # item_loader = InsItemLoader(item=InscrawlItem(), response=response)
                    display_url = edge['node']['display_url']
                    urls.append(display_url)
                    # content = edge['node']['edge_media_to_caption']['edges'][0]['node']['text']
                    # comment = edge['node']['edge_media_to_comment']['count']
                    # like = edge['node']['edge_media_preview_like']['count']
                    #
                    # item_loader.add_value('user', self.user)
                    # item_loader.add_value('content', content)
                    # item_loader.add_value('display_url', [display_url])
                    # item_loader.add_value('like', like)
                    # item_loader.add_value('comment', comment)
                    #
                    # ins_item = item_loader.load_item()
                    # yield ins_item

                headers = DEFAULT_REQUEST_HEADERS

                if cursor is not None:
                    queryVariables = '{"id":"' + user_id + '","first":12,"after":"' + cursor + '"}'
                    headers['X-Instagram-GIS'] = self.hashStr(rhx_gis + ":" + queryVariables)
                headers['User-Agent'] = random.choice(UA_LIST)

                url = url_base.format(user_id=user_id, cursor=cursor)
                yield scrapy.Request(url, callback=self.js_parse,
                                     meta={'url_base': url_base, 'urls': urls, 'user_id': user_id, 'rhx_gis': rhx_gis},
                                     headers=headers)

    def js_parse(self, response):
        js_data = json.loads(response.text, encoding='utf-8')
        # 提取meta数据
        user_id = response.meta['user_id']
        rhx_gis = response.meta['rhx_gis']
        url_base = response.meta['url_base']
        urls = response.meta['urls']

        page_info = js_data['data']['user']['edge_owner_to_timeline_media']['page_info']
        # url中的after数据
        cursor = page_info['end_cursor']
        # 是否有下一页
        flag = page_info['has_next_page']
        edges = js_data['data']['user']['edge_owner_to_timeline_media']['edges']
        for edge in edges:
            # item_loader = InsItemLoader(item=InscrawlItem(), response=response)
            # display_url = ""
            if edge['node']['is_video']:
                display_url = edge['node']['video_url']
                # urls.append(display_url)
            else:
                if edge['node']['display_url']:
                    display_url = edge['node']['display_url']
                    urls.append(display_url)
            # content = edge['node']['edge_media_to_caption']['edges'][0]['node']['text']
            # comment = edge['node']['edge_media_to_comment']['count']
            # like = edge['node']['edge_media_preview_like']['count']
            #
            # item_loader.add_value('user', self.user)
            # item_loader.add_value('content', content)
            # item_loader.add_value('display_url', [display_url])
            # item_loader.add_value('like', like)
            # item_loader.add_value('comment', comment)
            #
            # ins_item = item_loader.load_item()
            # yield ins_item

        headers = DEFAULT_REQUEST_HEADERS
        if cursor is not None:
            queryVariables = '{"id":"' + user_id + '","first":12,"after":"' + cursor + '"}'
            headers['X-Instagram-GIS'] = self.hashStr(rhx_gis + ":" + queryVariables)
        headers['User-Agent'] = random.choice(UA_LIST)

        url = url_base.format(user_id=user_id, cursor=cursor)
        yield scrapy.Request(url, callback=self.js_parse,
                             meta={'url_base': url_base, 'urls': urls, 'user_id': user_id, 'rhx_gis': rhx_gis},
                             headers=headers)

        time.sleep(1)

        if not flag:
            self.item['urls'] = urls
            yield self.item

    def hashStr(self, strInfo):
        h = hashlib.md5()
        h.update(strInfo.encode("utf-8"))
        return h.hexdigest()
