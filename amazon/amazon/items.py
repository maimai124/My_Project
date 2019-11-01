# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    data = scrapy.Field()
    author = scrapy.Field()
    type = scrapy.Field()
    type2 = scrapy.Field()
    price = scrapy.Field()
    Kindle_Unlimited = scrapy.Field()
    title = scrapy.Field()
    press = scrapy.Field()
    pass
