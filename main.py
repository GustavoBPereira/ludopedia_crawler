import datetime
import re
import requests
from bs4 import BeautifulSoup

from storage import add_product

data = []
leilao = {}


def get_soup(_id):
    req = requests.get(f'https://ludopedia.com.br/leiloes?id_leilao={_id}')
    return BeautifulSoup(req.text, 'html.parser') if req.status_code else None


def get_leilao_data(_id):
    print(_id)
    data = {}
    soup = get_soup(_id)
    if not soup or soup.find('a', attrs={'title': 'Leilões que terminam em menos de 24 horas'}):
        return []

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
    try:
        trs = tab.find('tbody').find_all('tr')
    except AttributeError:
        return []

    for tr in trs:
        try:
            if not 'Finalizado' in tr.find('td', 'td-leilao').find('span').text:
                continue
        except:
            continue

        finish_at = tr.find('td', 'td-leilao').find('span').text.split('Finalizado (')[-1][0:-1]
        price_text = getattr(tr.find('td', 'td-leilao').find('span', 'lance-atual'), 'text', 'R$ 0,0')
        price = float(price_text.split('R$ ')[-1].replace('.', '').replace(',', '.'))
        products.append(
            {
                'name': tr.find('td', 'td-info').find('a', 'item-title').text,
                'state': tr.find('td', 'td-info').find('span').text.strip(),
                'finish_at': datetime.datetime.strptime(finish_at[0:5] + f'/{year}' + finish_at[5::], '%d/%m/%Y %H:%M'),
                'price': price
            }
        )
    return products


def crawl():
    import time, random
    for leilao_data in get_leilao_data(2832):
        yield leilao_data
    time.sleep(random.randint(5, 16))


if __name__ == '__main__':
    for line in crawl():
        add_product(**line)
