from pylon.exceptions import RedactedResults
from pylon.tasks import Tasks
from pylon.pylonanalysis.analysisresult import AnalysisResult
from pylon.utils import Utils


class AnalysisTask(Tasks):
    def __init__(self, config, client, analysis):
        super().__init__(config, client)
        self.analyses = [analysis]

    def result(self):
        if 0 in self.results and self.results[0]['status'] == 'completed':

            if self.results[0]['result']['analysis']['redacted'] or len(
                    self.results[0]['result']['analysis']['results']) == 0:
                raise RedactedResults

            return AnalysisResult(Utils.pylon_response_to_dataframes(self.results[0])[0],
                               self.results[0]['result']['unique_authors'], self.results[0]['result']['interactions'])
