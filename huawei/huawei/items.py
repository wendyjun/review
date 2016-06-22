# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy.item import Item,Field
import scrapy

class HuaweiItem(Item):
    url=Field()
    pass


class HuaweiGameUrlItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    game_name=Field()
    game_type_name=Field()
    game_size=Field()
    game_load_number=Field()
    game_owner=Field()
    game_time=Field()
    game_edition=Field()
    game_content=Field()

    pass
