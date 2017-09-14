#!/usr/bin/env python
# coding:utf-8

import pymongo
import os
import sys
import json
from time import time

'''
数据结构：
_id:资源的infohash
n:资源的名字
f:文件结构：
    包含n-名字和l-长度
d:创建日期
m:修改日期
l:总长度
s:文件总数
e:是否被屏蔽
t:资源类型
c:资源热度
'''

class MongoManager(object):
    def __init__(self):
        self._real_path = os.path.split(os.path.realpath(sys.argv[0]))[0]
        with open(self._real_path + os.sep + 'config.json') as f:
            c = json.loads(f.read())
        self._c = pymongo.MongoClient(host=c['mongodb']['host'],
                                      port=c['mongodb']['port'],
                                      connect=False)[c['mongodb']['db']][c['mongodb']['collection']]

    def put(self, content):
        self._c.update(
            {'_id': content.get('_id')},
            {'$setOnInsert': content,
             '$set': {'m': int(time())},
             '$inc': {'c': 1}},
            upsert=True
        )

    def get(self, h):
        return self._c.find_one({'_id': h})
