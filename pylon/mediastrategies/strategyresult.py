import copy

class StrategyResult:
    def __init__(self, result):
        self.result = result

    def write_as_csv(self, filepath, columns=None):
        df = copy.deepcopy(self.result)

        if columns is None:
            df.to_csv(filepath, encoding='utf-8', index=True)
        else:
            df = df.reset_index()
            df[columns].to_csv(filepath, encoding='utf-8', index=False)