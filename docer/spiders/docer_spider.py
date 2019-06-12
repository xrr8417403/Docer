import scrapy
import re

class DocerSpider(scrapy.Spider):

    name = 'docer'
    start_urls = [
        "http://www.docer.com/"
    ]

    def parse(self,response):
        for type_url in response.css('ul.nll_ul li a').extract():
            url = re.search(r'\((.*?)\)', type_url).group(1).replace("'", '').split(",")
            url = url[0] + "&channel=" + url[1] + "@sub channel=" + url[2]
            yield response.follow(url,callback=self.parse_info)
            #sub_response = scrapy.Request(url)
            #for info_url in sub_response.css('div#searchPagePaging a::attr(href)'):
            #    yield sub_response.follow(info_url,callback=self.parse_info)
            #nextpage_url = response.urljoin(response.css('div#searchPagePaging a::attr(href)').extract()[-2])


        #for type_url in response.css('ul.nll_ul li a').extract():
        #    url = re.search(r'\((.*?)\)', type_url).group(1).replace("'", '').split(",")
        #    url = url[0] + "&channel=" + url[1] + "@sub channel=" + url[2]
    def parse_info(self,response):
        for info in response.css('ul.ml_content_main li'):
            url = re.search(r'\((.*?)\)', info.css('p a.mcm_title').get()).group(1).replace('\\', '').replace("'", '')
            yield response.follow(url,callback=self.parse_details)
        nextpage_url = response.urljoin(response.css('div#searchPagePaging a::attr(href)').extract()[-2])
        yield response.follow(nextpage_url,callback=self.parse_info)

    def parse_details(self,response):
        for details in response.css('div.dl_goods_info'):
            yield{
                'title':details.css('h2.dginfo_h2::attr(title)').get(),
                'price':details.css('div.dginfo_price_span span.final_price::text').get(),
                'preview': details.css('ul.dginfo_info li::text')[1].get(),
                'uploadtime':details.css('ul.dginfo_info li::text')[5].get(),
                'type': details.css('ul.dginfo_info li::text')[4].get(),
                'author':details.css('span.dginfo_auther a::text').get()
            }

'''        
    def parse_info(self,response):
        for info in response.css('ul.ml_content_main li'):
            yield {
                'tiele': info.css('a.mcm_title::attr(title)').get(),
                'price': info.css('span.mcm_title_price span::text').get(),
                'preview': info.css('div.mcm_show span.gray::text').get(),
                'url':re.search(r'\((.*?)\)',info.css('p a.mcm_title').get()).group(1).replace('\\','').replace("'",'')
            }
        nextpage_url = response.urljoin(response.css('div#searchPagePaging a::attr(href)').extract()[-2])
        yield response.follow(nextpage_url,callback=self.parse_info)
'''