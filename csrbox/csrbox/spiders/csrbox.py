# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy_splash import SplashRequest
import urllib
from scrapy import FormRequest


class FbrefSpider(scrapy.Spider):
    name = 'csrbox'
    start_urls = ['https://csrbox.org/India-list-CSR-projects-India']

    # def start_requests(self):
    #     page_size = 25
    #     headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
    #                'X-Requested-With': 'XMLHttpRequest',
    #                'Host': 'csrbox.org',
    #                'Origin': 'https://www.csrbox.org',
    #                'Accept': '*/*',
    #                'Referer': 'https://www.csrbox.org/',
    #                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    #     for offset in (0, 200, page_size):
    #         # yield Request('https://csrbox.org/moreCompanyProjects.php',
    #         yield SplashRequest('https://csrbox.org/moreCompanyProjects.php',
    #                       method='POST',
    #                       headers=headers,
    #                       body=urllib.parse.urlencode(
    #                           {'action': 'load_more',
    #                            'numPosts': page_size,
    #                            'offset': offset,
    #                            'category': '',
    #                            'orderby': 'date',
    #                            'time': ''}),
    #                            callback=self.parse)

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(
                url=url,
                callback=self.parse
            )

    def parse(self, response):
        # self.log(response.body)


        page_size = 25
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                   'X-Requested-With': 'XMLHttpRequest',
                   'Host': 'csrbox.org',
                   'Origin': 'https://www.csrbox.org',
                   'Accept': '*/*',
                #    'Referer': 'https://www.csrbox.org/',
                   'Referer': 'https://csrbox.org/India-list-CSR-projects-India',
                   'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        data = {
            'last_id': '10861',
            'limit': '9',
            'qry': 'select *,  cm.id AS PDID from ngo_cmp_projectdetail cm join ngo_csr_prolocation pl on pl.pro_id=cm.id where cm.status!=0',
            'ob': 'order by cm.project_name asc',
            'incre': '3',
            'array_records': '[{"prid":"13781","loopid":1}]'
        }
        for offset in (0, 200, page_size):
            # yield Request('https://csrbox.org/moreCompanyProjects.php',
            # yield SplashRequest('https://csrbox.org/moreCompanyProjects.php',
            #               method='POST',
            #               headers=headers,
            #               body=urllib.parse.urlencode(
            #                   {'action': 'load_more',
            #                    'numPosts': page_size,
            #                    'offset': offset,
            #                    'category': '',
            #                    'orderby': 'date',
            #                    'time': ''}),
            #                    callback=self.parse_test)
            yield FormRequest(
                'https://csrbox.org/moreCompanyProjects.php',
                method='POST',
                headers=headers,
                callback=self.parse_test,
                formdata=data
            )

    def parse_test(self, response):
        # self.log(response.body)
        pass
