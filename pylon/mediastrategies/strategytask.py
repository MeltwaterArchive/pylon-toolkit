from pylon.tasks import Tasks
from pylon.mediastrategies.resultparser import ResultParser

class StrategyTask(Tasks):
    def __init__(self, config, client, analysis, result_key=None, index_key=None):
        super().__init__(config, client)
        self.analyses = [analysis]
        self.result_key = result_key
        self.index_key = index_key
        self.strategy = analysis['strategy']

    def result(self):
        if 0 in self.results and self.results[0]['status'] == 'completed':
            if 'groups' in self.analyses[0]['parameters']:
                return ResultParser.parse_grouped_result(self.strategy, self.results[0], self.result_key, self.index_key)
            else:
                return ResultParser.parse_result(self.strategy, self.results[0], self.result_key, self.index_key)