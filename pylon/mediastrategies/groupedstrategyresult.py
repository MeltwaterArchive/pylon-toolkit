from pylon.mediastrategies.strategyresult import StrategyResult


class GroupedStrategyResult(StrategyResult):
    def __init__(self, result, redacted_groups):
        self.result = result
        self.redacted_groups = redacted_groups

    def write_as_csv(self, filepath):
        self.result.to_csv(filepath, encoding='utf-8')