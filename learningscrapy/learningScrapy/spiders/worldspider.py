import scrapy


class WorldspiderSpider(scrapy.Spider):
    name = "worldspider"
    allowed_domains = ["www.worldometers.info"]
    start_urls = ["https://www.worldometers.info/world-population/population-by-country/"]

    def parse(self, response):
        countries = response.xpath('//td/a')

        for country in countries:
            name = country.xpath('.//text()').get()
            link = country.xpath('.//@href').get()
        
            yield response.follow(url=link, callback=self.parse_country)

    def parse_country(self, response):
        col_names = response.xpath('(//table[@class="table table-striped table-bordered table-hover table-condensed table-list"])[1]/thead/tr/th')
        col_names = [col.xpath('.//text()').get() for col in col_names]
        rows = response.xpath('(//table[@class="table table-striped table-bordered table-hover table-condensed table-list"])[1]/tbody/tr')
        rows = [td.xpath('.//text()').get() for td in tr for tr in rows]
        yield {'rows': rows}
        # yield {key: value for (key, value) in zip(col_names, rows)}