import unittest

from app import main


class TutorialFunctionalTests(unittest.TestCase):
    def setUp(self):
        app = main({})
        from webtest import TestApp

        self.testapp = TestApp(app)

    def test_search_payload(self):
        res = self.testapp.get('/search?q=santorini', status=200)

        for product in res.json:
            self.assertListEqual(list(product.keys()), ['name', 'count_sold', 'count_not_sold'])

    def test_search_another_game_find(self):
        res = self.testapp.get('/search?q=santorini', status=200)

        another_game_find = False
        for product in res.json:
            if product['name'] == 'Santorini: Golden Fleece':
                another_game_find = True
        assert another_game_find

    def test_detail_payload(self):
        res = self.testapp.get('/detail?q=santorini', status=200)

        for product in res.json:
            self.assertListEqual(list(product.keys()),
                                 ['id', 'leilao_id', 'title', 'finish_at', 'name', 'price', 'state'])

    def test_detail_filter_just_query(self):
        res = self.testapp.get('/detail?q=santorini', status=200)

        for product in res.json:
            assert product['name'] == 'Santorini'
