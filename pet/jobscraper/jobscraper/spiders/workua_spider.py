import scrapy # type: ignore
import logging
from jobscraper.items import JobItem, JobDetails

class WorkuaSpiderSpider(scrapy.Spider):
    name = "workua_spider"
    allowed_domains = ["work.ua"]
    start_urls = ["https://www.work.ua/jobs-it"]
    pages_parsed = 1

    def parse(self, response):
        root_url = "https://www.work.ua"
        job_cards = response.css('div[class*="card-hover"]')
        for job_card in job_cards:
            item = JobItem()

            item['title'] = job_card.css('h2 a::text').get().replace('\n', '').strip()
            comp_city = job_card.css('div[class="mt-xs"] span::text').getall()
            item['city'] = comp_city[1] if len(comp_city) > 1 else comp_city[0]
            item['url'] = root_url + job_card.css('h2 a::attr(href)').get()
            
            request = scrapy.Request(url=item['url'], callback=self.parse_job_page)
            request.meta['item'] = item
            yield request

        next_page = response.css('li[class*="no-style add-left-default"] a::attr(href)').get()
        logging.info(f'Pages parsed: {self.pages_parsed}')

        if next_page is not None:
            self.pages_parsed += 1
            yield response.follow(url=next_page, callback=self.parse)

    def parse_job_page(self, response):
        item = response.meta['item']
        details = JobDetails()

        details['salary'] = response.css('[title="Зарплата"] + span::text').get()
        details['company'] = response.css('[title="Дані про компанію"] + a span::text').get()
        details['company_link'] = response.css('[title="Дані про компанію"] + a::attr(href)').get()
        details['address'] = response.xpath('//li[span[@title="Адреса роботи"]]/text()[2]').get()
        details['job_type'] = response.xpath('//li[span[@title="Умови й вимоги"]]/text()[2]').get()
        details['tags'] = response.css('.flex.flex-wrap.list-unstyled.w-100.my-0.pb-0.toggle-block.overflow.block-relative.js-toggle-block li span::text').getall()
        details['description'] = response.css('[class="company-description"] *::text').getall()
        item['details'] = details
        yield item
