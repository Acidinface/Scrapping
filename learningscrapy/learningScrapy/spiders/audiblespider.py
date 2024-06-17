import scrapy


class AudiblespiderSpider(scrapy.Spider):
    name = "audiblespider"
    allowed_domains = ["www.audible.co.uk"]
    start_urls = ["https://www.audible.co.uk/search"]

    def parse(self, response):
        book_list = response.xpath('//div[@class="adbl-impression-container "]/div/span/ul/li')
        for book in book_list:
            title = book.xpath('.//h3/a/text()').get()
            author = book.xpath('.//li[contains(@class, "author")]/span/a/text()').getall()
            narrator = book.xpath('.//li[contains(@class, "narrator")]/span/a/text()').getall()
            series = list(map(lambda b: b.replace('Series:', '').strip(),book.xpath('.//li[contains(@class, "series")]/span/a/text()').getall()))
            length = book.xpath('.//li[contains(@class, "runtime")]/span/text()').get().replace('Length: ', '')
            release = book.xpath('.//li[contains(@class, "release")]/span/text()').get().replace('Release date:', '').strip()
            language = book.xpath('.//li[contains(@class, "language")]/span/text()').get().replace('Language:', '').strip()
            rating = book.xpath('.//li[contains(@class, "rating")]/span/text()').get()
            popular = bool(book.xpath('.//li[contains(@class, "mostPopular")]/span/text()').get())
            trending = bool(book.xpath('.//li[contains(@class, "trending")]/span/text()').get())
            price = book.xpath('//p[contains(@id,"buybox-regular-price")]/span[2]/text()').get().strip()

            yield {
                'title': title,
                'price': price,
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

        next_page_url = response.xpath('//ul[contains(@class, "pagingElements")]/li/span[contains(@class, "nextButton")]/a/@href').get()

        if next_page_url:
            yield response.follow(url=next_page_url, callback=self.parse)