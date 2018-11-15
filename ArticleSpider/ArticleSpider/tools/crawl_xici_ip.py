import requests
from scrapy.selector import Selector
import MySQLdb
import time

conn = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="zf961118", db="spider", charset="utf8")
cursor = conn.cursor()


def crawl_ip():
    # 爬取西刺代理的ip
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }
    for i in range(1738):
        response = requests.get("http://www.xicidaili.com/nn/{0}".format(i), headers=headers)

        selector = Selector(text=response.text)
        all_trs = selector.css("#ip_list tr")

        ip_list = []
        for tr in all_trs[1:]:
            speed_str = tr.css(".bar::attr(title)").extract()[0]
            if speed_str:
                speed = float(speed_str.split("秒")[0])
            all_texts = tr.css("td::text").extract()

            ip = all_texts[0]
            port = all_texts[1]
            proxy_type = all_texts[5]
            ip_list.append((ip, port, proxy_type, speed))

        for ip_info in ip_list:
            cursor.execute(
                "insert into proxy_ip (ip, port, proxy_type, speed) values ('{0}','{1}','{2}','{3}')".format(ip_info[0],
                                                                                                             ip_info[1],
                                                                                                             ip_info[2],
                                                                                                             ip_info[3])
            )
            conn.commit()
        time.sleep(12)


class GetIP(object):
    def delete_ip(self, ip):
        # 从数据库中删除无效的ip
        delete_sql = """
                    delete from proxy_ip where ip='{0}'
                """.format(ip)
        cursor.execute(delete_sql)
        conn.commit()
        return True

    def judge_ip(self, ip, port):
        # 判断ip是否可用
        http_url = "https://www.baidu.com"
        proxy_url = "http://{0}:{1}".format(ip, port)

        try:
            proxy_dict = {
                'http': proxy_url
            }
            response = requests.get(http_url, proxies=proxy_dict)
        except Exception as e:
            print("invalid ip and port")
            self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            if code >= 200 & code < 300:
                print("effective ip")
                return True
            else:
                print("invalid ip and port")
                self.delete_ip(ip)
                return False

    def get_random_ip(self):
        # 从数据库中获取一个可用的ip
        random_sql = """
            SELECT ip, port FROM proxy_ip ORDER BY RAND() LIMIT 1
        """
        result = cursor.execute(random_sql)
        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]

            judge_re = self.judge_ip(ip, port)
            if judge_re:
                return "http://{0}:{1}".format(ip, port)
            else:
                return self.get_random_ip()


if __name__ == '__main__':
    get_ip = GetIP()
    get_ip.get_random_ip()
