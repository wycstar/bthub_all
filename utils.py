#!/usr/bin/env python
# coding:utf-8
import math


def convert_readable_size(x):
    label = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB']
    m = math.floor(math.log(x, 2) / 10)
    t = divmod(x, 2 ** (m * 10))
    return '%.1f%s' % ((t[0] + t[1] / (1024 ** m)), label[int(m)])
