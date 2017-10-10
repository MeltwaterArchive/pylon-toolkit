from pylon.mediastrategies.strategytask import StrategyTask

class StrategyFactory(object):

    def __init__(self, config, client):
        self.config = config
        self.client = client

    def strategy_task(self, strategy, version, name, params, result_key=None, index_key=None):

        task_params = {
            "name": name,
            "type": "strategy",
            "strategy": strategy,
            "version": version,
            "parameters": params
        }

        return StrategyTask(self.config, self.client, task_params, result_key, index_key)