# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
import json

# TODO: set User Agent
class Capterra1Spider(scrapy.Spider):
    name = 'capterra_1'
    # allowed_domains = ['capterra.com']
    # start_urls = ['https://www.capterra.com']
    start_urls = ['https://www.capterra.com/categories']
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse, headers={"User-Agent": self.user_agent})

    def parse(self, response):
        list_cat_links = response.xpath("//li[@data-alias-name]/a/@href").getall()
        # TODO: For loop
        # cat_link = list_cat_links[5]
        for cat_link in list_cat_links:
            url = response.urljoin(cat_link)
            yield Request(url=url, callback=self.parse_products, headers={"User-Agent": self.user_agent})

    def parse_products(self, response):
        # TODO: Handle Show More button :(
        if response.xpath("//div/a[contains(text(), 'Learn more about')]/@href"):
            list_product_links = response.xpath("//div/a[contains(text(), 'Learn more about')]/@href").getall()
        elif response.xpath("//p/a[contains(text(), 'Learn more about')]/@href"):
            list_product_links = response.xpath("//p/a[contains(text(), 'Learn more about')]/@href").getall()
        # TODO: For loop
        product_link = list_product_links[0]
        url = response.urljoin(product_link)
        yield Request(url=url, callback=self.parse_items, headers={"User-Agent": self.user_agent})

    def parse_items(self, response):

        result = {}

        # similar products
        list_comp_names = response.xpath("//div[contains(@class, 'section__CarouselContainer')]//a/div[contains(@class, 'ProductComparisonCardHeader__')]/text()").getall()
        list_comp_hrefs = response.xpath("//div[contains(@class, 'section__CarouselContainer')]//a/div[contains(@class, 'ProductComparisonCardHeader__')]/parent::*/@href").getall()
        list_comp_links = [response.urljoin(i) for i in list_comp_hrefs]
        result['comp_info'] = '\n'.join([name + ': ' + link for name, link in zip(list_comp_names, list_comp_links)])

        # rating
        result['overal_rating'] = response.xpath("//div[contains(@class, 'ReviewInfoSubheading__StarRatingCustom')]/div[contains(@class, 'StarRating__Rating')]/text()").get()

        # parse alternative
        alt_url = response.url + 'alternatives/'
        request = Request(url=alt_url, callback=self.parse_alternative, headers={"User-Agent": self.user_agent}, cb_kwargs=result)
        yield request

    def parse_alternative(self, response, **kwargs):
        list_alt_names = response.xpath("//div[contains(@class, 'DesktopProductCard__Product')]/*/a[contains(text(), 'Learn more about')]/text()").re(r'Learn more about (.*)')
        list_alt_hrefs = response.xpath("//div[contains(@class, 'DesktopProductCard__Product')]/*/a[contains(text(), 'Learn more about')]/@href").getall()
        list_alt_links = [response.urljoin(i) for i in list_alt_hrefs]
        alt_info = '\n'.join([name + ': ' + link for name, link in zip(list_alt_names, list_alt_links)])
        kwargs['alt_info'] = alt_info

        # detail review
        # TODO: Handle show more with REST API
        id = re.search(r'.*/(\d+)/.*', response.url).groups()[0]
        review_api_url = f'https://www.capterra.com/spotlight/rest/reviews?apiVersion=2&productId={id}&from='

        num_of_loop = 1
        for i in range(1, num_of_loop + 1):
            url = review_api_url + str(i)
            request = Request(url=url, callback=self.parse_review, headers={"User-Agent": self.user_agent}, cb_kwargs=kwargs)
            yield request

    def parse_review(self, response, **kwargs):
        reviews = json.loads(response.text)
        # TODO: For loop
        review = reviews['hits'][0]
        rev_name = review['reviewer']['fullName']
        rev_industry = review['reviewer']['industry']
        rev_used_time = review['reviewer']['timeUsedProduct']
        rev_rating = review['overallRating']
        rev_date = review['writtenOn']
        rev_pros_cons = 'Pros: ' + review['prosText'] + '\n' + 'Cons: ' + review['consText']

        item = kwargs
        item['rev_name'] = review['reviewer']['fullName']
        item['rev_industry'] = review['reviewer']['industry']
        item['rev_used_time'] = review['reviewer']['timeUsedProduct']
        item['rev_rating'] = review['overallRating']
        item['rev_date'] = review['writtenOn']
        item['rev_pros_cons'] = 'Pros: ' + review['prosText'] + '\n' + 'Cons: ' + review['consText']
        yield item