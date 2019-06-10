import scrapy


class DocerSpider(scrapy.Spider):

    name = 'docer'
    start_urls = [
        "http://search.docer.com/%E6%89%80%E6%9C%89/?tags=%E4%BC%9A%E8%AE%AE%E8%AE%B0%E5%BD%95&orderby=hot"
    ]

    def parse(self,response):
        for type_url in response.css('ul.nll_ul::attr(href)'):
            print(type_url)