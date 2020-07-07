# -*- coding: utf-8 -*-
import scrapy
from ..items import CityItem, CountryItem, CompanyItem


class Caring1Spider(scrapy.Spider):
    name = 'caring_1'
    # allowed_domains = ['caring.com']
    start_urls = ['https://www.caring.com/']

    def parse(self, response):
        list_state_hrefs = response.xpath("//*[@id='top-states']//a/@href").getall()
        list_state_keys = [i.split('/')[-1] for i in list_state_hrefs]
        base_url = 'https://www.caring.com/senior-care'
        list_url_cares = [f'{base_url}/{state}' for state in list_state_keys]
        for url in list_url_cares:
            yield scrapy.Request(url=url, callback=self.parse_summary)

    def parse_summary(self, response):
        list_cities = response.xpath("//*[@id='cities']//div[@class='lrtr-list-item']")
        state = response.xpath("//ol[@class='breadcrumb']//a/text()")[-1].get()
        # ### inspect response by scrapy shell
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        # ###
        # city = list_cities[0]
        for city in list_cities:
            city_name = city.xpath(".//a/text()").get()
            city_sum = city.xpath("./div[@class='text-subtitle2']/text()").get().strip()
            # print(f'{city_name}: {city_sum}')
            city_item = CityItem()
            city_item['state'] = state
            city_item['city'] = city_name
            city_item['total'] = city_sum
            yield city_item

        ### start country ###
        list_countries = response.xpath("//*[@id='counties']//div[@class='lrtr-list-item']")
        # country = list_countries[0]
        for country in list_countries:
            country_name = country.xpath(".//a/text()").get()
            country_sum = country.xpath("./div[@class='text-subtitle2']/text()").get().strip()
            # print(f'{country_name}: {country_sum}')
            country_item = CountryItem()
            country_item['state'] = state
            country_item['country'] = country_name
            country_item['total'] = country_sum
            yield country_item

            country_url = country.xpath(".//a/@href").get()
            yield scrapy.Request(url=country_url, callback=self.parse_country)
        ### end country ###

    def parse_country(self, response):
        country = response.xpath("//ol[@class='breadcrumb']//a/text()")[-1].get()
        state = response.xpath("//ol[@class='breadcrumb']//a/text()")[-2].get()

        ### start company ###
        list_companies = response.xpath("//div[@class='search-result']")
        # company = list_companies[0]
        for company in list_companies:
            company_name = company.xpath(".//div[@class='details']/h3//a/text()").get()
            if company.xpath(".//span[@class='count']/a/text()"):
                review_num = company.xpath(".//span[@class='count']/a/text()").re(r'(\d+) review')[0]
            else:
                self.log(f'There is no reviewer for this company: {response.url}')
                review_num = None
            if company.xpath(".//input/@value"):
                review_star = round(float(company.xpath(".//input/@value").get()), 1)
            else:
                self.log(f'There is no star for this company: {response.url}')
                review_star = None
            review_text = company.xpath(".//div[@class='hidden-xs']/div[@class='description']/text()").get().strip().strip('"')
            company_info = {
                'state': state,
                'country': country,
                'name': company_name,
                'review_num': review_num,
                'review_star': review_star,
                'review_text': review_text
            }
            link = company.xpath(".//a[contains(@class, 'btn-secondary')]/@href").get()
            url = link + '#description'
            req = scrapy.Request(url=url, callback=self.parse_desc, cb_kwargs=company_info, dont_filter=True)
            yield req
        ### end company ###

    def parse_desc(self, response, **kwargs):
        # print(reponse.url)
        company = kwargs
        text = response.xpath("//*[@id='description']/div//p/text()").getall()
        description = '\n'.join(text).strip()
        company['description'] = description

        company_item = CompanyItem()
        company_item['state'] = company['state']
        company_item['country'] = company['country']
        company_item['name'] = company['name']
        company_item['service'] = 'Home Care'
        company_item['total_review'] = company['review_num']
        company_item['star'] = company['review_star']
        company_item['review_text'] = company['review_text']
        company_item['description'] = company['description']
        yield company_item
