import logging, time
from pylon.clientwrapper import ClientWrapper
from pylon.mediastrategies.strategyfactory import StrategyFactory

logging.basicConfig(format="%(asctime)-15s -- %(message)s", level=logging.INFO)


class Strategies(object):
    def __init__(
            self,
            client,
            service,
            recording_id,
            sleep_interval=1,
            max_sleep_interval=60
    ):
        class Config(object):
            def __init__(
                    self,
                    service,
                    recording_id,
                    sleep_interval=1,
                    max_sleep_interval=60
            ):
                self.service = service
                self.recording_id = recording_id
                self.sleep_interval = sleep_interval
                self.max_sleep_interval = max_sleep_interval
                self.task_type='strategy'

        self.config = Config(service, recording_id, sleep_interval, max_sleep_interval)
        self.client = ClientWrapper(client)
        self.factory = StrategyFactory(self.config, self.client)
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

    ############################### Individual tasks ###########################################

    def top_urls(self, name, params, version=1):
        task = self.factory.strategy_task('top_urls', version, name, params, 'urls', 'url')
        self.tasks.append(task)
        return task

    def top_domains(self, name, params, version=1):
        task = self.factory.strategy_task('top_domains', version, name, params, 'domains', 'domain')
        self.tasks.append(task)
        return task

    def top_company_mentions(self, name, params, version=1):
        task = self.factory.strategy_task('top_company_mentions', version, name, params, 'company_mentions', 'company')
        self.tasks.append(task)
        return task

    def top_concepts(self, name, params, version=1):
        task = self.factory.strategy_task('top_concepts', version, name, params, 'concepts', ['concept_type', 'concept_name'])
        self.tasks.append(task)
        return task

    def audience_breakdown(self, name, params, version=1):
        task = self.factory.strategy_task('audience_breakdown', version, name, params)
        self.tasks.append(task)
        return task

    def top_terms(self, name, params, version=1):
        task = self.factory.strategy_task('top_terms', version, name, params)
        self.tasks.append(task)
        return task