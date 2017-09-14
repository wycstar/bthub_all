#!/usr/bin/env python
# -*-coding:utf-8 -*-

from cedis import RedisManager
from mongo import MongoManager
from utils import parse_metadata
from multiprocessing import Process, Manager
from bson.errors import InvalidStringData

HASH_QUEUE = Manager().Queue()
MONGO = MongoManager()
REDIS = RedisManager()

__all__ = ['MongoManager', 'RedisManager', 'get_file_type', 'DataProcess']


class DataProcess(Process):
    def __init__(self):
        Process.__init__(self)

    def run(self):
        while True:
            a = HASH_QUEUE.get()
            tid = a.get('_id')
            try:
                MONGO.put(a)
            except InvalidStringData:
                continue
            REDIS.put(tid)
