# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item,Field


class XiechengItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name= Field()
    address=Field()
    price=Field()
    content = Field()
    score= Field()
    comment=Field()

    pass
