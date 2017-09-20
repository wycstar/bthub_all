#!/usr/bin/env python
# -*-coding:utf-8 -*-

from cedis import RedisManager
from mongo import MongoManager
from utils import parse_metadata
from multiprocessing import Process, Manager
from bson.errors import InvalidStringData
from apscheduler.schedulers.background import BackgroundScheduler


HASH_QUEUE = Manager().Queue()
MONGO = MongoManager()
REDIS = RedisManager()

__all__ = ['MongoManager', 'RedisManager', 'get_file_type', 'DataProcess']


class DataProcess(Process):
    def __init__(self):
        Process.__init__(self)
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(DataProcess.manage_popular_search, trigger='cron', hour='0', minute='0')  # 每天都分析热搜
        self.scheduler.add_job(DataProcess.push_recent_search, trigger='interval', seconds=3)

    # 分析并清理热搜
    @staticmethod
    def manage_popular_search():
        REDIS.clean_fresh()

    @staticmethod
    def push_recent_search():
        from server import SERVER
        f = REDIS.get_fresh()[:10]
        SERVER.emit('update', f, broadcast=True)

    # 从队列里取出种子的meta信息并存储
    def run(self):
        self.scheduler.start()
        while True:
            import time
            time.sleep(1)
            # a = HASH_QUEUE.get()
            # tid = a.get('_id')
            # try:
            #     MONGO.put(a)
            # except InvalidStringData:
            #     continue
            # REDIS.put_heat(tid)
