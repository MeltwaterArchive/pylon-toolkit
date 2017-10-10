import copy
import pandas as pd

class GroupedStrategyResult(object):
    def __init__(self, group_results):
        self.group_results = group_results

    def group(self, group_name):
        return self.group_results[group_name]

    def result(self):
        dfs = []
        keys = []

        for group_name, group_result in self.group_results.items():
            if not group_result.redacted:
                keys.append(group_name)

                # Handles result types with result property or result method
                result_op = getattr(group_result, "result", None)
                if callable(result_op):
                    dfs.append(group_result.result())
                else:
                    dfs.append(group_result.result)

        if len(keys) > 0:
            return pd.concat(dfs, keys=keys)
        else:
            return None


    def write_as_csv(self, filepath, group_col_name=None, columns=None):

        df = copy.deepcopy(self.result())

        if not group_col_name is None:
            df.index.names = [group_col_name] + df.index.names[1:]

        if columns is None:
            df.to_csv(filepath, encoding='utf-8', index=True)
        else:
            df = df.reset_index()
            df[columns].to_csv(filepath, encoding='utf-8', index=False)