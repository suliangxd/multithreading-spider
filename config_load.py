#!/usr/bin/env python
#-*- coding: UTF-8 -*-

"""
This module is used to parse the configuration file

Authors: Light(suliangxd@gmail.com)
Date:    2016/12/28 13:28
"""

import ConfigParser
import logging
import os

import global_value

def conf_parser(conf_file):
    """Parse the conf file
    Call global_value to init global variable.Then cover it.
    Call ConfigParser.ConfigParser to read config info, set global variables.
    Args:
        conf_file: A file with all config info for spider work.
    Returns:
        The status of parser result.
    Raises:
        ValueError: an exception of configParser
    """
    logger = logging.getLogger(__name__)

    if not os.path.exists(conf_file):
        logging.error("Config file %s doesn't exist!" % (conf_file))
        return False
    config = ConfigParser.ConfigParser()
    config.read(conf_file)

    try:
        global_value.URL_LIST_FILE = config.get('spider', 'url_list_file')
        global_value.OUTPUT_DIRECTORY = config.get('spider', 'output_directory')
        global_value.MAX_DEPTH = config.getint('spider', 'max_depth')
        global_value.CRAWL_INTERVAL = config.getfloat('spider', 'crawl_interval')
        global_value.CRAWL_TIMEOUT = config.getfloat('spider', 'crawl_timeout')
        global_value.TARGET_URL = config.get('spider', 'target_url')
        global_value.THREAD_COUNT = config.getint('spider', 'thread_count')
        logging.info("Read global values from %s successfully" % (conf_file))
        # check config is legal
        return check_config()
    except (ValueError, ConfigParser.NoOptionError) as err:
        logger.error("Read global value error, Error message: %s ", err)
        return False


def check_config():
    """
    check config is legal
    """
    if not isinstance(global_value.MAX_DEPTH, int) or global_value.MAX_DEPTH < 0:
        logging.warn("the config of max_depth is illegal.")
        return False
    if not isinstance(global_value.CRAWL_INTERVAL, float) or global_value.CRAWL_INTERVAL < 0:
        logging.warn("the config of crawl_interval is illegal.")
        return False
    if not isinstance(global_value.CRAWL_TIMEOUT, float) or global_value.CRAWL_TIMEOUT < 0:
        logging.warn("the config of crawl_timeout is illegal.")
        return False
    if not isinstance(global_value.THREAD_COUNT, int) or global_value.THREAD_COUNT < 1:
        logging.warn("the config of thread_count is illegal.")
        return False
    if not os.path.exists(global_value.URL_LIST_FILE):
        logging.warn("the url_list_file is not exist.")
        return False
    return True

