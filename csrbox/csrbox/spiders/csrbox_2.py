# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
# from scrapy_splash import SplashRequest
# import urllib
from scrapy.http import HtmlResponse
from selenium import webdriver
import time

class FbrefSpider(scrapy.Spider):
    name = 'csrbox_2'
    start_urls = ['https://csrbox.org/India-list-CSR-projects-India']

def scroll(self, driver, timeout):
    scroll_pause_time = timeout

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    num = 2
    for i in range(2) :
    # while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # If heights are the same it will exit the function
            break
        last_height = new_height

    def start_requests(self):
        for url in self.start_urls:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            driver =webdriver.Chrome(executable_path='./csrbox/chromedriver', options=chrome_options)
            driver.get(url)
            self.scroll(driver, 5)
            yield HtmlResponse(driver.current_url, body=driver.page_source, encoding='utf-8')


    def parse(self, response):

        print(response)

    def parse_test(self, response):
        pass
