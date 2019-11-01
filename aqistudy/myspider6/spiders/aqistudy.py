# -*- coding: utf-8 -*-
import scrapy

from ..items import Myspider6Item
from scrapy_redis.spiders import RedisSpider

class AqistudySpider(RedisSpider):
    name = 'aqistudy'
    allowed_domains = ['aqistudy.cn']
    base_url = "https://www.aqistudy.cn/historydata/"
    redis_key = "redis_key:urls"

    def parse(self, response):
        print('爬取城市信息....')
        url_list = response.xpath("//div[@class='all']/div[@class='bottom']/ul/div[2]/li/a/@href").extract()  # 全部链接
        city_list = response.xpath("//div[@class='all']/div[@class='bottom']/ul/div[2]/li/a/text()").extract()  # 城市名称
        for url,city in zip(url_list[:1],city_list[:1]):
            url = self.base_url + url
            yield scrapy.Request(url=url, callback=self.parse_month,meta={'city': city})

    def parse_month(self,response):
        print('爬取月份...')
        url_list = response.xpath('//tbody/tr/td/a/@href').extract()
        for url in url_list[:3]:
            url = self.base_url + url
            print(url)
            yield scrapy.Request(url=url, callback=self.parse_day,meta={'city': response.meta['city']})

    def parse_day(self, response):
        print('爬取最终数据...')
        item = Myspider6Item()
        node_list = response.xpath('//tr')
        node_list.pop(0)
        data = {response.meta['city']: {}}
        for node in node_list:
            date = node.xpath('./td[1]/text()').extract_first()
            item['aqi'] = node.xpath('./td[2]/text()').extract_first()
            item['quality'] = node.xpath('./td[3]/span/text()').extract_first()
            item['pm_25'] = node.xpath('./td[4]/text()').extract_first()
            item['pm_10'] = node.xpath('./td[5]/text()').extract_first()
            item['so_2'] = node.xpath('./td[6]/text()').extract_first()
            item['co'] = node.xpath('./td[7]/text()').extract_first()
            item['no_2'] = node.xpath('./td[8]/text()').extract_first()
            item['o_3'] = node.xpath('./td[9]/text()').extract_first()
            data[response.meta['city']].update({date:item})
            yield data


