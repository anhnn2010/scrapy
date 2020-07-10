# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from ..items import EcaytradeItem


class Ecaytrade1Spider(scrapy.Spider):
    name = 'ecaytrade_1'
    start_urls = ['https://ecaytrade.com/cayman/real-estate/for-rent']

    def parse(self, response):
        next_href = response.xpath("//a[@title = 'Go to next page']/@href").get()
        if next_href:
            next_url = response.urljoin(next_href)
            yield Request(url=next_url, callback=self.parse)

        list_rent = response.xpath("//li/div[contains(@class, 'node-product')]")
        for rent in list_rent:
            symbol = rent.xpath(".//sup/text()").get()
            number = ''.join(rent.xpath(".//div[@class='price-box']/text()").getall()).strip()
            unit = rent.xpath(".//span[@class='currency']/text()").get()
            image = rent.xpath(".//img/@src").get()
            tmp = {
                'symbol': symbol,
                'number': number,
                'unit': unit,
                'image': image,
                'url': response.url
            }

            href = rent.xpath(".//h3/a/@href").get()
            if href:
                url = response.urljoin(href)
                req = Request(url=url, callback=self.parse_details, cb_kwargs=tmp)
                yield req
            else:
                self.log("There is not href to details")

    def parse_details(self, response, **kwargs):
        title = response.xpath("//h1/text()").get()
        address = response.xpath("//ul[@class='meta--list']/li[contains(text(), 'Address')]/strong/text()").get()
        location = response.xpath("//ul[@class='meta--list']/li[contains(text(), 'Address')]/preceding-sibling::li/strong/text()").get()
        seller = response.xpath("//div[@class='product--seller']/h2/text()").get()
        desc_hdr = response.xpath("//h2[text()='Description:']")
        if desc_hdr:
            description = ''.join(desc_hdr.xpath("./following-sibling::*//p/text()").getall())
        else:
            description = None

        item = EcaytradeItem()
        item['title'] = title
        item['address'] = address
        item['location'] = location
        item['seller'] = seller
        item['description'] = description
        item['symbol'] = kwargs['symbol']
        item['number'] = kwargs['number']
        item['unit'] = kwargs['unit']
        item['image'] = kwargs['image']
        item['url'] = kwargs['url']
        yield item
