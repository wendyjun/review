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

    def parse(self, response):
        print '**************',response.url
        # pass
