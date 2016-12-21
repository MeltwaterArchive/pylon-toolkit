import logging
import json
import time

from concurrent.futures import as_completed

class QueryBase(object):

    def __init__(self, config, client):
        self.analyses=None #must be initialised to a list in derived classes
        self.config = config
        self.client = client

        self.tasks=dict() # map from analysis index to task
        self.results=dict() # map from analysis index to result

    def start(self):

        promise2index=dict()

        for i, analysis in enumerate(self.analyses):

            logging.info('Posting new analysis task: \n' + json.dumps(analysis))

            name = analysis['name']
            analysis.pop('name', None)

            try:
                promise=self.client.pylon.task.create(
                        subscription_id=self.config.recording_id,
                        parameters=analysis,
                        service=self.config.service,
                        name=name
                    )

                promise2index[promise]=i

            except Exception as exc:
                print(exc)

        for result in as_completed(promise2index): # changes order!
            try:
                self.tasks[promise2index[result]]=result.process()['id']
                logging.debug('Posted task id: ' + self.tasks[promise2index[result]])

            except Exception as exc:
                print(exc)

    def is_pending(self,i):
        return i not in self.results or self.results[i]['status']!="completed"

    def get(self):

        promise2index=dict()

        for i, analysis in enumerate(self.analyses):

            logging.debug('Checking state of analysis task: ' + self.tasks[i])

            if self.is_pending(i):
                try:
                    promise=self.client.pylon.task.get(self.tasks[i],service=self.config.service)
                    promise2index[promise]=i
                except Exception as exc:
                    print(exc)

        for result in as_completed(promise2index): # changes order!
            try:
                self.results[promise2index[result]]=result.process()

                if self.results[promise2index[result]]['status'] == "completed":
                    logging.info('Task completed: ' + self.tasks[i])

            except Exception as exc:
                print(exc)

    def run(self):
        self.start()
        join_queries([self])
        return self.df()

    def status(self):
        retval=dict()

        for i, analysis in enumerate(self.analyses):
            if i in self.tasks:
                if i in self.results:
                    retval[self.tasks[i]]=self.results[i]['status']
                else:
                    retval[self.tasks[i]]='started'
        return retval

    # returns a list of tasks that are pending (started but not complete)
    def pending(self):
        return [self.tasks[i] for i, analysis in enumerate(self.analyses) if i in self.tasks and self.is_pending(i)]

    def wait(self):

        pending=len(self.pending())

        while pending>0:

            t=min(max(pending/2,1),60) # at least 1, at most 60, otherwise #running/2
            time.sleep(t)

            self.get()

            pending=len(self.pending())

    def run(self):
        self.start()
        self.wait()
        return self.df()