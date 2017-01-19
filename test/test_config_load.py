#!/usr/bin/env python
#-*- coding: UTF-8 -*-

"""
This module is to set global variables for spider program to use.

Author: Light(suliangxd@gmail.com)
Date: 2016/12/28 13:28:57
"""
import os
import unittest
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import config_load
import global_value as gl

class TestConfigLoad(unittest.TestCase):
    """
    test of config load
    """
    def setUp(self):
        self.conf_file = "test_spider.conf"
        conf_content = "[spider]\n"\
                       "url_list_file: ../urls ; 种子文件路径\n"\
                       "output_directory: ./output ; 抓取结果存储目录\n"\
                       "max_depth: 2 ; 最大抓取深度(种子为0级)\n"\
                       "crawl_interval: 1 ; 抓取间隔. 单位: 秒\n"\
                       "crawl_timeout: 1 ; 抓取超时. 单位: 秒\n"\
                       "target_url: .*.(htm|html)$ ; 需要存储的目标网页URL pattern(正则表达式)\n"\
                       "thread_count: 8 ; 抓取线程数"

        try:
            with open(self.conf_file, "w") as f:
                f.write(conf_content)
        except IOError as msg:
            print "open conf_file to write error. error message: %s" % msg

    def tearDown(self):
        try:
            if os.path.exists(self.conf_file):
                os.remove(self.conf_file)
        except IOError as msg:
            print "clear conf_file error. error messsage: %s" % msg

    def test_conf_parser(self):
        """
        test config_load.conf_parser
        """
        conf_ret = config_load.conf_parser(self.conf_file)
        self.assertEqual(conf_ret, True)
        self.assertEqual(gl.URL_LIST_FILE, "../urls")
        self.assertEqual(gl.OUTPUT_DIRECTORY, "./output")
        self.assertEqual(gl.MAX_DEPTH, 2)
        self.assertEqual(gl.CRAWL_INTERVAL, 1)
        self.assertEqual(gl.CRAWL_TIMEOUT, 1)
        self.assertEqual(gl.TARGET_URL, ".*.(htm|html)$")
        self.assertEqual(gl.THREAD_COUNT, 8)

if __name__ == '__main__':
    unittest.main()
