import scrapy
from scrapy_splash import SplashRequest
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser

class Spider1(scrapy.Spider):
    name = 'tour'
    api_url = ['https://tournaments.hjgt.org/tournament/TournamentResultSearch']

    # using custom header to look like a human and not getting baned
    custom_headers = {
        "accept": 'application/json, text/javascript, */*; q=0.01',
        "accept-encoding": 'gzip, deflate, br',
        "accept-language": 'en-GB,en-US;q=0.9,en;q=0.8',
        "connection": 'keep-alive',
        "content-length": 319,
        "content-type": 'application/x-www-form-urlencoded; charset=UTF-8',
        "Cookie": 'ASP.NET_SessionId=n2jckzausnirmfqtq3icjwwn; __RequestVerificationToken=9CbPAvcr20TjuTFZVBBgT-1PhASeeMuVRQYRJMeKpSJN-yrF0D6ywTDuJQqZWkwaCsm1tf15HPExPiho9xTmwzmdog4VNb9WCzAHemdklgE1',
        "host": 'tournaments.hjgt.org',
        "origin": 'https://tournaments.hjgt.org',
        "referer": 'https://tournaments.hjgt.org/Tournament/Results/',
        "user-agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/72.0.3626.121 Chrome/72.0.3626.121 Safari/537.36',
        "x-requested-with": 'XMLHttpRequest',
    }

    # Scrapy entry point
    def start_requests(self):
        yield scrapy.Request(url = "https://tournaments.hjgt.org/Tournament/Results/",  dont_filter=True, callback = self.parse)

    def parse(self, response):
        token = response.xpath('//*[@name="__RequestVerificationToken"]/@value').extract_first()

        params = {
            '__RequestVerificationToken': token,
            'PageIndex': '3',
            'PageSize': '10',
            'UpcomingPast': '',
            'SearchString': '',
            'StartDate': '',
            'Distance': '',
            'ZipCode': '',
            'SeasonSelected': '',
        }

        req = FormRequest('https://tournaments.hjgt.org/tournament/TournamentResultSearch',method="POST", headers = self.custom_headers, formdata = params, callback=self.finished)
        yield req
        print("\n\nrequest headers:", req.headers)

    def finished(self, response):
        print(response.text)