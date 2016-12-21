from pylon.queries.querybase import QueryBase
from pylon.utils import Utils

import pandas as pd

class QueryBatch(QueryBase):

    def __init__(self, config, client, analyses, filter=None, start=None, end=None):
        super().__init__(config, client)
        self.analyses=analyses

    def df(self,index_names=[],level=-1):
        dfs=list()
        keys=list()

        for i, analysis in enumerate(self.analyses):
            if i in self.results and self.results[i]['status']=='completed':
                x=Utils.pylon_response_to_dataframes(self.results[i])
                dfs.append(x[level] if len(x)>0 else None)
                keys.append(self.results[i]['name'])

        if dfs:
            if len(index_names)==0:
                if isinstance(keys[0],tuple):
                        index_names=['level_%i' % e for e,i in enumerate(keys[0])]
                else:
                    index_names=['level_0']
            index_names+=dfs[0].index.names
            return pd.concat(dfs,keys=keys,names=index_names)