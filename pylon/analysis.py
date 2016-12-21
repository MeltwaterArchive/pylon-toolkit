import datasift
import logging
import time

from pylon.queries.queryfactory import QueryFactory

logging.basicConfig(format="%(asctime)-15s -- %(message)s", level=logging.INFO)

class Analysis(object):

    def __init__(self, *args, **kwargs):

        class Config(object):
            def __init__(self, username, apikey, service, recording_id, start=None, end=None, filter=None):
                self.username = username
                self.apikey = apikey
                self.service = service
                self.recording_id = recording_id
                self.start = start
                self.end = end
                self.filter = filter

        self.config = Config(*args, **kwargs)
        self.client = datasift.Client(self.config.username, self.config.apikey, async=True, max_workers=5)
        self.queryfactory = QueryFactory(self.config, self.client, start=self.config.start, end=self.config.end, filter=self.config.filter)
        self.queries = []

    def clear(self):
        self.queries = []

    def waitAll(self):

        logging.info('Waiting completion of all queries.')

        pending=len([i for query in self.queries for i in query.pending()])

        while pending>0:

            t=min(max(pending/2,1),60) # at least 1, at most 60, otherwise #running/2
            time.sleep(t)

            for i in self.queries:
                i.get()

            pending=len([i for query in self.queries for i in query.pending()])


    ############################### Individual analysis queries ###########################################

    def freq_dist(self, name, target, threshold=200, filter=None, start=None, end=None):

        query = self.queryfactory.freq_dist(name, target, threshold=threshold, start=start, end=end, filter=filter)
        self.queries.append(query)
        return query

    def time_series(self, name, interval, span=1, filter=None, start=None, end=None):

        query = self.queryfactory.time_series(name, interval, span=span, start=start, end=end, filter=filter)
        self.queries.append(query)
        return query

    def nested_freq_dist(self, name, level1, threshold1, level2, threshold2, level3=None, threshold3=None, filter=None, start=None, end=None):

        query = self.queryfactory.nested_freq_dist(name, level1, threshold1, level2, threshold2, level3=level3, threshold3=threshold3, start=start, end=end, filter=filter)
        self.queries.append(query)
        return query

    # ############################### Batch analysis queries ###########################################

    def freq_dist_batch_filters(self, target, threshold, filters, start=None, end=None):

        batch = self.queryfactory.freq_dist_batch_filters(target, threshold, filters, start=start, end=end)
        self.queries.append(batch)
        return batch

