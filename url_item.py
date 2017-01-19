#!/usr/bin/env python
#-*- coding: UTF-8 -*-

"""
This module is a url object

Authors: Light(suliangxd@gmail.com)
Date:    2016/12/28 13:28
"""

class UrlItem(object):
    """
    A Url object with url_link and depth.
    Attributs:
        url: A pure url link.
        depth: A number to identify how deep when spider a url, default is 0.
    """
    def __init__(self, url, depth=0):
        self.url = url
        self.depth = depth

    def __eq__(self, other):
        if isinstance(other, UrlItem):
            return self.url == other.url and self.depth == other.depth
        return object.__eq__(self, other)
