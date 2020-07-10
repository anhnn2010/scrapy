# -*- coding: utf-8 -*-
import scrapy
from ..items import BarristerItem
import json


class Barrister1Spider(scrapy.Spider):
    name = 'barrister_1'

    def start_requests(self):
        base_url = 'https://fab-api.nswbar.asn.au/fab/api/barristers?text=' \
                   '&currPage={}' \
                   '&limit=16&yearRange=all&expType=noPref&gender=noPref&silk=noPref&crownProsecutor=noPref&interstate=N&sort=surname&sortOrder=1'''
        page = 1
        last_page = 162
        while page < last_page:
            url = base_url.format(str(page))
            yield scrapy.Request(url=url, callback=self.parse)
            page += 1

    def parse(self, response):
        content = json.loads(response.body)
        list_companies = content['results']
        # company = list_companies[0]
        for company in list_companies:
            if company.get('barristers', False):
                #barrister
                list_barristers = company['barristers']
                barrister = list_barristers[0]
                _id =barrister['_id']
            elif company.get('chambers', False):
                #chamber
                _id = company['_id']
            else:
                self.log('Something wrong. There is not chamber or barrister')

            url = f'https://fab-api.nswbar.asn.au/fab/api/barrister?_id={_id}'
            yield scrapy.Request(url=url, callback=self.parse_barristers)

    def parse_barristers(self, response):
        company = json.loads(response.body)
        item = BarristerItem()
        item['email'] = company['email']
        item['name'] = company['firstName'] + company['surname']
        item['phone'] = company['phone']
        chambers = company['chambers']
        if chambers != []:
            item['company'] = chambers[0]['name']
            item['address'] = chambers[0]['address']
        else:
            item['company'] = None
            item['address'] = None
        yield item
