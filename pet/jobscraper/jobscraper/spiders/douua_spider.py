import scrapy # type: ignore
from jobscraper.items import JobItem, JobDetails
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DouuaSpiderSpider(scrapy.Spider):
    name = "douua_spider"
    allowed_domains = ["dou.ua"]
    start_urls = ["https://jobs.dou.ua/vacancies/?search=+"]

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                wait_time=10,
                wait_until=EC.element_to_be_clickable((By.XPATH, '//*[@id="vacancyListId"]/div/a'))
            )

    def parse(self, response):
        job_list = response.xpath('//ul[@class="lt"]/li')
        for job in job_list:
            item = JobItem()
            item['title'] = job.xpath('//div[@class="title"]/a[@class="vt"]/text()').get()
            # item['company'] = response.xpath('//div[@class="title"]/strong/a[@class="company"]')
            item['url'] = job.xpath('//div[@class="title"]/a[@class="vt"]/@href').get()
            item['city'] = job.xpath('//div[@class="title"]/span/text()').get()

            yield item
                