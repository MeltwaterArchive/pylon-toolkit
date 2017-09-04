import logging
import pandas as pd

from pylon.mediastrategies.strategytask import StrategyTask
from pylon.exceptions import RedactedResults
from pylon.mediastrategies.groupedstrategyresult import GroupedStrategyResult

logging.basicConfig(format="%(asctime)-15s -- %(message)s", level=logging.INFO)


class GroupedStrategyTask(StrategyTask):

    def parse_result(self, result, result_key, index_keys):

        dfs = []
        names = []
        redacted_groups = []

        for g in result['result']['groups']:
            if not result['result']['groups'][g]['redacted']:
                dfs.append(pd.DataFrame.from_records(result['result']['groups'][g][result_key], index=index_keys))
                names.append(g)
            else:
                logging.warning('Redacted result for group: ' + g)
                redacted_groups.append(g)

        if len(result['result']['groups']) == len(redacted_groups):
            raise RedactedResults
        else:
            return GroupedStrategyResult(pd.concat(dfs, keys=names), redacted_groups)
