import datetime
import re
import csv
import requests
from bs4 import BeautifulSoup

data = []
leilao = {}


def get_soup(_id):
    req = requests.get(f'https://ludopedia.com.br/leiloes?id_leilao={_id}')
    return BeautifulSoup(req.text, 'html.parser')


def get_leilao_data(_id):
    print(_id)
    data = {}
    soup = get_soup(_id)
    data['leilao_id'] = _id
    data['title'] = soup.find('h3', 'no-margin').text.split(' (Término')[0]
    return [
        {**data, **product} for product in get_product_data(soup)
    ]


def get_product_data(soup):
    products = []
    year_text = soup.find('h3', 'no-margin').find('span').text
    year_match = re.search(r'/\d\d\d\d', soup.find('h3', 'no-margin').find('span').text)
    if year_match:
        year = year_text[year_match.start() + 1:year_match.end()]
    else:
        year = datetime.date.today().year

    tab = soup.find('table', {'class': 'table-ofertas'})
    for tr in tab.find('tbody').find_all('tr'):
        if not 'Finalizado' in tr.find('td', 'td-leilao').find('span').text:
            continue

        finish_at = tr.find('td', 'td-leilao').find('span').text.split('Finalizado (')[-1][0:-1]
        price_text = getattr(tr.find('td', 'td-leilao').find('span', 'lance-atual'), 'text', 'R$ 0,0')
        price = float(price_text.split('R$ ')[-1].replace(',', '.'))
        products.append(
            {
                'name': tr.find('td', 'td-info').find('a', 'item-title').text,
                'state': tr.find('td', 'td-info').find('span').text.strip(),
                'finish_at': finish_at[0:5] + year + finish_at[5::],
                'price': price
            }
        )
    return products


def crawl():
    for c in range(528, 530):
        for leilao_data in get_leilao_data(c):
            yield leilao_data


if __name__ == '__main__':
    with open('data.csv', "w", newline='') as csv_file:
        fields = ['leilao_id', 'title', 'finish_at', 'name', 'price', 'state']
        writer = csv.DictWriter(csv_file, fieldnames=fields)
        writer.writeheader()
        for line in crawl():
            writer.writerow(line)
