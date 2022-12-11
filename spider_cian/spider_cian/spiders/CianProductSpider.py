import scrapy
from urllib.parse import urlencode
from urllib.parse import urlparse
from urllib.parse import urljoin
import re
import json
from spider_cian.items import SpiderCianItem

# API = '4b22e100200a489f9fdfdcec2b3b1eb3'

# def get_url(url):
#     payload = {'api_key': API, 'url': url}
#     proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload) # обращаемся к ScraperAPI, указывая необходимый сайт и API ключ
#     return proxy_url

class CianproductspiderSpider(scrapy.Spider):
    name = 'CianProductSpider'
    # allowed_domains = ['cian.ru']
    start_urls = ['https://www.cian.ru/']
    def start_requests(self):
        page = 1
        cur_url = 'https://www.gdeetotdom.ru/kupit-kvartiru-moskva/?' + urlencode({'page': str(page)})
        print(cur_url)
        yield scrapy.Request(url=cur_url, callback=self.parse_keyword_response)


    def parse_keyword_response(self, response):
        for res in response.xpath('//div[starts-with(@class, "c-card premium")]//a[@class="c-card__title"]/@href').extract():
            yield scrapy.Request(url=res, callback=self.parse_flat_page)

    def parse_flat_page(self, response):
        item = SpiderCianItem()
        price = response.xpath('//span[@id="price_nat" and @itemprop="price"]/text()').extract()
        title = response.xpath('//div[@class="title-block premium"]//div[@class="title"]/h1/text()').extract()[0].replace("\xa0", "")
        price_spaces = price[0].replace("\xa0", " ")
        price_mortgage = price[0].replace("\xa0", "")
        address_line = response.xpath('//div[@class="title-block premium"]//div[@class="address-line"]/text()[1]').extract()[0]
        data_first_gen = response.xpath('//div[@class="b-dotted-block__col"]')[0]
        right_data_gen = data_first_gen.xpath('.//div[@class="b-dotted-block__right"]/span[1]/text()[1]').extract()
        left_data_gen = list(data_first_gen.xpath('.//div[@class="b-dotted-block__left"]/span[1]/text()[1]').extract())
        try:
            left_data_gen.remove("Ипотека")
        except:
            pass
        general_info = dict(list(zip(left_data_gen, right_data_gen)))

        floor = general_info["Этаж"]
        floor = floor.replace("\xa0", " ")
        area = general_info["Общая площадь"]
        area = area.replace("\xa0", " ")
        rooms_cnt = general_info["Комнат"]
        rooms_cnt = rooms_cnt.replace("\xa0", " ")


        loc_left = response.xpath('//div[@class="address-params"]//div[@class="b-dotted-block__left"]/span[1]/text()[1]').extract()
        loc_right = response.xpath('//div[@class="address-params"]//div[@class="b-dotted-block__inner"]/a/text()').extract()
        loc_info = dict(list(zip(loc_left, loc_right)))
        loc_info["Метро"] = response.xpath('//div[@class="address-params__metro"]/a[1]/text()[1]').extract()
        for elem in ["Район", "Улица"]:
            if elem not in loc_info:
                loc_info[elem] = ""

        district = loc_info["Район"]
        district.replace("\xa0", " ")
        street = loc_info["Улица"]
        street.replace("\xa0", " ")
        metro = loc_info["Метро"]
        metro = [elem.replace("\xa0", " ") for elem in metro]
        photos = response.xpath('//div[starts-with(@class, "slide js-slide") and @itemprop="image"]/@src').extract()

        item["title"] = title
        item["price_spaces"] = price_spaces
        item["price_mortgage"] = price_mortgage
        item["address_line"] = address_line
        item["photos"] = photos
        item["area"] = area
        item["floor"] = floor
        item["rooms_cnt"] = rooms_cnt
        item["district"] = district
        item["street"] = street
        item["metro"] = metro
        yield item