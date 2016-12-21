from pylon.utils import Utils
from pylon.queries.query import Query
from pylon.queries.querybatch import QueryBatch

class QueryFactory(object):

    def __init__(self, config, client, start=None, end=None, filter=None):
        self.config = config
        self.client = client
        self.start = start
        self.end = end
        self.filter = filter

    def complete_params(self, analysis, start=None, end=None, filter=None):

        if(not start is None):
            analysis['start'] = start
        elif(not self.start is None):
            analysis['start'] = self.start

        if(not end is None):
            analysis['end'] = end
        elif(not self.end is None):
            analysis['end'] = self.end

        if (not self.filter is None):
            if(filter is None):
                analysis['filter'] = self.filter
            else:
                analysis['filter'] = Utils.join_filters('AND', self.filter, filter)
        elif(not filter is None):
            analysis['filter'] = filter

    def params_freq_dist(self, name, target, threshold, filter=None, start=None, end=None):

        analysis = {
            "name": name,
            "parameters": {
                "analysis_type": "freqDist",
                "parameters": {
                    "target": target,
                    "threshold": threshold
                }
            }
        }

        self.complete_params(analysis, start=start, end=end, filter=filter)
        return analysis

    def freq_dist(self, name, target, threshold=200, filter=None, start=None, end=None):
        analysis = self.params_freq_dist(name, target, threshold, start=start, end=end, filter=filter)
        return Query(self.config, self.client, analysis)

    def params_time_series(self, name, interval, span=1, filter=None, start=None, end=None):

        analysis = {
            "name": name,
            "parameters": {
                "analysis_type": "timeSeries",
                "parameters": {
                    "interval": interval,
                    "span": span
                }
            }
        }

        self.complete_params(analysis, start=start, end=end, filter=filter)
        return analysis

    def time_series(self, name, interval, span=1, filter=None, start=None, end=None):
        analysis = self.params_time_series(name, interval, span, filter=filter, start=start, end=end)
        return Query(self.config, self.client, analysis)

    def params_nested_freq_dist(self, name, level1, threshold1, level2, threshold2, level3=None, threshold3=None, filter=None, start=None, end=None):

        analysis = {
            "name": name,
            "parameters": {
                "analysis_type": "freqDist",
                "parameters": {
                    "target": level1,
                    "threshold": threshold1
                },
                "child": {
                    "analysis_type": "freqDist",
                    "parameters": {
                        "target": level2,
                        "threshold": threshold2
                    }
                }
            }
        }

        if(not level3 is None):
            if(threshold3 is None):
                raise ArgumentException('threshold3 argument cannot be None when level3 is specified')
            else:
                analysis['parameters']['child']['child'] = {
                    "analysis_type": "freqDist",
                    "parameters": {
                        "target": level3,
                        "threshold": threshold3
                    }
                }

        self.complete_params(analysis, start=start, end=end, filter=filter)
        return analysis

    def nested_freq_dist(self, name, level1, threshold1, level2, threshold2, level3=None, threshold3=None, filter=None, start=None, end=None):
        analysis = self.params_nested_freq_dist(name, level1, threshold1, level2, threshold2, level3=level3, threshold3=threshold3, filter=filter, start=start, end=end)
        return Query(self.config, self.client, analysis)

    def freq_dist_batch_filters(self, target, threshold, filters, start=None, end=None):

        analyses = []

        for n, f in filters.items():
            analyses.append(self.params_freq_dist(n, target, threshold, start=start, end=end, filter=f))

        return QueryBatch(self.config, self.client, analyses)
