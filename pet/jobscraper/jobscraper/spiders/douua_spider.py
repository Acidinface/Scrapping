import scrapy # type: ignore


class DouuaSpiderSpider(scrapy.Spider):
    name = "douua_spider"
    allowed_domains = ["jobs.dou.ua"]
    start_urls = ["https://jobs.dou.ua/vacancies/"]

    def parse(self, response):
        pass
