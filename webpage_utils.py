#!/usr/bin/env python
#-*- coding: UTF-8 -*-

"""
This module is a webpage parse tools.

Authors: Light(suliangxd@gmail.com)
Date:    2016/12/28 13:28
"""

from bs4 import BeautifulSoup
import contextlib
import chardet
import logging
import os
import re
import time
import urllib
import urllib2
import urlparse

import global_value as gl

def singleton(cls):
    """
    The Singleton function decorator
    """
    instances = {}

    def _singleton(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton


@singleton
class WebUtils(object):
    """
    webpage parse, save tools
    Attributes:
        crawl_timeout: The timeout when open a url.
        save_dir: The directory for url save.
        target_url: The reg match for crawl target.
        url: The url to parse.
    """

    def __init__(self):
        self.__init_save_dir()
        self.crawl_timeout = gl.CRAWL_TIMEOUT
        self.target_url = re.compile(gl.TARGET_URL)

    def __init_save_dir(self):
        """
        initialize the save dir
        """
        if gl.OUTPUT_DIRECTORY.startswith("/"):
            save_dir = gl.OUTPUT_DIRECTORY
        else:
            save_dir = os.path.join(os.getcwd(), gl.OUTPUT_DIRECTORY)

        if not os.path.exists(save_dir):
            logging.warn("save dir don't exits %s, create it" % gl.OUTPUT_DIRECTORY)
            try:
                os.makedirs(save_dir)
            except os.error as err:
                logging.error("mkdir %s error, error message: %s" % (save_dir, err))
                return
        self.save_dir = save_dir

    def __save_url(self, url):
        """
        use urllib.urlretrieve() to save web page
        """
        save_name=os.path.join(self.save_dir, url.replace('/', '_'))
        try:
            urllib.urlretrieve(url, save_name)
            logging.info("saving %s success." % url)
        except IOError as err:
            logging.error("saving %s error. error message: %s" % (url, err))

    def get_content(self, url):
        """
        get the web page's content
        :return: web page content
        """
        if self.target_url.match(url):
            self.__save_url(url)
        else:
            logging.info("url %s not match target_url, do not save." % url)

        try:
            with contextlib.closing(urllib2.urlopen(url, timeout=gl.CRAWL_TIMEOUT)) as res:
                content = res.read()
        except Exception as err:
            logging.error("open url %s error. error message: %s" % (url, err))
            return None

        if res.getcode() != 200:
            time.sleep(gl.CRAWL_INTERVAL)
            return None

        if len(content) == 0:
            return None

        return content

    def parse_url(self, html, url):
        """
        get all links in html
        :param html: html page
        :return: all url list of html
        """
        char_dict = chardet.detect(html)
        web_encoding = char_dict['encoding']
        if web_encoding == 'utf-8' or web_encoding == 'UTF-8':
            content = html
        else:
            try:
                content = html.decode('GBK', 'ignore').encode('utf-8')
            except UnicodeDecodeError as err:
                logging.error("decode html error. error message: %s.", err)
                return None
        page_links = []
        base_url = url.strip('/ ')
        try:
            urls = BeautifulSoup(content, "lxml").findAll('a', href=True)
            imgs = BeautifulSoup(content, "lxml").findAll('img', src=True)
        except TypeError as msg:
            logging.error("type error! error message: %s" % msg)
            return page_links
        except UnicodeDecodeError as msg:
            logging.error("unicode decode error! error message: %s" % msg)
            return page_links

        links_set = set()
        for link in urls:
            if not link['href'].startswith('javascript:'):
                links_set.add(link['href'])
        for link in imgs:
            links_set.add(link['src'])
        for link in links_set:
            if not link.startswith('http'):
                try:
                    page_links.append(urlparse.urljoin(base_url, link.strip('/ ')))
                except UnicodeDecodeError as msg:
                    logging.error('url parse error. error message: %s' % msg)
            else:
                page_links.append(link.strip('/ '))
        return page_links
