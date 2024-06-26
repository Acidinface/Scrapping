import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ScriptcrawlspiderSpider(CrawlSpider):
    name = "scriptcrawlspider"
    allowed_domains = ["subslikescript.com"]
    start_urls = ["https://subslikescript.com/movies_letter-X"]
    custom_settings = {
        'DOWNLOAD_DELAY': 0.5,
    }

    rules = (Rule(LinkExtractor(restrict_xpaths="//ul[@class='scripts-list']/li/a"), callback="parse_item", follow=True),
             Rule(LinkExtractor(restrict_xpaths="(//a[@rel='next'])[2]")))

    def parse_item(self, response):
        article = response.xpath("//article[@class='main-article']")
        script_str = ' '.join(article.xpath("./div[@class='full-script']/text()").getall())
        yield {
            'title': article.xpath("./h1/text()").get()[:-18],
            'plot': article.xpath("./p/text()").get(),
            'script': script_str,
            'url': response.url,
        }
