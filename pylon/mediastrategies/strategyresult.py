
class StrategyResult:
    def __init__(self, result):
        self.result = result

    def write_as_csv(self, filepath):
        self.result.to_csv(filepath, encoding='utf-8')