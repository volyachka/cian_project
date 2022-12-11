import requests
from bs4 import BeautifulSoup

def get_information(data):
    mortgage = dict()
    mortgage['name_of_mortgage'] = data.find_all('td')[0].text
    mortgage['name_of_bank'] = data.find_all('td')[1].text
    mortgage['percent'] = data.find_all('td')[2].text
    mortgage['payment'] = data.find_all('td')[3].text
    mortgage['link_to_apply'] = 'https://www.banki.ru' + data.find_all('a')[0].get('href')
    return mortgage

def get_mortgage(initialFee = 2500000, price = 6000000, isHaveChildBefore2018 = 1, remainingPayment =3000000, priceForRefinance =4000000):
    link = f"""https://www.banki.ru/products/hypothec/?initialFee={initialFee}&price={price}&period=7&isHaveChildBefore2018={isHaveChildBefore2018}&remainingPayment={remainingPayment}&priceForRefinance={priceForRefinance}&periodForRefinance=7&sortType=popular&sortDirection=desc&selectedFormIndex=0"""
    r = requests.get(link)
    page = r.content.decode("utf-8")
    soup = BeautifulSoup(page, 'html.parser')
    root = soup.find_all('tr')
    list_of_top_3_mortgages = list()
    list_of_top_3_mortgages.append(get_information(root[1]))
    list_of_top_3_mortgages.append(get_information(root[2]))
    list_of_top_3_mortgages.append(get_information(root[3]))
    print(list_of_top_3_mortgages)
    return list_of_top_3_mortgages

get_mortgage()