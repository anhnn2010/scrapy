# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from ..items import WellbookiItem
import json


class Wellbooki1Spider(scrapy.Spider):
    name = 'wellbooki_1'
    start_urls = ['https://wellbooki.com/api/marketplace/merchants?page=1&descOrAsc=asc&serviceType=0']

    def parse(self, response):
        data = json.loads(response.body)
        last_page = data['data']['pagination']['last_page']

        for page in range(1, last_page + 1):
            base_url = 'https://wellbooki.com/api/marketplace/merchants?page={}&descOrAsc=asc&serviceType=0'
            url = base_url.format(str(page))
            yield Request(url=url, callback=self.parse_services)

    def parse_services(self, response):
        data = json.loads(response.body)
        services = data['data']['data']
        for service in services:
            token = service['token']
            url = f'https://wellbooki.com/api/marketplace/merchant/{token}'
            yield Request(url=url, callback=self.parse_items)

    def parse_items(self, response):
        data = json.loads(response.body)
        item = WellbookiItem()
        item['name'] = data['data']['location']['name']
        item['address'] = data['data']['location']['address']
        item['phone'] = data['data']['location']['phone_number']
        item['website'] = data['data']['website']

        yield item
