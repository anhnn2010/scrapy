# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EcaytradeItem(scrapy.Item):
    symbol = scrapy.Field()
    number = scrapy.Field()
    unit = scrapy.Field()
    image = scrapy.Field()
    title = scrapy.Field()
    address = scrapy.Field()
    location = scrapy.Field()
    seller = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
