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

import webpage_utils
import global_value as gl

class TestWebUtils(unittest.TestCase):
    """
    test WebUtils
    """
    def setUp(self):
        self.url = "http://pycm.baidu.com:8081"
        self.url_content = """
<!DOCTYPE html>
<html>
    <head>
        <meta charset=utf8>
        <title>Crawl Me</title>
    </head>
    <body>
        <ul>
            <li><a href=page1.html>page 1</a></li>
            <li><a href="page2.html">page 2</a></li>
            <li><a href='page3.html'>page 3</a></li>
            <li><a href='mirror/index.html'>mirror</a></li>
            <li><a href='javascript:location.href="page4.html"'>page 4</a></li>
        </ul>
    </body>
</html>
"""
        self.parse_url = ['http://pycm.baidu.com:8081/mirror/index.html',
              'http://pycm.baidu.com:8081/page2.html',
              'http://pycm.baidu.com:8081/page1.html',
              'http://pycm.baidu.com:8081/page3.html']

        gl.OUTPUT_DIRECTORY = "./output"
        gl.CRAWL_TIMEOUT = 1
        gl.TARGET_URL = ".*.(htm|html)$"
        self.webpage_tools = webpage_utils.WebUtils()

    def tearDown(self):
        save_name=os.path.join(self.webpage_tools.save_dir, self.url.replace('/', '_'))
        try:
            if os.path.exists(save_name):
                os.remove(save_name)
            if os.path.exists(gl.OUTPUT_DIRECTORY):
                os.removedirs(gl.OUTPUT_DIRECTORY)
        except IOError as ex:
            print "clean output of test error, " + ex

    def test_get_content(self):
        """
        test of WebUtils.get_content(self.url)
        :return:
        """
        str_org = self.webpage_tools.get_content(self.url).strip()
        self.assertEqual(str_org, self.url_content.strip())

    def test_parse_url(self):
        """
        test of WebUtils.parse_url()
        :return:
        """
        parse_ret = self.webpage_tools.parse_url(self.webpage_tools.get_content(self.url), self.url)
        self.assertEqual(parse_ret.sort(), self.parse_url.sort())

if __name__ == '__main__':
    unittest.main()
