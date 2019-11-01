# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Myspider6Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    month = scrapy.Field()
    city = scrapy.Field()
    day = scrapy.Field()
    aqi = scrapy.Field()
    sphere = scrapy.Field()
    quality = scrapy.Field()
    pm_25 = scrapy.Field()
    pm_10 = scrapy.Field()
    so_2 = scrapy.Field()
    co = scrapy.Field()
    no_2 = scrapy.Field()
    o_3 = scrapy.Field()
