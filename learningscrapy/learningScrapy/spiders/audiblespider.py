import scrapy


class AudiblespiderSpider(scrapy.Spider):
    name = "audiblespider"
    allowed_domains = ["www.audible.co.uk"]
    start_urls = ["https://www.audible.co.uk/search"]

    def parse(self, response):
        pass
