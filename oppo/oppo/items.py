# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy.item import Item, Field
import scrapy

class OppoItem(Item):
    url=Field()
    pass

class OppoGameUrlItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    game_name=Field()
    game_url =Field()
    game_type_name=Field()
    game_download_times=Field()
    game_id=Field()
    game_make_num=Field()
    game_star=Field()
    game_lastupdate=Field()
    game_content=Field()
    pass
