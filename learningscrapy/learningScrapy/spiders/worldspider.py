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
        
            yield response.follow(url=link, callback=self.parse_country, meta={'country': name})

    def parse_country(self, response):
        country = response.request.meta['country']
        col_names = response.xpath('(//table[@class="table table-striped table-bordered table-hover table-condensed table-list"])[1]/thead/tr/th')
        col_names = [col.xpath('.//text()').get() for col in col_names]
        rows = response.xpath('(//table[@class="table table-striped table-bordered table-hover table-condensed table-list"])[1]/tbody/tr')
        rows = [tr.xpath('.//*/text()').getall() for tr in rows]
        def transpose(matrix):
            result = []
            while all(matrix):
                new_row = []
                for row in matrix:
                    new_row.append(row.pop(0))
                result.append(new_row)
            return result
        rows = transpose(rows)
        yield {country:{key: value for (key, value) in zip(col_names, rows)}}