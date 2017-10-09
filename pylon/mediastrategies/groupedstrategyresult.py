import copy
from pylon.mediastrategies.strategyresult import StrategyResult


class GroupedStrategyResult(StrategyResult):
    def __init__(self, result, redacted_groups):
        self.result = result
        self.redacted_groups = redacted_groups

    def write_as_csv(self, filepath, group_col_name=None, columns=None):
        df = copy.deepcopy(self.result)

        if not group_col_name is None:
            df.index.names = [group_col_name] + df.index.names[1:]

        if columns is None:
            df.to_csv(filepath, encoding='utf-8', index=True)
        else:
            df = df.reset_index()
            df[columns].to_csv(filepath, encoding='utf-8', index=False)