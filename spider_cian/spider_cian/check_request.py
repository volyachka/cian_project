import requests
import scrapy
from urllib.parse import urlencode
from urllib.parse import urlparse
from urllib.parse import urljoin
import re
import json
from spider_cian.items import SpiderCianItem


API = '4b22e100200a489f9fdfdcec2b3b1eb3'

def get_url(url):
    payload = {'api_key': API, 'url': url}
    proxy_url = 'https://realty.ya.ru/moskva/kupit/kvartira/?' + urlencode(payload) # обращаемся к ScraperAPI, указывая необходимый сайт и API ключ
    return proxy_url


page = 1
cur_url = 'https://www.cian.ru/cat.php?' + urlencode(
    {'deal_type': 'sale', 'engine_version': '2', 'offer_type': 'flat',
     'p': str(page), 'region': '1', 'room1': '1', 'room2': '1'})

r = requests.get(get_url(cur_url))
print(r)