import logging
import time

from pylon.clientwrapper import ClientWrapper
from pylon.pylonanalysis.analysistaskfactory import AnalysisTaskFactory

logging.basicConfig(format="%(asctime)-15s -- %(message)s", level=logging.INFO)


class Analysis(object):
    def __init__(
            self,
            client,
            service,
            recording_id,
            start=None,
            end=None,
            filter=None,
            sleep_interval=1,
            max_sleep_interval=60
    ):
        class Config(object):
            def __init__(
                    self,
                    service,
                    recording_id,
                    start=None,
                    end=None,
                    filter=None,
                    sleep_interval=1,
                    max_sleep_interval=60
            ):
                self.service = service
                self.recording_id = recording_id
                self.start = start
                self.end = end
                self.filter = filter
                self.sleep_interval = sleep_interval
                self.max_sleep_interval = max_sleep_interval
                self.task_type = 'analysis'

        self.config = Config(service, recording_id, start, end, filter, sleep_interval, max_sleep_interval)
        self.client = ClientWrapper(client)
        self.factory = AnalysisTaskFactory(self.config, self.client, start=self.config.start, end=self.config.end,
                                         filter=self.config.filter)
        self.tasks = []

    def clear(self):
        self.tasks = []

    def _unfinished(self):
        return [i for task in self.tasks for i in task.unfinished()]

    def waitAll(self):
        logging.debug('Waiting completion of all tasks.')

        while len(self._unfinished()) > 0:
            time.sleep(self.config.sleep_interval)

            for i in self.tasks:
                i.get()

    ############################### Individual analysis tasks ###########################################

    def freq_dist(self, name, target, threshold=200, filter=None, start=None, end=None):
        task = self.factory.freq_dist(name, target, threshold=threshold, start=start, end=end, filter=filter)
        self.tasks.append(task)
        return task

    def time_series(self, name, interval, span=1, filter=None, start=None, end=None):
        task = self.factory.time_series(name, interval, span=span, start=start, end=end, filter=filter)
        self.tasks.append(task)
        return task

    def nested_freq_dist(self, name, level1, threshold1, level2, threshold2, level3=None, threshold3=None, filter=None,
                         start=None, end=None):
        task = self.factory.nested_freq_dist(name, level1, threshold1, level2, threshold2, level3=level3,
                                                   threshold3=threshold3, start=start, end=end, filter=filter)
        self.tasks.append(task)
        return task

    # ############################### Batch analysis tasks ###########################################

    def freq_dist_batch_filters(self, target, threshold, filters, start=None, end=None):
        batch = self.factory.freq_dist_batch_filters(target, threshold, filters, start=start, end=end)
        self.tasks.append(batch)
        return batch
