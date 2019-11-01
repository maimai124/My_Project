import pymysql
import redis
from django.test import TestCase

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='mall', charset='utf8')
# Create your tests here.
pool = redis.ConnectionPool(host='localhost', port=6379)
r = redis.Redis(connection_pool=pool)
r.delete('chenhan')
