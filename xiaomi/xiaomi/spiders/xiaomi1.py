# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector,Selector
from xiaomi.items import XiaomiGameUrlItem
from scrapy import log
from scrapy.http import FormRequest,Request
import requests
import json
import pprint




class Xiaomi1Spider(CrawlSpider):
    name = "xiaomi"
    allowed_domains = ["xiaomi.com"]
    start_urls = [
        'http://game.xiaomi.com/category-categoryappmore--category_id__2000016.html'
        ]

    def parse(self, response):
        sel=Selector(response)
        cate_game=sel.xpath("//div[@class='category-box']//li/a/@data").extract()
        for cate_u in cate_game[:1]:
            cate_game_url=cate_u
            req=Request(cate_game_url,callback=self.get_game)
            yield req
    #抓取分类页码
    def get_game(self,response):
        # print '========category url is:',response.url
        sel=Selector(response)
        total_page = int(sel.xpath("//input[@id='total_page']/@value").extract()[0])
        for i in range(0,total_page+1)[:1]:
            cate=response.url.split("id__")[1].split(".")[0]
            data={'page':i,'category_id':cate,'total_page':total_page}
            cate_url="http://game.xiaomi.com/index.php?c=category&a=ajaxPage&category_id=" +str(cate)
            print '+++++++++++cate_url',cate_url
            r =requests.post(cate_url,data=data)
            #把字符串转换成字典
            game_url_message = json.loads(r.text)
            # pprint.pprint(game_url_message)
            for game in game_url_message:
                game_id= game['ext_id']
                game_url = "http://game.xiaomi.com/app-appdetail--app_id__" + str(game_id)+ ".html"
                print '------------game_url',game_url
                req=Request(game_url,callback=self.game_detail)
                yield req

        # total_page = int(sel.xpath("//input[@id='total_page']/@value").extract()[0])
        # for i in range(0,total_page+1):
        #     cate = response.url.split("id__")[1].split(".")[0]
        #     data = {"page":i,"category_id":cate,"total_page":total_page}
        #     cate_url = 'http://game.xiaomi.com/index.php?c=category&a=ajaxPage&category_id=' + str(cate)
        #     print cate_url
        #     r = requests.post(cate_url,data=data)
        #     game_url_message =  json.loads(r.text)
        #     # pprint.pprint(game_url_message)
        #     for game in game_url_message:
        #         game_id = game["ext_id"]
        #         game_url = 'http://game.xiaomi.com/app-appdetail--app_id__' + str(game_id) + '.html'
        #         print game_url
    #             req=Request(game_url,callback=self.game_detail)
    #             yield req



    def game_detail(self,response):
        print '22222222222',response.url
        sel=Selector(response)

        game=XiaomiGameUrlItem()
        game['game_name']=sel.xpath("//div[@class='info-words']/h1/text()").extract()[0].strip()
        # print '3333333333333333333',game['game_name']
        game['game_type_name']=sel.xpath("//div[@class='tip']/a/text()").extract()[-1].strip()

        game['game_size']=sel.xpath("//div[@class='info-words']/p/text()").extract()[0].split("|")[-1]
        print '3333333333333333',game['game_size']
        game['game_load_number']=sel.xpath("//div[@class='info-words']/p/text()").extract()[0].split("|")[0]
        print '4444444444444444',game['game_load_number']
        game['game_owner']=sel.xpath("//ul[@class='baseinfo']//li//h4/text()").extract()[1].strip()
        print '5555555555555',game['game_owner']
        game['game_time']=sel.xpath("//ul[@class='baseinfo']//li//h4/text()").extract()[3].strip()
        print '666666666666666',game['game_time']
        game['game_content']=''.join(sel.xpath("//p[@class='pslide']/text()").extract()[:])
        print '777777777777777',game['game_content']


        return game
