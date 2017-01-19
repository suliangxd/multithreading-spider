#!/usr/bin/env python
#-*- coding: UTF-8 -*-

"""
This module is to set global variables for spider program to use.

Author: Light(suliangxd@gmail.com)
Date: 2016/12/28 13:28
"""
import Queue
import threading

# global variables
URL_LIST_FILE=''
OUTPUT_DIRECTORY=''
MAX_DEPTH=''
CRAWL_INTERVAL=0
CRAWL_TIMEOUT=0
TARGET_URL=''
THREAD_COUNT=0

LOCK = threading.Lock()
URL_QUEUE = Queue.Queue()
CRAWED_URLS = set()
