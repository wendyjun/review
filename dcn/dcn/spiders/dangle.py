# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector,Selector
from dcn.items import DcnItem
from scrapy.http import FormRequest,Request
import json
import requests
from bs4 import BeautifulSoup
import pprint

class DcnPipeline(CrawlSpider):
    name = "dcn"
    allowed_domains = ["ng.d.cn"]
    start_urls = ['http://ng.d.cn/channel/list_0_0_0_0_0_0_1_0.html?sort=0&keyword=']
    header={
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'en-US,en;q=0.8',
        'Connection':'keep-alive',
        'Host':'ng.d.cn',
        'Referer':'http://ng.d.cn/channel/list_0_3_0_0_0_0_3_0.html?sort=0&searchByEs=1&keyword=',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36'
    }
    def parse(self, response,headers=header):
        # print '************',response.url
        sel= Selector(response)
        cate_url=sel.xpath("//div[@class='sortBox clearfix']//a/@href").extract()
        print '000000000000000000',pprint.pprint(cate_url)
        for cate_u in cate_url[:9]:
            cate_game_url='http://ng.d.cn/' +''.join(cate_u.split("./")[1:])
            print '+++++++++++cate_url*******',cate_game_url
            req = Request(cate_game_url,callback=self.game_page)
            yield req

    def game_page(self,response):
        # print '************',response.url
        cate=(response.url).split('_')[2]
        # print '**********cate***************',cate
        for j in cate:
            for i in range(1,100):
                cate_url='http://ng.d.cn/channel/list_0_' + str(j) +'_0_0_0_0_' + str(i) + '_0.html?sort=0'
                r=requests.get(cate_url)
                soup=BeautifulSoup(r.text,'html5lib')
                total_page=soup.select('.num')[-1]
                total_n=total_page['href'].split('_')[-2]
                # print '*********total_page************',total_n
                if i>int(total_n):
                    print '++++++++  url  ++++++++',cate_url
                    break
                else:
                    req=Request(cate_url,callback=self.cate_game)
                    yield req
    def cate_game(self,response):
        # print '*********************',response.url
        sel=Selector(response)
        cate_game=sel.xpath("//ul[@class='lineList']/li/a/@href").extract()
        # print '+++++++cate_game+++++++',cate_game
        for cate in cate_game:
            game_url='http://ng.d.cn/' + ''.join(cate).split('/')[1]
            # print '*********cate_game_url*******',game_url
            req=Request(game_url,callback=self.game_detail)
            yield req
    def game_detail(self,response):
        print '++++++++++game++++++++++++++++',response.url
        sel=Selector(response)
        game=DcnItem()
        game['game_name']=sel.xpath("//div[@class='zoneGame']/div/h1/a/text()").extract()[0].strip()
        game['game_type_name']=sel.xpath("//div[@class='rigame fl']/text()").extract()[1].strip()
        game['game_time']=sel.xpath("//div[@class='rigame fl']/text()").extract()[-2].strip()
        game['game_content']=sel.xpath("//div[@class='zgamejs']/p/text()").extract()[0].strip()
        return game






