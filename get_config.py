"""
-------------------------------------------------
   File Name：     GetConfig.py
   Description :   获取配置信息
   Author :        Cyrus_Ren
   date：          2018/12/10
-------------------------------------------------
   Change Activity:
                   
-------------------------------------------------
"""
__author__ = 'Cyrus_Ren'

import os
import configparser


class LazyProperty(object):
    """
    LazyProperty
    explain: http://www.spiderpy.cn/blog/5/
    """

    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance, self.func.__name__, value)
            return value


class GetConfig(object):
    """
    to get config from config.ini
    """

    def __init__(self):
        self.conf = configparser.ConfigParser()
        self.conf.read('./config.ini', encoding='UTF-8')

    @LazyProperty
    def crawl_is_download(self):
        return self.conf.get('crawl', 'isDownloadFile')

    @LazyProperty
    def crawl_is_crack_code(self):
        return self.conf.get('crawl', 'isCrackCode')

    @LazyProperty
    def crawl_user_agent(self):
        return self.conf.get('crawl', 'userAgent')

    @LazyProperty
    def crawl_step_wait_time(self):
        return int(self.conf.get('crawl', 'stepWaitTime'))

    @LazyProperty
    def crawl_is_downLoad_link(self):
        return self.conf.get('crawl', 'isDownLoadLink')

    @LazyProperty
    def crawl_common_headers(self):
        return {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Pragma': 'no-cache',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': self.crawl_user_agent,
        }


config = GetConfig()
