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
        self._url = 'http://localhost:9200/bt'
        if requests.put(self._url).status_code != 200:
            pass
        if requests.post(self._url + '/fulltext/_mapping',
                         data=json.dumps(self._config_json.get('search').get('mapping')),
                         headers={'Content-type': 'application/json'}) != 200:
            pass

    def search(self, keyword):
        search_format = {
            "query": {
                "match": {
                    "n": {
                        "query": keyword
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
        r = requests.post(self._url + '/_search',
                          data=json.dumps(search_format),
                          headers={'Content-type': 'application/json'})
        print r.content


if __name__ == '__main__':
    s = SearchManager()
    s.search('东京')
