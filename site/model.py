#!/usr/bin/env python
# coding:utf-8

import requests
import json
import os
import sys


class SearchManager(object):
    def __init__(self):
        self._real_path = os.path.split(os.path.realpath(sys.argv[0]))[0]
        with open(self._real_path + os.sep + 'config.json') as f:
            self._config_json = json.loads(f.read())
        self._url = 'http://localhost:9200/' + self._config_json['db']

    # type:
    # 1: relative asc
    # 2: relatice dec
    # 3: ctime asc
    # 4: ctime dec
    # 5: size asc
    # 6: size dec
    # 7: files asc
    # 8: files dec
    def search(self, keyword, page, sort=1):
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
            },
            "sort": {[
                {"_score":"asc"}
            ]}
        }
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
