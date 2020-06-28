# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy_selenium import SeleniumRequest

class FbrefSpider(scrapy.Spider):
    name = '3'
    start_urls = ['https://csrbox.org/India-list-CSR-projects-India']

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response):
        # print('hehe' + response.request.meta['driver'].title)
        print(response.body)

    def parse_test(self, response):
        pass
