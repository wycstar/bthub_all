#!/usr/bin/env python
# coding:utf-8

import requests
import json
import os
import sys

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
SEARCH_TYPE = []
SEARCH_TYPE[0] = {
    "sort": [
        {"_score": "asc"}
    ]
}
SEARCH_TYPE[1] = {
    "sort": [
        {"_score": "desc"}
    ]
}
SEARCH_TYPE[2] = {
    "sort": [
        {"m": "asc"}
    ]
}
SEARCH_TYPE[3] = {
    "sort": [
        {"m": "desc"}
    ]
}
SEARCH_TYPE[4] = {
    "sort": [
        {"l": "asc"}
    ]
}
SEARCH_TYPE[5] = {
    "sort": [
        {"l": "desc"}
    ]
}
SEARCH_TYPE[6] = {
    "sort": [
        {"s": "asc"}
    ]
}
SEARCH_TYPE[7] = {
    "sort": [
        {"s": "desc"}
    ]
}
SEARCH_TYPE[8] = {
    "sort": [
        {"c": "asc"}
    ]
}
SEARCH_TYPE[9] = {
    "sort": [
        {"c": "desc"}
    ]
}


class SearchManager(object):
    def __init__(self):
        self._real_path = os.path.split(os.path.realpath(sys.argv[0]))[0]
        with open(self._real_path + os.sep + 'config.json') as f:
            self._config_json = json.loads(f.read())
        self._url = 'http://localhost:9200/' + self._config_json['db']

    def search(self, keyword, page, sort=0):
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
        search_format.update(SEARCH_TYPE[sort])
        r = requests.post(self._url + '/_search',
                          data=json.dumps(search_format),
                          headers={'Content-type': 'application/json'}).content
        for x in r.get('hits').get('hits'):
            k.append(x.get('_source'))
        return {
            'total': r.get('hits').get('total'),
            'took': r.get('took'),
            'result': k
        }


if __name__ == '__main__':
    s = SearchManager()
    s.search('东京', 1)
