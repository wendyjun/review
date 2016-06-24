# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb

class TaijipandaPipeline(object):
    def __init__(self):
        self.conn=MySQLdb.connect(
                host='localhost',
                port = 3306,
                user='root',
                passwd=' ',
                db ='mysql',
                charset='utf8'
                )
    def process_item(self, item, spider):
        cur=self.conn.cursor()
        sql="""INSERT INTO pandar(name,time,comment) VALUES (%s','%s','%s')""" % (
                           item['name'].encode('utf8'),
                           item['time'].encode('utf8'),
                           item['comment'].encode('utf8')
                           )
        cur.execute(sql)
        self.conn.commit()
        cur.close()

        return item