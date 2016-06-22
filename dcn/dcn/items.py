# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item,Field


class DcnItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    game_name=Field()
    game_type_name=Field()
    game_time=Field()
    game_content=Field()
    pass
