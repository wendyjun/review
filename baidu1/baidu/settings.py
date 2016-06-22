#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Scrapy settings for baidu project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'baidu'

SPIDER_MODULES = ['baidu.spiders']
NEWSPIDER_MODULE = 'baidu.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'baidu (+http://www.yourdomain.com)'
DOWNLOAD_DELAY = 1.0
#同时请求数
#default :16
CONCURRENT_REQUESTS = 10


# 结果ITEM通过PIPE
ITEM_PIPELINES = {
    'baidu.pipelines.BaiduPipeline':800,

}


#日志的设置
LOG_ENABLED = True
LOG_ENCODING = 'utf-8'
LOG_FILE = './baidu.log'
LOG_LEVEL = 'DEBUG'
LOG_STDOUT = True
