import copy
import logging

logging.basicConfig(format="%(asctime)-15s -- %(message)s", level=logging.INFO)

class StrategyResult:
    def __init__(self, redacted, result=None, unique_authors=None, interactions=None):
        self.result = result
        self.unique_authors = unique_authors
        self.interactions = interactions
        self.redacted = redacted

    def write_as_csv(self, filepath, columns=None):
        if not self.redacted:

            df = copy.deepcopy(self.result)

            if columns is None:
                df.to_csv(filepath, encoding='utf-8', index=True)
            else:
                df = df.reset_index()
                df[columns].to_csv(filepath, encoding='utf-8', index=False)

        else:
            logging.error('Cannot write CSV because result is redacted.')