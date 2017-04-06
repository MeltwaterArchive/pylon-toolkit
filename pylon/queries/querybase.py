import json
import logging
import time
from concurrent.futures import as_completed


class QueryBase(object):
    def __init__(self, config, client):
        self.analyses = None  # must be initialised to a list in derived classes
        self.config = config
        self.client = client

        self.tasks = dict()  # map from analysis index to task
        self.results = dict()  # map from analysis index to result

    def start(self):
        promise2index = dict()

        for i, analysis in enumerate(self.analyses):
            logging.debug('Posting new analysis task: \n' + json.dumps(analysis))

            name = analysis['name']
            analysis.pop('name', None)

            promise = self.client.create_task(
                subscription_id=self.config.recording_id,
                parameters=analysis,
                service=self.config.service,
                name=name
            )

            promise2index[promise] = i

        for result in as_completed(promise2index):  # changes order!
            self.tasks[promise2index[result]] = result.process()['id']
            logging.debug('Posted task id: ' + self.tasks[promise2index[result]])

    def is_unfinished(self, i):
        return not self.is_finished(i)

    def is_finished(self, i):
        return self.results.get(i, {}).get("status", None) in ["completed", "failed"]

    def get(self):
        promise2index = dict()

        for i, analysis in enumerate(self.analyses):
            logging.debug('Checking state of analysis task: ' + self.tasks[i])

            if self.is_unfinished(i):
                promise = self.client.get_task(self.tasks[i], service=self.config.service)
                promise2index[promise] = i

        for result in as_completed(promise2index):  # changes order!
            self.results[promise2index[result]] = result.process()

            if self.results[promise2index[result]]['status'] == "completed":
                logging.debug('Task completed: {}'.format(self.tasks[promise2index[result]]))

    def status(self):
        retval = dict()
        for i, analysis in enumerate(self.analyses):
            if i in self.tasks:
                retval[self.tasks[i]] = self.results.get(i, {}).get("status", "started")
        return retval

    def _filter_state(self, fn):
        return [self.tasks[i] for i, analysis in enumerate(self.analyses) if i in self.tasks and fn(i)]

    def unfinished(self):
        return self._filter_state(self.is_unfinished)

    def wait(self):
        unfinished = len(self.unfinished())

        while unfinished > 0:
            t = min(max(unfinished / 2, 1), 60)  # at least 1, at most 60, otherwise #running/2
            time.sleep(t)
            self.get()
            unfinished = len(self.unfinished())

    def result(self):
        raise NotImplementedError()

    def run(self):
        self.start()
        self.wait()
        return self.result()
