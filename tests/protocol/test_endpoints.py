import unittest
from datetime import datetime

from app import main


class ApiFunctionalTests(unittest.TestCase):
    def setUp(self):
        app = main({})
        from webtest import TestApp

        self.testapp = TestApp(app)

    def test_search_payload(self):
        res = self.testapp.get('/search?q=santorini', status=200)

        for product in res.json:
            self.assertListEqual(list(product.keys()), ['id', 'name', 'quantity'])

    def test_search_another_game_find(self):
        res = self.testapp.get('/search?q=santorini', status=200)

        another_game_find = False
        for product in res.json:
            if product['name'] == 'Santorini: Golden Fleece':
                another_game_find = True
        assert another_game_find

    def test_search_ordenation(self):
        res = self.testapp.get('/search?q=santorini', status=200)
        previous_name = None
        for product in res.json:
            if previous_name:
                assert product['name'] > previous_name
            previous_name = product['name']


    def test_detail_payload(self):
        res = self.testapp.get('/detail?q=santorini', status=200)

        for product in res.json:
            self.assertListEqual(list(product.keys()),
                                 ['id', 'leilao_id', 'title', 'finish_at', 'name', 'price', 'state'])

    def test_detail_filter_just_query(self):
        res = self.testapp.get('/detail?q=santorini', status=200)

        for product in res.json:
            assert product['name'] == 'Santorini'

    def test_detail_param_with_spaces(self):
        res = self.testapp.get('/detail?q=Santorini:%20Golden%20Fleece', status=200)

        for product in res.json:
            assert product['name'] == 'Santorini: Golden Fleece'

    def test_detail_filter_only_sold(self):
        res = self.testapp.get('/detail?q=santorini', status=200)
        for product in res.json:
            assert product['price'] > 0

    def test_detail_filter_include_not_sold(self):
        res = self.testapp.get('/detail?q=santorini&include_not_sold=true', status=200)

        not_sold_finded = False
        for product in res.json:
            if product['price'] == 0.0:
                not_sold_finded = True
        assert not_sold_finded

    def test_detail_ordenation(self):
        res = self.testapp.get('/detail?q=santorini', status=200)

        previous_price = None
        for product in res.json:
            if previous_price:
                assert previous_price <= product['price']
            previous_price = product['price']
