#!/usr/bin/env python
# -*-coding:utf-8 -*-

from flask import Flask
from model import SearchManager
from config import config

# __all__ = ['SearchManager']

SITE = Flask(__name__)
SITE.config.from_object(config['development'])
ELASTIC = SearchManager()
from view import *
