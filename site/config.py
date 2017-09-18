#!/usr/bin/env python
# coding=utf-8


class Config(object):
    pass


class OnlineConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True

config = {
    'online': OnlineConfig,
    'development': DevelopmentConfig
}
