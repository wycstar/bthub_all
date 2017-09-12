#!/usr/bin/env python
# -*- coding:utf-8 -*-

from math import log, floor
from time import localtime, strftime
import sys
import pymongo
import time

MDBClient = pymongo.MongoClient()
MDBCollection = MDBClient['dht']
MDB = MDBCollection.hashSet
HASH_INDEX = MDB.count()
CREATE_TIME = time.strftime("%Y-%m-%d")

def readableFileSize(x):
    label = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB']
    m = floor(log(x, 2) / 10)
    t = divmod(x, 2 ** (m * 10))
    return '%.1f%s' % ((t[0] + t[1] / (1024 ** m)), label[int(m)])

def storeMetaData(metadata, infohash):
    global HASH_INDEX
    HASH_INDEX += 1
    print 'insert'
    files = []
    if 'files' in metadata:
        for x in metadata.get('files'):
            length = x.get('length')
            files.append({'name': '/'.join(x.get('path')),
                          'length': length,
                          'human_length': readableFileSize(length)})
    else:
        length = metadata.get('length')
        files.append({'name': metadata.get('name'),
                      'length': length,
                      'human_length': readableFileSize(length)})
    for x in files:
        print 'name: %s  size:%s' % (x.get('name'), x.get('human_length'))
    MDB.update({'infohash': infohash},
               {'$setOnInsert': {
                   'id': HASH_INDEX,
                   'create_date': CREATE_TIME,
                   'store_date': CREATE_TIME,
                   'name': metadata.get('name'),
                   'files': files,
                   'file_num': len(files),
                   'total_length': readableFileSize(sum([x.get('length') for x in files]))},
                '$inc': {'count': 1}},
               upsert=True)

if __name__ == "__main__":
    print(readableFileSize(int(sys.argv[1])))

