# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request


class Myhomepage1Spider(scrapy.Spider):
    name = 'myhomepage_1'
    # allowed_domains = ['myhomepage.ca']
    start_urls = ['https://myhomepage.ca/builder/']

    def parse(self, response):
        next_url = response.xpath("//div[@class='pagination-style']/a[contains(@class, 'next')]/@href").get()
        if next_url:
            yield Request(url=next_url, callback=self.parse)
        else:
            print('There is no more page.')

        list_blocks = response.xpath("//div[@class='col-md-6']")
        for block in list_blocks:
            name = block.xpath(".//a/h4/text()").get()
            email = block.xpath(".//p/a[contains(@href, 'mailto')]/text()").get()
            yield {
                'name': name,
                'email': email
            }
