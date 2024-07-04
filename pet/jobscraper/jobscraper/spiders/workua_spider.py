import scrapy
import logging
from jobscraper.items import JobItem

class WorkuaSpiderSpider(scrapy.Spider):
    name = "workua_spider"
    allowed_domains = ["www.work.ua"]
    start_urls = ["https://www.work.ua/jobs-it"]
    pages_parsed = 1


    def parse(self, response):
        root_url = "www.work.ua"
        job_cards = response.css('div[class*="card-hover"]')
        for job_card in job_cards:
            item = JobItem()
            
            item['title'] = job_card.css('h2 a::text').get().replace('\n','').strip()
            item['description'] = ' '.join(job_card.css('p::text').get().replace('\xa0', ' ').replace('\n','').strip().split())
            
            comp_city = job_card.css('div[class="mt-xs"] span::text').getall()
            item['city'] = comp_city[1] if len(comp_city) > 1 else None
            
            salary_and_comp = job_card.css('[class="strong-600"]::text').getall()
            item['url'] = root_url + job_card.css('h2 a::attr(href)').get()
            
            if len(salary_and_comp) > 1:
                item['salary'] = salary_and_comp.pop(0).replace('\n', '').replace('\u202f', '').replace('\xa0', '').replace('\u2009', '').strip()[:-3].split('–')
                item['company'] = salary_and_comp.pop(0).replace('\n','').strip()
            else:
                item['company'] = salary_and_comp.pop(0).replace('\n','').strip()
                item['salary'] = None
            
            yield item
            

        next_page = response.css('li[class*="no-style add-left-default"] a::attr(href)').get()
        logging.info(f'Pages parsed: {self.pages_parsed}')

        if next_page is not None:
            self.pages_parsed+=1
            yield response.follow(url=next_page, callback=self.parse)

    # def parse_job_page(self, response):
        