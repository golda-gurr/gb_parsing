# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from pymongo import MongoClient
import csv

class JobParserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.job_loader

    def process_item(self, item, spider):
        collection = self.mongobase[spider.name]
        collection.insert_one(item)
        return item


class CSVPipeline():
    def __init__(self):
        self.file = f'database.csv'
        with open(self.file, 'r', newline='') as csv_file:
            self.tmp_data = csv.DictReader(csv_file).fieldnames

        self.csv_file = open(self.file, 'a', newline='', encoding='UTF-8')

    def __del__(self):
        self.csv_file.close()

    def process_item(self, item, spider):
        columns = item.fields.keys()

        data = csv.DictWriter(self.csv_file, columns)
        if not self.tmp_data:
            data.writeheader()
            self.tmp_data = True
        data.writerow(item)
        return item
