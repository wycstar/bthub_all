#!/usr/bin/env python
# -*-coding:utf-8-*-

import time

def perfmon(f):
    def wrapper(*args, **kwargs):
        begin = time.time()
        f(*args, **kwargs)
        print time.time() - begin
    return wrapper
