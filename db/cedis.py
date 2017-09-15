#!/usr/bin/env python
# coding:utf-8

import redis
import json
import os
import sys
import time
import datetime


class RedisManager(object):
    def __init__(self):
        self._real_path = os.path.split(os.path.realpath(sys.argv[0]))[0]
        with open(self._real_path + os.sep + 'config.json') as f:
            j = json.loads(f.read())
        # 存储资源的下载次数(热度)
        self._c = redis.Redis(host=j['redis']['host'],
                              port=j['redis']['port'],
                              db=j['redis']['channel']['heat'],
                              password=j['redis']['password'])
        # 缓存前端的搜索结果
        self._d = redis.Redis(host=j['redis']['host'],
                              port=j['redis']['port'],
                              db=j['redis']['channel']['search'],
                              password=j['redis']['password'])
        # 存储最近一周内的关键词并作分析
        self._e = redis.Redis(host=j['redis']['host'],
                              port=j['redis']['port'],
                              db=j['redis']['channel']['popular'],
                              password=j['redis']['password'])

    def put_heat(self, h):
        hd = h + '-' + time.strftime("%Y-%m-%d")
        if self._c.incr(hd) == 1:
            self._c.expire(hd, 16 * 24 * 3600)

    def get_heat(self, h):
        d = [(datetime.datetime.utcnow() - datetime.timedelta(days=x)).strftime("%Y-%m-%d") for x in range(14, 0, -1)]
        s = map(lambda x: 0 if x is None else int(x), [self._c.get(h + '-' + x) for x in d])
        return d, s

    def put_cache(self, k, r):
        p = self._d.pipeline()
        p.set(k, r)
        p.expire(k, 3600) # 缓存前端搜索结果1小时
        p.execute()

    def get_cache(self, h):
        return self._d.get(h)

    # 利用两个sorted set来存储曾经搜过的词语，一个存储搜索数量，一个存储搜索时间，分别用于热搜和大家都在搜功能。
    # 在模块中定义了一个定时任务，每天删除14天之前的数据。
    def put_popular(self, k):
        p = self._e.pipeline()
        p.zincrby('heat', k, 1)
        p.zadd('fresh', k, int(time.time()))
        p.execute()

    def get_popular(self):
        return self._e.zrevrange('heat', 0, 9)
