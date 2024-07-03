import scrapy
import logging

class WorkuaSpiderSpider(scrapy.Spider):
    name = "workua_spider"
    allowed_domains = ["www.work.ua"]
    start_urls = ["https://www.work.ua/jobs-it-python"]

    def parse(self, response):
        root_url = "www.work.ua"
        job_cards = response.css('div[class*="card-hover"]')
        pages_parsed = 1
        for job_card in job_cards:
            title = job_card.css('h2 a::text').get()
            description = job_card.css('p::text').get()
            comp_city = job_card.css('div[class="mt-xs"] span::text').getall()
            city = comp_city[1] if len(comp_city) > 1 else None
            salary_and_comp = job_card.css('[class="strong-600"]::text').getall()
            url = root_url + job_card.css('h2 a::attr(href)').get()
            if len(salary_and_comp) > 1:
                salary = salary_and_comp.pop(0).replace('\n','').replace('\u202f', '').replace('\xa0', '').replace('\u2009', '').strip()
                company = salary_and_comp.pop(0)
            else:
                company = salary_and_comp.pop(0)
                salary = None

            yield {
                "Title": title.replace('\n','').strip(),
                "Salary": salary[:-3].split('–') if salary else None,
                "Company": company.replace('\n','').strip(),
                "City": city,
                "Url": url,
                "Description": ' '.join(description.replace('\xa0', ' ').replace('\n','').strip().split()),
            }

        next_page = response.css('li[class*="no-style add-left-default"] a::attr(href)').get()
        logging.info(f'Pages parsed: {pages_parsed}')

        if next_page:
            pages_parsed+=1
            yield response.follow(url=next_page, callback=self.parse)
