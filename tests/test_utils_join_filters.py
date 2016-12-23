from unittest import TestCase
from pylon.utils import Utils
from nose.tools import with_setup

class TestJoinFilters(TestCase):

    def test_both_none_returns_none(self):
        res = Utils.join_filters('AND', None, None)
        self.assertEqual(None, res)

    def test_both_empty_returns_empty(self):
        res = Utils.join_filters('AND', '', '')
        self.assertEqual(len(res), 0)

    def test_second_none_returns_first(self):
        res = Utils.join_filters('AND', 'li.type exists', None)
        self.assertEqual(res, 'li.type exists')

    def test_second_empty_returns_first(self):
        res = Utils.join_filters('AND', 'li.type exists', '')
        self.assertEqual(res, 'li.type exists')

    def test_first_none_returns_second(self):
        res = Utils.join_filters('AND', None, 'li.type exists')
        self.assertEqual(res, 'li.type exists')

    def test_first_empty_returns_second(self):
        res = Utils.join_filters('AND', '', 'li.type exists')
        self.assertEqual(res, 'li.type exists')

    def test_both_non_empty_returns_joined(self):
        res = Utils.join_filters('AND', 'li.type exists', 'li.type exists')
        self.assertEqual(res, '(li.type exists) AND (li.type exists)')