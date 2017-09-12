#!/usr/bin/env python
# -*-coding:utf-8 -*-

from spider import Master
from spider import DHTServer
from db import DataProcess


if __name__ == '__main__':
    q = DataProcess()
    q.start()
    master = Master()
    master.start()
    dht = DHTServer(master, "0.0.0.0", 6881, max_node_qsize=200)
    dht.start()
    dht.auto_send_find_node()
    q.join()
