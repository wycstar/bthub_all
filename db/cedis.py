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
                              db=j['redis']['channel']['heat'])
        # 存储最近一周内的关键词并作分析
        self._e = redis.Redis(host=j['redis']['host'],
                              port=j['redis']['port'],
                              db=j['redis']['channel']['popular'])

    def put_heat(self, h):
        hd = h + '-' + time.strftime("%Y-%m-%d")
        if self._c.incr(hd) == 1:
            self._c.expire(hd, 16 * 24 * 3600)

    def get_heat(self, h):
        d = [(datetime.datetime.utcnow() - datetime.timedelta(days=x)).strftime("%Y-%m-%d") for x in range(14, 0, -1)]
        s = map(lambda x: 0 if x is None else int(x), [self._c.get(h + '-' + x) for x in d])
        return d, s

    # 利用两个sorted set来存储曾经搜过的词语，一个存储搜索数量，一个存储搜索时间，分别用于热搜和大家都在搜功能。
    # 在模块中定义了一个定时任务，每天删除14天之前的数据。
    def put_popular(self, k):
        p = self._e.pipeline()
        p.zincrby('heat', k, 1)
        p.zadd('fresh', k, int(time.time()))
        p.execute()

    def get_popular(self):
        return self._e.zrevrange('heat', 0, 9)

    # 取出最近搜索的词语
    def get_fresh(self):
        return self._e.zrevrange('fresh', 0, 9, withscores=True)

    def clean_fresh(self):
        l = self._e.zrangebyscore('fresh', 0, time.time() - time.time() % 86400 - 86400 * 14)
        map(lambda x: self._e.zrem('fresh', x), l)
