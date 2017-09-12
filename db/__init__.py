#!/usr/bin/env python
# -*-coding:utf-8 -*-

from multiprocessing import Manager
from mongo import MongoManager
from cedis import RedisManager
from multiprocessing import Process, Manager

HASH_QUEUE = Manager().Queue()
MONGO = MongoManager()
REDIS = RedisManager()


class DataProcess(Process):
    def __init__(self):
        Process.__init__(self)

    def run(self):
        while True:
            a = HASH_QUEUE.get()
            print a
