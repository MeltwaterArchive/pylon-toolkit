import pandas as pd
import copy, logging
from pylon.mediastrategies.strategyresult import StrategyResult

logging.basicConfig(format="%(asctime)-15s -- %(message)s", level=logging.INFO)

class AudienceBreakdownResult(StrategyResult):
    def __init__(self, redacted, dimension_results=None):
        self.dimension_results = dimension_results
        self.redacted = redacted

    def dimension(self, dimension_name):
        return self.dimension_results[dimension_name]

    def result(self):
        if not self.redacted:
            dfs = []
            keys = []

            for dimension, dimension_result in self.dimension_results.items():
                if not dimension_result.redacted:
                    dfs.append(dimension_result.result)
                    keys.append(dimension)

            if len(keys) > 0:
                return pd.concat(dfs, keys=keys, names=['dimension', 'segment'])
            else:
                return None

        else:
            return None

    def write_as_csv(self, filepath, group_col_name='dimension'):
        if not self.redacted:

            df = copy.deepcopy(self.result())
            df.index.names = [group_col_name, 'segment'] + df.index.names[2:]
            df.to_csv(filepath, encoding='utf-8', index=True)

        else:
            logging.error('Cannot write CSV because result is redacted.')