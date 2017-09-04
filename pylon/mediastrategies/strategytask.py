from pylon.tasks import Tasks
from pylon.exceptions import RedactedResults
from pylon.mediastrategies.strategyresult import StrategyResult

import pandas as pd

class StrategyTask(Tasks):
    def __init__(self, config, client, analysis, result_key, index_key):
        super().__init__(config, client)
        self.analyses = [analysis]
        self.result_key = result_key
        self.index_key = index_key

    def result(self):
        if 0 in self.results and self.results[0]['status'] == 'completed':
            return self.parse_result(self.results[0], self.result_key, self.index_key)

    def parse_result(self, result, result_key, index_keys):
        if not result['result']['redacted']:
            return StrategyResult(pd.DataFrame.from_records(result['result'][result_key], index=index_keys))
        else:
            raise RedactedResults