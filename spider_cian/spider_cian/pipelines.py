# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json


class SpiderCianPipeline:
    def open_spider(self, spider):
        self.file = open('items.json', 'w')
        self.data = []

    def close_spider(self, spider):
        json.dump(self.data, self.file, indent=2, ensure_ascii=False)
        self.file.close()

    def process_item(self, item, spider):
        self.data.append(ItemAdapter(item).asdict())
        return item
