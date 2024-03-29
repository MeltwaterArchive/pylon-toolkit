import pandas as pd
from pylon.tasks import Tasks
from pylon.pylonanalysis.analysisresult import AnalysisResult
from pylon.utils import Utils


class AnalysisBatch(Tasks):
    def __init__(self, config, client, analyses):
        super().__init__(config, client)
        self.analyses = analyses

    def result(self, index_names=[], level=-1):
        dfs = list()
        keys = list()
        unique_authors = 0
        interactions = 0

        for i, analysis in enumerate(self.analyses):
            if i in self.results and self.results[i]['status'] == 'completed':
                x = Utils.pylon_response_to_dataframes(self.results[i])
                dfs.append(x[level] if len(x) > 0 else None)
                keys.append(self.results[i]['name'])
                unique_authors += self.results[i]['result']['unique_authors']
                interactions += self.results[i]['result']['interactions']

        if dfs:
            if len(index_names) == 0:
                if isinstance(keys[0], tuple):
                    index_names = ['level_%i' % e for e, i in enumerate(keys[0])]
                else:
                    index_names = ['level_0']

            index_names += dfs[0].index.names

            return AnalysisResult(pd.concat(dfs, keys=keys, names=index_names),
                               unique_authors, interactions)
