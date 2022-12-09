# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderCianItem(scrapy.Item):
    title = scrapy.Field()
    price_spaces = scrapy.Field()
    price_mortgage = scrapy.Field()
    address_line = scrapy.Field()
    photos = scrapy.Field()
    area = scrapy.Field()
    floor = scrapy.Field()
    rooms_cnt = scrapy.Field()
    district = scrapy.Field()
    street = scrapy.Field()
    metro = scrapy.Field()
