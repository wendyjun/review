# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector,Selector
from taijipanda.items import TaijipandaItem
from scrapy.http import FormRequest,Request
import json
import requests
from bs4 import BeautifulSoup
import pprint

class TaijipandaPipeline(CrawlSpider):
    name = "panda"
    allowed_domains = ["tieba.baidu.com"]
    start_urls = [
        'http://tieba.baidu.com/f?ie=utf-8&kw='+'%E5%A4%AA%E6%9E%81%E7%86%8A%E7%8C%AB'
         ]
    #每页的url
    def parse(self, response):
        sel=Selector(response)
        total_page=sel.xpath("//div[@id ='frs_list_pager']/a/@href").extract()[-1].split("=")[-1]
        # print '******98150********',total_page
        #获取每页的url
        total=int(total_page)/50
        # print '++++++++++',total,type(total)
        for i in range(total)[:2]:
            if i>total:
                break
            else:
                cate=sel.xpath(("//div[@id='frs_list_pager']/a/@href")).extract()[0].split('=')[:-1]
                # print '********************',cate
                cate_url='='.join(cate)+ '=' + str(i*50)
                # print '********cate_url*******',cate_url
                req=Request(cate_url,callback=self.cate_url_all)
                yield req

    def cate_url_all(self,response):
        sel=Selector(response)
        first_u=sel.xpath("//dl[@id='threadListGroupCnt']/dt/span/a/@href").extract()[0]
        total=[]
        total.append(str(first_u))
        #++++++++++首页精品区待处理++++++++++++
        middle=sel.xpath("//ul[@id='thread_top_list']/li//div/a/@href").extract()[1:6:2]
        middle1_u='http://tieba.baidu.com' + str(middle[0])
        middle2_u='http://tieba.baidu.com' + str(middle[1])
        middle3_u='http://tieba.baidu.com' + str(middle[2])
        print '..................',middle1_u,middle2_u
        # middle1_u='http://tieba.baidu.com' + str(middle[0])
        #IndexError: list index out of range
        total.append(middle1_u)
        total.append(middle2_u)
        total.append(middle3_u)

        normal_u=sel.xpath("//li[@class=' j_thread_list clearfix']//div/a/@href").extract()
        #测试用部分
        for i in normal_u[:3]:
            if len(i)<10:
                pass
            else:
                normal_url='http://tieba.baidu.com' + str(i)
                total.append(normal_url)
                # print '----------------------',type(first_u),type(normal_url),total
                for i in total:
                    req=Request(i,callback=self.detail_p)
                    yield req
    #每贴的页码url
    def detail_p(self,response):
        sel=Selector(response)
        total_p=sel.xpath("//li[@class='l_reply_num']/span/text()").extract()[1]
        # print '+++++++++++++++++++',total_p
        if int(total_p)==1:
            page_url=response.url
            print '**************',page_url
        else:
              for i in range(1,int(total_p)+1):
                  page_url=response.url + '?pn=' + str(i)
                  print '++++++++++++++++++',page_url
                  req=Request(page_url,callback=self.url_mess)
                  yield req
    #
    def url_mess(self,response):
        sel=Selector(response)







        # pass
