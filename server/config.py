#!/usr/bin/env python
# coding=utf-8

import sys
import os
import json


class Config(object):
    real_path = os.path.split(os.path.realpath(sys.argv[0]))[0]
    with open(real_path + os.sep + 'config.json') as f:
        c = json.loads(f.read())
    SECRET_KEY = 'asdghtyu'
    WTF_CSRF_SECRET_KEY = 'acf1235'
    WTF_CSRF_ENABLED = True
    DOMAIN = c['domain']
    COMPRESS_MIMETYPES = ['text/html', 'text/css', 'text/xml', 'application/json', 'application/javascript']
    COMPRESS_LEVEL = 6
    COMPRESS_MIN_SIZE = 500


class OnlineConfig(Config):
    DEBUG = True


class DevelopmentConfig(Config):
    DEBUG = True

config = {
    'online': OnlineConfig,
    'development': DevelopmentConfig
}
