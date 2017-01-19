#!/usr/bin/env python
#-*- coding: UTF-8 -*-

"""
This module initialize the logger setting.

Modifier: Light(suliangxd@gmail.com)
Date: 2016/12/28 10:24
"""

import logging
import logging.handlers
import os


class ColoredFormatter(logging.Formatter):
    """
    A colorful formatter to console
    """

    def __init__(self, fmt=None, datefmt=None):
        logging.Formatter.__init__(self, fmt, datefmt)

    def format(self, record):
        """
        return a colorful output in console
        :param record:
        :return:
        """
        COLOR_RESET = '\033[1;0m'
        COLOR_RED = '\033[1;31m'
        COLOR_GREEN = '\033[1;32m'
        COLOR_YELLOW = '\033[1;33m'
        COLOR_BLUE = '\033[1;34m'
        # Define log color
        LOG_COLORS = {
            'DEBUG': COLOR_BLUE + '%s' + COLOR_RESET,
            'INFO': COLOR_GREEN + '%s' + COLOR_RESET,
            'WARNING': COLOR_YELLOW + '%s' + COLOR_RESET,
            'ERROR': COLOR_RED + '%s' + COLOR_RESET,
            'CRITICAL': COLOR_RED + '%s' + COLOR_RESET,
        }
        level_name = record.levelname
        msg = logging.Formatter.format(self, record)
        return LOG_COLORS.get(level_name, '%s') % msg


def init_log(log_path, level=logging.INFO, when="D", backup=7,
             format="[%(levelname)s]: %(asctime)s: %(filename)s:%(lineno)d %(message)s",
             datefmt="%m-%d %H:%M:%S"):
    """
    init_log - initialize log module

    Args:
        log_path      - Log file path prefix.
                        Log data will go to two files: log_path.log and log_path.log.wf
                        Any non-exist parent directories will be created automatically
        level         - msg above the level will be displayed
                        DEBUG < INFO < WARNING < ERROR < CRITICAL
                        the default value is logging.INFO
        when          - how to split the log file by time interval
                        'S' : Seconds
                        'M' : Minutes
                        'H' : Hours
                        'D' : Days
                        'W' : Week day
                        default value: 'D'
        format        - format of the log
                        default format:
                        %(levelname)s: %(asctime)s: %(filename)s:%(lineno)d %(message)s
                        [CRITICAL]: 04-20 16:11:02: mini_spider.py:70 * MainThread test critical
        backup        - how many backup file to keep
                        default value: 7
    Returns:
        Boolean - True for success, False for fail

    Raises:
        OSError: fail to create log directories
        IOError: fail to open log file
    """

    formatter = logging.Formatter(format, datefmt)
    stream_formatter = ColoredFormatter(format, datefmt)
    logger = logging.getLogger()
    logger.setLevel(level)

    dir = os.path.dirname(log_path)
    if not os.path.isdir(dir):
        try:
            os.makedirs(dir)
        except OSError as e:
            logger.error("create log directories error : %s" % e)
            return False

    try:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(stream_formatter)
        logger.addHandler(stream_handler)
    except Exception as e:
        logger.error("stream_handler error : %s" % e)

    try:
        handler = logging.handlers.TimedRotatingFileHandler(log_path + ".log", when=when,
                                                            backupCount=backup)
        handler.setLevel(level)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    except IOError as e:
        logger.error("open log file error : %s" % e)
        return False

    try:
        handler = logging.handlers.TimedRotatingFileHandler(log_path + ".log.wf", when=when,
                                                            backupCount=backup)
        handler.setLevel(logging.WARNING)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    except IOError as e:
        logger.error("open log.wf file error : %s" % e)
        return False
    return True
