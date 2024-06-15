import scrapy


class AudiblespiderSpider(scrapy.Spider):
    name = "audiblespider"
    allowed_domains = ["www.audible.co.uk"]
    start_urls = ["https://www.audible.co.uk/search"]

    def parse(self, response):
        book_list = response.xpath('//div[@id="center-3"]/div/div/div/span/ul/li')
        for book in book_list:
            title = book.xpath('.//h3/text()').get()
            author = book.xpath('.//li[contains(@class, "author")]/text()').getall()
            break
            narrator = book.xpath('.//li[contains(@class, "narrator")]/text()').getall()
            series = book.xpath('.//li[contains(@class, "series")]/text()').getall()
            length = book.xpath('.//li[contains(@class, "runtime")]/text()').getall()
            release = book.xpath('.//li[contains(@class, "release")]/text()').getall()
            language = book.xpath('.//li[contains(@class, "language")]/text()').getall()
            rating = book.xpath('.//li[contains(@class, "rating")]/text()').getall()
            popular = book.xpath('.//li[contains(@class, "mostPopular")]/text()').getall()
            trending = book.xpath('.//li[contains(@class, "trending")]/text()').getall()
            yield {
                'title': title,
                'author': author,
                'narrator': narrator,
                'series': series,
                'length': length,
                'release': release,
                'language': language,
                'rating': rating,
                'popular': popular,
                'trending': trending,
            }