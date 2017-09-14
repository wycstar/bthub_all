#!/usr/bin/env python
# coding=utf-8


class Config(object):
    SECRET_KEY = 'asdghtyu'
    WTF_CSRF_SECRET_KEY = 'acf1235'
    WTF_CSRF_ENABLED = True


class OnlineConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True

config = {
    'online': OnlineConfig,
    'development': DevelopmentConfig
}
