# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class JobscraperPipeline:
    def process_item(self, item, spider):
        details = item['details']

        if details['salary']:
            details['salary'] = details['salary'].replace('\u202f', '').replace('\xa0', '').replace('\u2009', '').strip()[:-3].split('–')

        if details['company_link']:
            details['company_link'] = "https://www.work.ua" + details['company_link']

        if details['address']:
            details['address'] = details['address'].replace('\n', '').strip() if details['address'] else None
        
        if details['job_type']:
            details['job_type'] = details['job_type'].replace('\n', '').strip()

        if details['description']:
            description = " ".join(list(map(lambda x: x.replace('\n', '').strip(), details['description'])))
        details['description'] = description.strip()

        item['details'] = details
        return item
