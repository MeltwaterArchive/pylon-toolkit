from unittest import TestCase
from pylon.queries.queryfactory import QueryFactory
from tests.mockclient import MockClient

class TestsQueryFactory(TestCase):

    def setUp(self):
        self.queryfactory = QueryFactory(None, MockClient())

    def test_complete_params_filter_none_none_filter_success(self):
        params = {}
        self.queryfactory.complete_params(params, filter=None)
        self.assertEqual(params, {})

    def test_complete_params_filter_empty_none_filter_success(self):
        params = {}
        self.queryfactory.complete_params(params, filter='')
        self.assertEqual(params, {})

    def test_complete_params_filter_whitespace_none_filter_success(self):
        params = {}
        self.queryfactory.complete_params(params, filter='''
                 ''')
        self.assertEqual(params, {})

    def test_overall_filter_none_none_filter_success(self):
        params = {}
        factory = QueryFactory(None, MockClient(), filter=None)
        factory.complete_params(params, filter=None)
        self.assertEqual(params, {})

    def test_overall_filter_empty_none_filter_success(self):
        params = {}
        factory = QueryFactory(None, MockClient(), filter='')
        factory.complete_params(params, filter=None)
        self.assertEqual(params, {})

    def test_overall_filter_whitespace_none_filter_success(self):
        params = {}
        factory = QueryFactory(None, MockClient(), filter='''
                 ''')
        factory.complete_params(params, filter=None)
        self.assertEqual(params, {})

