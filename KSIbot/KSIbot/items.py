# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class KsibotItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = Field()
    link = Field()
    desc = Field()

    pass

class PlayerItem(scrapy.Item):
	name = Field()
	year = scrapy.Field()
	age = scrapy.Field()
	link = scrapy.Field()
