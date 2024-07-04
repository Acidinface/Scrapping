# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobItem(scrapy.Item):
    title = scrapy.Field()
    salary = scrapy.Field()
    company = scrapy.Field()
    city = scrapy.Field()
    url = scrapy.Field()
    description = scrapy.Field()

class JobDetails(scrapy.Item):
    address = scrapy.Field()
