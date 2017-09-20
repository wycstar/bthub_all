#!/usr/bin/env python
# -*-coding:utf-8 -*-

from flask import Flask
from model import SearchManager
from config import config
from flask_socketio import SocketIO
import eventlet


SITE = Flask(__name__)
SITE.config.from_object(config['development'])
eventlet.monkey_patch()
SERVER = SocketIO(SITE, async_mode='eventlet', message_queue='redis://localhost:6379/1')
ELASTIC = SearchManager()
from view import *
