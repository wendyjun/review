#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class BaiduItem(Item):
    # define the fields for your item here like:
    # name = Field()
    game_type_name = Field()
    url = Field()
    pass
    
class BaiduGameUrlItem(Item):
    #游戏索引
    game_today = Field()
    game_url = Field()
    game_type_name = Field()
    game_name = Field()
    game_id = Field()
    game_download_times = Field()
    game_mark_num = Field()
    game_stars = Field()
    game_lastupdate = Field()
    game_size = Field()
    game_content=Field()
    pass
