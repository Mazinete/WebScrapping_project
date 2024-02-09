# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
    
class DataCleaning_Pipeline:
    def process_item(self, item, spider):
        #nettoyer et normaliser les données
        if item['title']:
            item['title'] = item['title'].strip()
        if item['release_date']:
            item['release_date'] = item['release_date'].strip()
        for review in item['reviews']:
            if review['comment']:
                review['comment'] = review['comment'].strip()
            if review['rating']:
                review['rating'] = review['rating'].strip()
        return item

class Json_Pipeline:
    def open_spider(self, spider):
        self.file = open('data.json', 'w')
        self.first_item = True
        self.file.write('[')

    def process_item(self, item, spider):
        if not self.first_item:
            self.file.write(',\n')
        else:
            self.first_item = False
        
        line = json.dumps(dict(item))
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.write('\n]')
        self.file.close()