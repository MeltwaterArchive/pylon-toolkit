from __future__ import absolute_import, division, print_function
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)
##Above lines for compatibility with python27

from pylon.queries.querybase import QueryBase
from pylon.queries.queryresult import QueryResult
from pylon.utils import Utils
from pylon.exceptions import RedactedResults

class Query(QueryBase):
    def __init__(self, config, client, analysis):
        super().__init__(config, client)
        self.analyses = [analysis]

    def result(self):
        if 0 in self.results and self.results[0]['status'] == 'completed':

            if self.results[0]['result']['analysis']['redacted'] or len(self.results[0]['result']['analysis']['results']) == 0:
                raise RedactedResults

            return QueryResult(Utils.pylon_response_to_dataframes(self.results[0])[0],
                self.results[0]['result']['unique_authors'], self.results[0]['result']['interactions'])

