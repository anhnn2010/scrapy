# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
# from scrapy_selenium import SeleniumRequest
from scrapy_splash import SplashRequest

class FbrefSpider(scrapy.Spider):
    name = 'csrbox_4'
    start_urls = ['https://csrbox.org/India-list-CSR-projects-India']

    script_1 = """
        function main(splash)
            local num_scrolls = 10
            local scroll_delay = 1.0

            local scroll_to = splash:jsfunc("window.scrollTo")
            local get_body_height = splash:jsfunc(
                "function() {return document.body.scrollHeight;}"
            )
            assert(splash:go(splash.args.url))
            splash:wait(splash.args.wait)

            for _ = 1, num_scrolls do
                scroll_to(0, get_body_height())
                splash:wait(scroll_delay)
            end
            --return splash:html()
            return {
                html = splash:html(),
                cookies = splash:get_cookies(),
            }
        end
    """

    script_2 = """
        function main(splash)
                local num_scrolls = 10
                local scroll_delay = 1

                local scroll_to = splash:jsfunc("window.scrollTo")
                local get_body_height = splash:jsfunc(
                    "function() {return document.body.scrollHeight;}"
                )
                assert(splash:go(splash.args.url))
                splash:wait(splash.args.wait)

                for _ = 1, num_scrolls do
                    local height = get_body_height()
                    for i = 1, 10 do
                        scroll_to(0, height * i/10)
                        splash:wait(scroll_delay/10)
                    end
                end
                return splash:html()
        end
    """

    script_3 = """
    function main(splash)
        local scroll_delay = 2 -- i have tried to vary this number with some success
        local is_down = splash:jsfunc(
            "function() { return((window.innerHeight + window.scrollY) >= document.body.offsetHeight);}"
            )

        local scroll_to = splash:jsfunc("window.scrollTo")
        local get_body_height = splash:jsfunc(
            "function() {return document.body.scrollHeight;}"
        )
        assert(splash:go(splash.args.url))

        while not is_down() do
            scroll_to(0, get_body_height())
            splash:wait(scroll_delay)
        end
        return splash:html()
    end
    """

    script_4 = """
        function main(splash)
            local num_scrolls = 10
            local scroll_delay = 1.0

            local scroll_to = splash:jsfunc("window.scrollTo")
            local get_body_height = splash:jsfunc(
                "function() {return document.body.scrollHeight;}"
            )
            assert(splash:go(splash.args.url))
            splash:wait(splash.args.wait)

            local current_height = get_body_height()
            local cnt = 0
            while true do
                scroll_to(0, current_height)
                splash:wait(scroll_delay)
                local new_height = get_body_height()
                if new_height == current_height then break end
                --if cnt == 5 then return 'GO', splash:html() end
                if cnt == 5 then return splash:html() end
                if cnt == 5 then break end
                --if cnt == 5 then
                --    return {
                --        html = splash:html(),
                --        cookies = splash:get_cookies(),
                --    }
                --end
                current_height = new_height
                cnt = cnt + 1
            end
            return splash:html()
            --return {
            --    html = splash:html(),
            --    cookies = splash:get_cookies(),
            --}
        end
    """

    script_5 = """
        function main(splash)
            local num_scrolls = 10
            local scroll_delay = 1.0

            local scroll_to = splash:jsfunc("window.scrollTo")
            local get_body_height = splash:jsfunc(
                "function() {return document.body.scrollHeight;}"
            )
            assert(splash:go(splash.args.url))
            splash:wait(splash.args.wait)

            local current_height = get_body_height()
            local cnt = 0
            while true do
                scroll_to(0, current_height)
                splash:wait(scroll_delay)
                local new_height = get_body_height()
                if cnt == 10 then break end
                current_height = new_height
                cnt = cnt + 1
            end
            return splash:html()
        end
    """

    script_6 = """
        function main(splash)
            local num_scrolls = 10
            local scroll_delay = 1.0

            local scroll_to = splash:jsfunc("window.scrollTo")
            local get_body_height = splash:jsfunc(
                "function() {return document.body.scrollHeight;}"
            )
            assert(splash:go(splash.args.url))
            splash:wait(splash.args.wait)

            local current_height = get_body_height()
            local cnt = 0
            while true do
                scroll_to(0, current_height)
                splash:wait(scroll_delay)
                local new_height = get_body_height()
                --if cnt == 10 then break end
                if cnt == 5 then return {flag = 'GO', html = splash:html()} end
                current_height = new_height
                cnt = cnt + 1
            end
            return splash:html()
        end
    """
    script_a = """
        function main(splash)
            assert(splash:go(splash.args.url))
            splash:wait(splash.args.wait)
            return {flag = 'GO', html = splash:html()}
        end
    """

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(
                url=url,
                callback=self.parse_links,
                endpoint='execute',
                args={'lua_source': self.script_a, 'wait': 1})

    def parse_links(self, response):
        list_read_more = response.xpath("//a[@class = 'readmore readmorebutton']")
        if list_read_more:
            for read_more in list_read_more:
                href = read_more.attrib['href']
                url = response.urljoin(href)
                yield Request(url=url, callback=self.parse_items)
        else:
            self.log("Cannot find the element")

        if response.data.get('flag', False) == 'GO':
            yield SplashRequest(
                url=response.url,
                callback=self.parse_links,
                endpoint='execute',
                # args={'lua_source': self.script_1, 'wait': 1}
                # args={'lua_source': self.script_4, 'wait': 1}
                # args={'lua_source': self.script_5, 'wait': 1}
                args={'lua_source': self.script_6, 'wait': 1}
            )
        else:
            self.log('Cannot find the flag GO. It is possible the end of loading pages')

    def parse_items(self, response):
        print(response.url)

