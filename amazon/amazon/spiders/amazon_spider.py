# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from ..items import AmazonItem


class AmazonSpiderSpider(RedisSpider):
    name = 'amazon_spider'
    allowed_domains = ['www.amazon.cn']
    redis_key = "redis_key:urls"

    def parse(self, response):
        # 一级路由列表
        booktype_url_first = response.xpath('//li/span/a/@href').extract()[0:37]
        # 一级类型
        booktype_first = response.xpath('//li/span/a').extract()[0:37]
        for i in range(0, 1):
            url = booktype_url_first[i]
            # type = booktype_first[i]

            yield scrapy.Request(url=url, callback=self.parse_second)

    def parse_second(self, response):
        # 二级路由
        booktype_url_second = response.xpath(
            '//ul[@class="a-unordered-list a-nostyle a-vertical s-ref-indent-two"]/div//a/@href').extract()
        # 二级分类
        boooktype_second = response.xpath(
            '//ul[@class="a-unordered-list a-nostyle a-vertical s-ref-indent-two"]/div//a/span/text()').extract()
        for i in booktype_url_second[:1]:
            url = i
            type_second = boooktype_second

            yield scrapy.Request(url=i, callback=self.parse_third)

    def parse_third(self, response):
        node_list = response.xpath('//*[@class="s-item-container"]/div')
        if node_list:
            for node in node_list:
                items = AmazonItem()
                # 书名
                items['title'] = node.xpath('.//h2/text()').extract_first()
                # 作者
                items['author'] = node.xpath(
                    './/span[@class="a-size-small a-color-secondary"][2]/text()').extract()
                # 时间
                items['data'] = node.xpath(
                    './/span[@class="a-size-small a-color-secondary"][1]/text()').extract()
                # # 类型
                items['type'] = node.xpath('.//h3/text()').extract()
                # 价格
                items['price'] = node.xpath(
                    './/span[@class="a-size-base a-color-price s-price a-text-bold"]/text()').extract()
                # 运营类型
                items['type2'] = node.xpath('.//i[@class="sx-self-operated"]/text()').extract()
                #Kindle Unlimited
                if items['price'][0] == '￥0.00':
                    items['Kindle_Unlimited'] = True
                yield items
        else:
            node_list = response.xpath('//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div/div/span/div/div/div[2]/div[2]/div/div[1]/div/div/div[1]/h2/a/span/text()')
            for i in range(1,len(node_list)):
                items = AmazonItem()
                items['title'] = response.xpath('//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div['+str(i)+']/div/span/div/div/div[2]/div[2]/div/div[1]/div/div/div[1]/h2/a/span/text()').extract_first()
                items['author'] = response.xpath('//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div['+str(i)+']/div/span/div/div/div[2]/div[2]/div/div[1]/div/div/div[1]/div/span[2]/text()').extract()
                items['type'] = response.xpath('//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div['+str(i)+']/div/span/div/div/div[2]/div[2]/div/div[2]/div[1]/div/div[1]/div[1]/a/text()').extract_first().replace('\n','').replace(' ','')
                items['price'] = response.xpath('//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div['+str(i)+']/div/span/div/div/div[2]/div[2]/div/div[2]/div[1]/div/div[1]/div[2]/div/a/span/span[1]/text()').extract()
                items['type2'] = response.xpath('//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]/div['+str(i)+']/div/span/div/div/div[2]/div[2]/div/div[2]/div[1]/div/div[2]/div/span/text()').extract()
                yield items
        #下一页面链接
        if response.xpath("//div[@class='a-text-center']/ul/li[@class='a-last']/a/@href|//div[@class='pagnHy']/span[@class='pagnRA']/a/@href"):
            url = "https://www.amazon.cn/" + response.xpath("//div[@class='a-text-center']/ul/li[@class='a-last']/a/@href|//div[@class='pagnHy']/span[@class='pagnRA']/a/@href").extract_first()
            yield scrapy.Request(url=url,callback=self.parse_third)

