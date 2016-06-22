#__author__ = 'gxj'
#-*-coding:utf-8-*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector,Selector
from oppo.items import OppoGameUrlItem
from scrapy import log
import requests
from bs4 import BeautifulSoup


#HTTP请求
from scrapy.http import FormRequest,Request

class OppoSpider(CrawlSpider):
    name='oppo'
    allowed_domains=['wap.game.oppomobile.com']
    start_urls=['http://wap.game.oppomobile.com/category/index']

    def parse(self, response):
        sel= Selector(response)
        cate_url = sel.xpath("""//div[@id="submenu"]//a/@href""").extract()
        for cate in cate_url:
            cate_u="http://wap.game.oppomobile.com" + cate
            req = Request(cate_u,callback=self.get_game)
            yield req

    #***************************post 请求分页抓取
    def get_game(self,response):
        sel = Selector(response)
        print '///////////////' ,response.url
        game_url1=sel.xpath("//ul[@id='part4']//li/div/@onclick").extract()[0]
        game_url01='http://wap.game.oppomobile.com'+game_url1.split("\"")[1]

        print '............',game_url01

        data1=sel.xpath("//ul[@id='part4']//li/@master_id").extract()[:]
        print '----------------master_id',data1
        data={}
        data['master_id']=data1
        # print '++++++++++++++',data
        for i in range(2,3):
            url='http://wap.game.oppomobile.com/category/getGames/listType/2/category/1804/gameType/0/pageIndex/' +  str(i)
            r=requests.post(url,data=data)
            soup=BeautifulSoup(r.text,'html5lib')

            mast_id_list = soup.select("li")
            for mast in mast_id_list[:1]:
                mast_id = int(mast['master_id'])
                data["master_id"].append(mast_id)
            game_list = soup.select('li')
            if len(game_list)==0:
                break
            for game in game_list:
                game_url = 'http://wap.game.oppomobile.com' + game.div["onclick"].split('"')[1]+game_url01
                print '**************game_url',game_url
                req = Request(game_url,callback=self.game_mes)
                yield req

    def game_mes(self,response):
        sel=Selector(response)
        # print '5555555555555555',response.url
        game= OppoGameUrlItem()
        game['game_name']=sel.xpath("//div[@class='li_middle']/h2/text()").extract()[0].strip()

        # game['game_url']=
        game['game_type_name']=sel.xpath("//div[@class='version']/text()").extract()[0].strip()
        # game['game_download_times']
        # game['game_id']
        game['game_make_num']=sel.xpath("//div[@class='f12']/text()").extract()[0].strip()
        # game['game_star']
        game['game_lastupdate']=sel.xpath("//div[@class='f12']/text()").extract()[-1].strip()
        game['game_content']=sel.xpath("//div[@class='game_detail']/text()").extract()[0].strip()

        return game




