# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CityItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    state = scrapy.Field()
    city = scrapy.Field()
    total = scrapy.Field()

class CountryItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    state = scrapy.Field()
    country = scrapy.Field()
    total = scrapy.Field()

class CompanyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    state = scrapy.Field()
    country = scrapy.Field()
    name = scrapy.Field()
    service =  scrapy.Field()
    total_review = scrapy.Field()
    star = scrapy.Field()
    review_text = scrapy.Field()
    description = scrapy.Field()