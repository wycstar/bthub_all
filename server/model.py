#!/usr/bin/env python
# coding:utf-8

import requests
import json
import os
import sys
from tools import convert_readable_size
from db import REDIS

'''
type:
0: 相关性正序
1: 相关性逆序
2: 访问时间正序
3: 访问时间逆序
4: 文件大小正序
5: 文件大小逆序
6: 文件数正序
7: 文件数逆序
8: 下载量正序
9: 下载量逆序
'''
SEARCH_TYPE = {}
SEARCH_TYPE['heatasc']  = {"sort": [{"c": "asc"}]}
SEARCH_TYPE['heatdesc'] = {"sort": [{"c": "desc"}]}
SEARCH_TYPE['atimeasc']  = {"sort": [{"m": "asc"}]}
SEARCH_TYPE['atimedesc'] = {"sort": [{"m": "desc"}]}
SEARCH_TYPE['ctimeasc']  = {"sort": [{"d": "asc"}]}
SEARCH_TYPE['ctimedesc'] = {"sort": [{"d": "desc"}]}
SEARCH_TYPE['fileasc']  = {"sort": [{"s": "asc"}]}
SEARCH_TYPE['filedesc'] = {"sort": [{"s": "desc"}]}
SEARCH_TYPE['sizeasc']  = {"sort": [{"l": "asc"}]}
SEARCH_TYPE['sizedesc'] = {"sort": [{"l": "desc"}]}


class SearchManager(object):
    def __init__(self):
        self._real_path = os.path.split(os.path.realpath(sys.argv[0]))[0]
        with open(self._real_path + os.sep + 'config.json') as f:
            self._config_json = json.loads(f.read())
        self._url = 'http://localhost:9200/' + self._config_json['mongodb']['db'] + '/_search'

    def _convert(self, f, all=False):
        n = []
        s = 0
        q = sorted(f, key=lambda k:k['l'], reverse=True)
        for x in q:
            s += x.get('l')
            b = x.get('n').strip()
            n.append({
                'n': b if b != '' else 'UNNAMED',
                'l': convert_readable_size(x.get('l'))
            })
        return n if all else n[:10], convert_readable_size(s)

    def analyze(self, text):
        search_format = {
            "analyzer": "ik_smart",
            "text": text
        }
        r = requests.post('http://localhost:9200/_analyze',
                          data=json.dumps(search_format),
                          headers={'Content-type': 'application/json'}).content
        d = json.loads(r)
        return sorted(map(lambda x: x.get('token'), d.get('tokens')), key=lambda k:len(k))

    def search(self, keyword, page, sort=0, order=0):
        k = []
        search_format = {
            "from": (page - 1) * 10,
            "size": 10,
            "query": {
                "match": {
                    "n": {
                        "query": keyword,
                        "operator": "and"
                    }
                }
            },
            "highlight": {
                "pre_tags": ["<em>"],
                "post_tags": ["</em>"],
                "fields": {
                    "n": {}
                }
            }
        }
        # search_format.update(SEARCH_TYPE[sort + '+' + 'oder'])
        try:
            print SEARCH_TYPE.get(sort + order)
        except:
            pass
        r = requests.post(self._url,
                          data=json.dumps(search_format),
                          headers={'Content-type': 'application/json'}).content
        j = json.loads(r)
        for x in j.get('hits').get('hits'):
            a = x.get('_source')
            r = self._convert(a.get('f'))
            k.append({
                'name':x.get('highlight').get('n')[0],
                'ctime': a.get('d'),
                'files': r[0],
                'size': r[1],
                'num': len(r[0]),
                'mag': 'magnet:?xt=urn:btih:' + x.get('_id'),
                'url': 'http://fycx.mynetgear.com:28000/hash/' + x.get('_id')
            })
        return {
            'total': j.get('hits').get('total'),
            'took': j.get('took') / 1000.0,
            'result': k
        }
