# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest


class FbrefSpider(scrapy.Spider):
    name = 'fbref'
    start_urls = ['https://fbref.com/en/comps/9/stats/Premier-League-Stats']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, callback=self.parse)

    def parse(self, response):

        # list of all rows containing players
        list_rows = response.xpath("//table/caption[text()='Player Standard Stats Table']/parent::*/tbody/tr[not(@class)]")
        number = 100    # just collect first 100 players
        list_select = list_rows[0:number]

        for row in list_select:
            href = row.xpath("./td[@data-stat='player']/a").attrib['href']
            url = response.urljoin(href)    # url to each players
            yield scrapy.Request(url=url, callback=self.parse_player)

    def parse_player(self, response):

        # I just get last 3 records first, but the web have dupicated records.
        # So I select specific seasons as requirement
        req_seasons = ['2017-2018', '2018-2019', '2019-2020']

        for s in req_seasons:
            # after investigating, the id is not only one value, it can be:
            # div_stats_standard_ks_dom_lg
            # div_stats_standard_dom_lg
            # div_stats_keeper_ks_dom_lg
            # a = response.xpath(f"//div[@id='div_stats_standard_ks_dom_lg']/table/tbody/tr/th[text()='{s}']/following-sibling::td[@data-stat='matches']/a")
            a = response.xpath(f"//div[contains(@id, '_dom_lg') and (contains(@id, 'div_stats_standard') or contains(@id, 'div_stats_keeper'))]/table/tbody/tr/th[text()='{s}']/following-sibling::td[@data-stat='matches']/a")
            if a:
                href = a.attrib['href']
                url = response.urljoin(href)    # url to each season
                yield scrapy.Request(url=url, callback=self.parse_summary)

    def parse_summary(self, response):

        url_split = response.url.split('/')
        season = url_split[-3:-2]

        # name of the player
        name =  response.xpath("//h1/text()").get()

        # list of all matches in a season
        list_rows = response.xpath("//table[@id='ks_matchlogs_all']//tbody/tr[not(@class)]")

        for row in list_rows:
            date = row.xpath("./th/a/text()").get()
            comp = row.xpath("./td[@data-stat='comp']/a/text()").get()
            rnd = row.xpath("./td[@data-stat='round']/a/text()").get()
            venue = row.xpath("./td[@data-stat='venue']/text()").get()
            result = row.xpath("./td[@data-stat='result']/text()").get()
            squad = row.xpath("./td[@data-stat='squad']/a/text()").get()
            opponent = row.xpath("./td[@data-stat='opponent']/a/text()").get()

            yield {
                'Name': name,
                'Season': season,
                'Date': date,
                'Competition': comp,
                'Round': rnd,
                'Venue': venue,
                'Result': result,
                'Squad': squad,
                'Opponent': opponent
            }