# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient


class Myspider6Pipeline(object):
    def open_spider(self,spider):
        print("cccccccccc")
        self.db = MongoClient().my_test

    def process_item(self, data, spider):
        print("dddddddddd")
        self.db.weather.insert_one(dict(data))
        return data