# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector,Selector
from huawei.items import HuaweiGameUrlItem
from scrapy import log
from scrapy.http import FormRequest,Request
import json
import requests
import pprint

class HuaweiPipeline(CrawlSpider):
    name = "huawei"
    allowed_domains = ["vmall.com"]
    start_urls = [ 'http://game.vmall.com/game']

    def parse(self, response):
        sel=Selector(response)
        cate_url=sel.xpath("""//div[@class="ui-item  line-dot-bottom"]/div/a/@href""").extract()
        # print '********cate_url**********',cate_url
        for cate in cate_url[:1]:
            cate_u = cate.split("'")[1]
            # print '********cate_u**********',cate_u

            req = Request(cate_u,callback=self.get_game)
            yield req
    #翻页请求游戏详细url
    def get_game(self,response):
        print 'get_game url is',response.url
        for i in range(1,1000):
            game_url= "http://game.vmall.com/apps/moreapplistaction.action?callbackp=jQuery2130763657433357426_1465616697680&reqPageNum=" + str(i) + "&sortColumn=download&kindId=" + response.url.split("/")[-2] + "&_=1465616697681"
            r = requests.get(game_url)
            game_m = "{"+ r.text.split("({")[1][:-1]
            # print game_m
            game_message = json.loads(game_m)
            # pprint.pprint(game_message)
            total_page = game_message["moreAppList"]["totalPages"]
            if i > int(total_page):
                break
            else:
                game_url_list = game_message["moreAppList"]["list"]
                for game in game_url_list:
                    game_url = "http://game.vmall.com/app/" + game["appId"]
                    print game_url
                    req = Request(game_url,callback=self.game_detail)
                    yield req



    def game_detail(self,response):
        sel = Selector(response)
        game=HuaweiGameUrlItem()

        game['game_name']=sel.xpath("//h3[@class='app-title']/text()").extract()[0].strip()
        game['game_type_name']=sel.xpath("//li[@class='in-row-a']/text()").extract()[-1].strip()
        game['game_size']=sel.xpath("//ul[@class='app-ul']//p[@class='app-remark-detail']//span/text()").extract()[0].strip()
        game['game_load_number']=''.join(sel.xpath("//ul[@class='app-ul']//p[@class='app-remark-detail']//span/text()").extract()[-1])[:-4]+'10000'
        game['game_owner']=sel.xpath("//div[@id='detailinfo']//ul/li/text()").extract()[1].strip()
        game['game_time']=sel.xpath("//div[@id='detailinfo']//ul/li/text()").extract()[3].strip()
        game['game_edition']=sel.xpath("//div[@id='detailinfo']//ul/li/text()").extract()[-3].strip()
        game['game_content']=sel.xpath("//input[@id='desc']/@value").extract()[0].strip()
        return game
