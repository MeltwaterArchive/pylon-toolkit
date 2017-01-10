from pylon.queries.querybase import QueryBase
from pylon.utils import Utils


class Query(QueryBase):
    def __init__(self, config, client, analysis):
        super().__init__(config, client)
        self.analyses = [analysis]

    def df(self, level=-1):
        if 0 in self.results and self.results[0]['status'] == 'completed':
            if self.results[0]['result']['analysis']['redacted']:
                raise RedactedResults
            return Utils.pylon_response_to_dataframes(self.results[0])[level]

class RedactedResults(Exception):
    pass
