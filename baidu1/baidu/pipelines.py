#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy import log
# import beanstalkc
import json
import MySQLdb

class BaiduPipeline(object):
    def __init__(self):
       self.conn = MySQLdb.connect(
                        host='localhost',
                        port = 3306,
                        user='root',
                        passwd=' ',
                        db ='mysql',
                        charset='utf8'
                        )

    def process_item(self, item, spider):
        #数据库
        cur = self.conn.cursor()
        sql = """INSERT INTO baidu(game_name, game_type_name, game_id )
                        VALUES('%s', '%s', '%s')
                    """ % (
                           item['game_name'].encode('utf8'),
                           item['game_type_name'].encode('utf8'),
                           item['game_id'].encode('utf8'),
                           )
        cur.execute(sql)
        self.conn.commit()
        cur.close()

        return item
