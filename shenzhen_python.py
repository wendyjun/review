# -*- coding: utf-8 -*-
import MySQLdb
import requests
import json

class Lagou(object):
    def __init__(self):
        self.conn=MySQLdb.connect(
                host='localhost',
                port = 3306,
                user='root',
                passwd=' ',
                db ='mysql',
                charset='utf8'
                )
    def message_get(self):
        data = {
            'first': 'false',
            'pn': '1',
            'kd': 'Python'
        }
        r = requests.post(
            'http://www.lagou.com/jobs/positionAjax.json?city=%E6%B7%B1%E5%9C%B3&needAddtionalResult=false',
            data=data
        )
        #把response 转换成字典的形式，然后进行取值
        message_page = json.loads(r.text)
        total_p = message_page['content']['positionResult']['totalCount']

        #确定页码的准确数字
        if  int(total_p) / 15 < float(total_p) / 15:
            cate_p = int(total_p) / 15  + 1
        else:
            cate_p = int(total_p) / 15
            print '**********', total_p, cate_p

        #对每一页以post请求，获得每页字典形式的信息
        for i in range(1,cate_p + 1):
            data = {
                'first': 'false',
                'pn': i,
                'kd': 'Python'
            }
            rel = requests.post(
                'http://www.lagou.com/jobs/positionAjax.json?city=%E6%B7%B1%E5%9C%B3&needAddtionalResult=false',
                data = data
            )
            cate_message = json.loads(rel.text)
            each_message = cate_message['content']['positionResult']['result']
            # print '*******',each_message

            for j in each_message:
                message={}

                message['company'] = j['companyFullName']
                message['salary'] = j['salary']
                message['time'] = j['createTime']
                #print '+++++++++++',message['company'],message['salary'],message['time']
                self.sql_insert(message)





    def sql_insert(self,item):
        cur=self.conn.cursor()
        sql ="""INSERT INTO pythonsz(company,salary,time) VALUES ('%s','%s','%s')""" % (

                           item['company'].encode('utf8'),
                           item['salary'].encode('utf8'),
                           item['time'].encode('utf8'),

                            )
        cur.execute(sql)
        self.conn.commit()
        cur.close()




if __name__ == "__main__":
    Lagou().message_get()