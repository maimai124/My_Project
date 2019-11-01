import json

from jsonpath import jsonpath
import requests,random
import time
from pymongo import MongoClient

class tencent_careers(object):
    """多页面爬取版"""
    def __init__(self):
        self.base_url = "https://careers.tencent.com/tencentcareer/api/post/Query"


    def send_request(self,p):
        # 发送请求
        ua_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]

        time_stamp = str(int(time.time()*1000))


        header = {
            'authority': 'careers.tencent.com',
            'cookie': 'loading = agree',
            'referer': 'https: // careers.tencent.com / search.html?query = ot_40001001, ot_40001002, ot_40001003, ot_40001004, ot_40001005, ot_40001006 & index = 2',
            'sec - fetch - mode': 'cors',
            'sec - fetch - site': 'same - origin',
            'user - agent': random.choice(ua_list),
        }

        Query = {
            'timestamp': time_stamp,
            'countryId':'',
            'cityId':'',
            'bgIds':'',
            'productId':'',
            'categoryId': '40001001, 40001002, 40001003, 40001004, 40001005, 40001006',
            'parentCategoryId':'',
            'attrId':'',
            'keyword':'',
            'pageIndex': p,
            'pageSize': 10,
            'language': 'zh-cn',
            'area': 'cn',
        }

        response = requests.get(url=self.base_url,params=Query,headers=header)
        response.encoding='utf-8'
        # 解析htmL文档,返回json格式文件
        json_obj = json.loads(response.text)
        return json_obj

    def spider_tencent_careers(self, response):
        """数据处理"""
        info = jsonpath(response,"$.Data.Posts[*]")
        return info

    def connect_mongo(self):
        """连接mongodb"""
        conn = MongoClient("localhost", 27017)
        db = conn.my_test
        collection = db.work
        return  collection

    def main(self,p):
        response = self.send_request(p)
        info_list = self.spider_tencent_careers(response)
        collection = self.connect_mongo()
        for i in info_list:
            collection.insert_one(i)



if __name__ == '__main__':
    tencent_careers = tencent_careers()
    p = 1
    while True:
        if p <= 10:
            tencent_careers.main(p)
            p += 1
        else:
            break
