import logging, copy
import pandas as pd
from pylon.mediastrategies.strategyresult import StrategyResult

logging.basicConfig(format="%(asctime)-15s -- %(message)s", level=logging.INFO)


class TopTermsTopicResult():
    def __init__(self, redacted, result=None):
        self.result = result
        self.redacted = redacted

    def write_as_csv(self, filepath):
        if not self.redacted:
            df = copy.deepcopy(self.result)
            df.to_csv(filepath, encoding='utf-8', index=True)
        else:
            logging.error('Cannot write CSV because result is redacted.')

class TopTermsResult(StrategyResult):
    def __init__(self, redacted, topic_results):
        self.topic_results = topic_results
        self.redacted = redacted

    def topic(self, topic_name):
        return self.topic_results[topic_name]

    def result(self):
        if not self.redacted:
            dfs = []
            keys = []

            for topic_name, topic_result in self.topic_results.items():
                if not topic_result.redacted:
                    keys.append(topic_name)
                    dfs.append(topic_result.result)

            if len(keys) > 0:
                return pd.concat(dfs, keys=keys)
            else:
                return None

        else:
            return None

    def write_as_csv(self, filepath, group_col_name='topic'):
        if not self.redacted:

            df = copy.deepcopy(self.result())
            df.index.names = [group_col_name, 'term'] + df.index.names[2:]
            df.to_csv(filepath, encoding='utf-8', index=True)

        else:
            logging.error('Cannot write CSV because result is redacted.')
