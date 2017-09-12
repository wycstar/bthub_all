#!/usr/bin/env python
# coding:utf-8

import pymongo
import os
import sys
import json


class MongoManager(object):
    def __init__(self):
        self._real_path = os.path.split(os.path.realpath(sys.argv[0]))[0]
        with open(self._real_path + os.sep + 'config.json') as f:
            c = json.loads(f.read())
        self._c = pymongo.MongoClient()[c['mongodb']['db']][c['mongodb']['collection']]

    def put(self, content):
        self._c.insert_one(content)

    def get(self, h):
        return self._c.find_one({'_id': h})
