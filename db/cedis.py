#!/usr/bin/env python
# coding:utf-8

import redis
import json
import os
import sys
import time


class RedisManager(object):
    def __init__(self):
        self._real_path = os.path.split(os.path.realpath(sys.argv[0]))[0]
        with open(self._real_path + os.sep + 'config.json') as f:
            j = json.loads(f.read())
        self._c = redis.Redis(host=j['redis']['host'],
                              port=j['redis']['port'],
                              db=j['redis']['index'],
                              password=j['redis']['password'])

    def put(self, h):
        hd = h + '-' + time.strftime("%Y-%m-%d")
        if self._c.incr(hd) == 1:
            self._c.expire(hd, 15 * 24 * 3600)

    def get(self, h):
        return self._c.get(h)

    def check(self, h):
        return self._c.exists(h)

    def count(self):
        return len(self._c.keys())
