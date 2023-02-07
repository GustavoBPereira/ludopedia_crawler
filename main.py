import requests
from bs4 import BeautifulSoup
import re
import datetime

data = []
leilao = {}

id = '5292'
req = requests.get(f'https://ludopedia.com.br/leiloes?id_leilao={id}')
soup = BeautifulSoup(req.text, 'html.parser')


leilao['leilao_id'] = id
leilao['title'] = soup.find('h3', 'no-margin').text.split(' (Término')[0]
leilao['products'] = []
year_text = soup.find('h3', 'no-margin').find('span').text
year_match = re.search(r'/\d\d\d\d', soup.find('h3', 'no-margin').find('span').text)
if year_match:
    leilao['year'] = year_text[year_match.start()+1:year_match.end()]
else:
    leilao['year'] = datetime.date.today().year

tab = soup.find('table', {'class': 'table-ofertas'})
for tr in tab.find('tbody').find_all('tr'):
    if not 'Finalizado' in tr.find('td', 'td-leilao').find('span').text:
        continue

    finish_at = tr.find('td', 'td-leilao').find('span').text.split('Finalizado (')[-1][0:-1]
    price_text = getattr(tr.find('td', 'td-leilao').find('span', 'lance-atual'), 'text', 'R$ 0,0')
    price = float(price_text.split('R$ ')[-1].replace(',', '.'))
    leilao['products'].append(
        {
            'link': tr.find('td', 'td-jogo').find('a')['href'],
            'name': tr.find('td', 'td-info').find('a', 'item-title').text,
            'state': tr.find('td', 'td-info').find('span').text.strip(),
            'finish_at': finish_at[0:5] + f"/{leilao['year']}" + finish_at[5::],
            'price': price
        }
    )

from ipdb import set_trace; set_trace()
"""
{
    'leilao_id': 529,
    'title': h3,
    'year': year
    'products': [
        'link':  td.jogo href
        'name': td.info a.item-title
        'state': td.info span
        'finish_at': td-leilao span + h3.span.year
        'price': td-leilao span.lance-atual
    ]
}
"""