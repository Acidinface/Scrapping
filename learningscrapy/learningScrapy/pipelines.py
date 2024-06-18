# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging
import pymongo
from itemadapter import ItemAdapter
import pymongo.mongo_client


class MongodbPipeline:
    collection_name = 'transcripts'

    def open_spider(self, spider):
        self.client = pymongo.MongoClient('mongodb+srv://sit4everacab:IGDD5Gxo4X2MOHwR@cluster0.sxqt7qt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
        self.db = self.client['My_Database']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(item)
        return item
