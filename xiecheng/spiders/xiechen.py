# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector,Selector
from xiecheng.items import XiechengItem
from scrapy import log
from scrapy.http import FormRequest,Request
import requests
import json
import pprint
import re


class XiechenSpider(scrapy.Spider):
    name = "xiecheng"
    allowed_domains = ["hotels.ctrip.com"]
    start_urls = [
        'http://hotels.ctrip.com/domestic-city-hotel.html',
    ]
    #抓取全国酒店url
    def parse(self, response):
        sel=Selector(response)
        cate_dress=sel.xpath("//dl[@class='pinyin_filter_detail layoutfix']//a/@href").extract()
        #调试使用
        for i in cate_dress[:3]:
            cate_url='http://hotels.ctrip.com' + str(i)
            req=Request(cate_url,callback=self.page_u)
            yield req
    #地方酒店的每页url
    def page_u(self,response):
        sel=Selector(response)
        total_p=int(sel.xpath("//div[@id='page_info']//a/text()").extract()[-2])
        for i in range(1,(total_p+1))[:2]:
            page_url=response.url + '/p' + str(i)
            req=Request(page_url,callback=self.hotel_u)
            yield req
    #酒店的url
    def hotel_u(self,response):
        sel=Selector(response)

        # log.msg('This is the hotel_url:%s' % response.url)
        cate_u=sel.xpath("//div[@class='searchresult_list ']//h2[@class='searchresult_name']/a/@href").extract()[:-1]
        cate_u_ctm=sel.xpath("//div[@class='searchresult_list ']//h2[@class='searchresult_name']/a/@data-ctm").extract()[:-1]
        print '***************',cate_u,cate_u_ctm
        # for i,j in cate_u,cate_u_ctm:
        #     cate_url='http://hotels.ctrip.com' +str(i) +str(j)
        #     print '*************',cate_url

    #
    #      # pass
