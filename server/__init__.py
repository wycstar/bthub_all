#!/usr/bin/env python
# -*-coding:utf-8 -*-

from flask import Flask
from model import SearchManager
from config import config
from flask_socketio import SocketIO

# __all__ = ['SearchManager']

SITE = Flask(__name__)
SITE.config.from_object(config['development'])
SERVER = SocketIO(SITE, async_mode='eventlet')
ELASTIC = SearchManager()
from view import *
