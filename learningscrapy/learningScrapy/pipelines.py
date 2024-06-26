# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging
import pymongo
import sqlite3
from itemadapter import ItemAdapter
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi



class MongodbPipeline:
    collection_name = 'transcripts'
    uri = "mongodb+srv://sit4everacab:sit4everacab@cluster0.sxqt7qt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

    def open_spider(self, spider):
        try:
            self.client = MongoClient(self.uri, server_api=ServerApi('1'))
            self.db = self.client['My_learning']
            self.collection = self.db[self.collection_name]
            logging.info("Connected to MongoDB")
        except pymongo.errors.ConnectionError as e:
            logging.error(f"Could not connect to MongoDB: {e}")

    def close_spider(self, spider):
        self.client.close()
        logging.info("Closed MongoDB connection")

    def process_item(self, item, spider):
        try:
            item_dict = ItemAdapter(item).asdict()  # Convert item to dictionary
            self.collection.insert_one(item_dict)
            logging.info(f"Inserted item: {item_dict}")
        except pymongo.errors.PyMongoError as e:
            logging.error(f"Error inserting item into MongoDB: {e}")
        return item
    
class SQLitePipeline:

    def open_spider(self, spider):
        self.connection = sqlite3.connect('transcripts.db')
        self.c = self.connection.cursor()
        try:
            self.c.execute('''
                            CREATE TABLE IF NOT EXISTS transcripts(
                           title TEXT,
                           plot TEXT,
                           script TEXT,
                           url TEXT)
                            ''')
            self.connection.commit()
        except sqlite3.OperationalError:
            logging.error("Error with SQL command(Table may already exist)")
        except:
            logging.error(f"Could not connect to SQL")

    def close_spider(self, spider):
        self.connection.close()
        logging.info("Closed SQL connection")

    def process_item(self, item, spider):
        try:
            logging.debug(f"Item to be inserted: {item}")
            self.c.execute('''
                            INSERT INTO transcripts (title, plot, script, url) VALUES(?, ?, ?, ?)
                           ''', (item.get('title'),
                                 item.get('plot'),
                                 item.get('script'),
                                 item.get('url'),))
            self.connection.commit()
            logging.info(f"Inserted item to transcripts.db")
        except Exception as e:
            logging.error(f"Error inserting item into transcripts.db: {e}")
        return item
