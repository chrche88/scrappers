import scrapy


class AeoSpider(scrapy.Spider):
    name = "aeospider"
    start_urls = ['https://guomin.alleatone.fr/about']


    def parse(self, response):
        name = response.css('div').extract()
        yield{'Name': name}