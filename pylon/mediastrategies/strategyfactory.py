from pylon.mediastrategies.strategytask import StrategyTask
from pylon.mediastrategies.groupedstrategytask import GroupedStrategyTask

class StrategyFactory(object):

    def __init__(self, config, client):
        self.config = config
        self.client = client

    def strategy_task(self, strategy, version, name, params, result_key, index_key):

        task_params = {
            "name": name,
            "type": "strategy",
            "strategy": strategy,
            "version": version,
            "parameters": params
        }

        if 'groups' in params:
            return GroupedStrategyTask(self.config, self.client, task_params, result_key, index_key)
        else:
            return StrategyTask(self.config, self.client, task_params, result_key, index_key)