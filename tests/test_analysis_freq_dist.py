from unittest import TestCase
from pylon.analysis import Analysis
from nose.tools import with_setup
from tests.mockclient import MockClient

class TestAnalysisFreqDist(TestCase):

    def setup(self):
        self.pylon =Analysis(MockClient(), 'linkedin', 'recording_id')
        self.task_name = 'Interaction types'
        self.target = 'li.type'
        self.threshold = 10

    def test_freq_dist_name(self):
        self.setup()

        res = self.pylon.freq_dist(self.task_name, self.target)
        self.assertEqual(res.analyses[0]['name'], self.task_name)

    def test_freq_dist_analysis_type(self):
        self.setup()

        res = self.pylon.freq_dist(self.task_name, self.target)
        self.assertEqual(res.analyses[0]['parameters']['analysis_type'], 'freqDist')

    def test_freq_dist_target(self):
        self.setup()

        res = self.pylon.freq_dist(self.task_name, self.target)
        self.assertEqual(res.analyses[0]['parameters']['parameters']['target'], self.target)

    def test_freq_dist_threshold(self):
        self.setup()

        res = self.pylon.freq_dist(self.task_name, self.target, threshold=self.threshold)
        self.assertEqual(res.analyses[0]['parameters']['parameters']['threshold'], self.threshold)

    def test_freq_dist_default_threshold(self):
        self.setup()

        res = self.pylon.freq_dist(self.task_name, self.target)
        self.assertEqual(res.analyses[0]['parameters']['parameters']['threshold'], 200)