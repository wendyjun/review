#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#  tanyewei@gmail.com
#  2014/01/16 14:55
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector,Selector
from baidu.items import BaiduGameUrlItem
# from scrapy import log
import time

#HTTP请求
from scrapy.http import FormRequest,Request

import re
import pprint

class AppstoreSpider(CrawlSpider):
    name = 'baidu'
    allowed_domains = ["baidu.com"]
    #
    start_urls = [
                "http://as.baidu.com/a/asgame?f=web_alad%40next%40rank_3000_1",
                  ]

    def parse(self,response):
        # log.msg("dkfjkjkdsjfksjdkfj")
        # print '========================',response.url
        sel = Selector(response)
        cate_url = sel.xpath("//ul[@class='cate']//div/a/@href").extract()
       # for cate in cate_url:
        for cate in cate_url:  #测试
            cate_u = 'http://shouji.baidu.com' + cate
            # print '++++++++++++++++++++++++',cate_u
            req = Request(cate_u,callback=self.get_game_page)
            yield req
    def get_game_page(self,response):
        # print '---game page---'
        # print '@@@@@@@@@@@@@@@@@',response.url
        sel = Selector(response)
        # print '000000000',sel
        cate_game_page=sel.xpath("//div[@class='pager']//a/@href").extract()
        # for game_page in cate_game_page:
        for game_page in cate_game_page:  #测试
            page_url= response.url + game_page
            # print '1111111111',page_url
            req = Request(page_url,callback=self.cate_game)
            yield req

    def cate_game(self,response):
        # print '----------------',response.url
        sel=Selector(response)
        cate_game_url=sel.xpath("//div[@class='list-bd app-bd']//a/@href").extract()
        for cate_game in cate_game_url[:1]:
            game_url0= 'http://shouji.baidu.com' + cate_game
            req = Request(game_url0,callback=self.game_get)
            yield req
    def game_get(self,reponse):
        sel = Selector(reponse)
        game= BaiduGameUrlItem()

        game['game_url']=reponse.url

        game['game_today'] =time.ctime()
        game['game_type_name']=sel.xpath("//div[@class='nav']//a/text()").extract()[-1].strip()
        game['game_name']=sel.xpath("//div[@class='content-right']/h1/span/text()").extract()[0].strip()
        game['game_id'] = sel.xpath("//span[@class='res-tag-ok']/text()").extract()[0].strip()
        game['game_download_times'] = sel.xpath("//span[@class='download-num']/text()").extract()[0].strip()
        game['game_size']=sel.xpath("//span[@class='size']/text()").extract()[0].strip()
        game['game_content']=sel.xpath("//div[@class='brief-long']/p/text()").extract()[-1].strip()
        return game


