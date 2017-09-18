#!/usr/bin/env python
# coding=utf-8

from flask import Flask
from config import config

website = Flask(__name__)
website.config.from_object(config['development'])
from view import *
