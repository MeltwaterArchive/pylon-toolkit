from unittest import TestCase

from pylon.queries.querybase import QueryBase


class TestQueryBase(TestCase):
    def test_should_classify_task_as_unfinished_if_queued(self):
        qb = QueryBase(None, None)
        qb.results = {1: {"status": "queued"}}
        self.assertFalse(qb.is_finished(1))
        self.assertTrue(qb.is_unfinished(1))

    def test_should_classify_task_as_unfinished_if_running(self):
        qb = QueryBase(None, None)
        qb.results = {1: {"status": "running"}}
        self.assertFalse(qb.is_finished(1))
        self.assertTrue(qb.is_unfinished(1))

    def test_should_classify_task_as_finished_if_completed(self):
        qb = QueryBase(None, None)
        qb.results = {1: {"status": "completed", "results": []}}
        self.assertTrue(qb.is_finished(1))
        self.assertFalse(qb.is_unfinished(1))

    def test_should_classify_task_as_finished_if_failed(self):
        qb = QueryBase(None, None)
        qb.results = {1: {"status": "failed"}}
        self.assertTrue(qb.is_finished(1))
        self.assertFalse(qb.is_unfinished(1))
