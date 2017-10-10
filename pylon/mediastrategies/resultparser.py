import pandas as pd

from pylon.mediastrategies.strategyresult import StrategyResult
from pylon.mediastrategies.groupedstrategyresult import GroupedStrategyResult
from pylon.mediastrategies.audiencebreakdownresult import AudienceBreakdownResult
from pylon.mediastrategies.toptermsresult import *

class ResultParser(object):

    @staticmethod
    def parse_result(strategy, result, result_key, index_keys):
        if strategy == 'audience_breakdown':
            return ResultParser.parse_audience_breakdown_result_group(result['result'])
        elif strategy == 'top_terms':
            return ResultParser.parse_top_terms_result_group(result['result'])
        else:
            return ResultParser.parse_result_group(result['result'], result_key, index_keys)

    @staticmethod
    def parse_grouped_result(strategy, result, result_key, index_keys):
        results = {}

        for group_name, group_result in result['result']['groups'].items():

            if strategy == 'audience_breakdown':
                results[group_name] = ResultParser.parse_audience_breakdown_result_group(group_result)
            else:
                results[group_name] = ResultParser.parse_result_group(group_result, result_key, index_keys)

        return GroupedStrategyResult(results)

    @staticmethod
    def parse_result_group(result, result_key, index_keys):
        if not result['redacted']:
            return StrategyResult(False, pd.DataFrame.from_records(result[result_key], index=index_keys),
                    result['unique_authors'], result['interactions'])
        else:
            return StrategyResult(True)

    @staticmethod
    def parse_top_terms_result_group(result):
        if not result['redacted']:
            topics = {}

            for topic_name, topic_result in result['topics'].items():

                if not topic_result['redacted']:
                    topics[topic_name] = TopTermsTopicResult(False, pd.DataFrame.from_records(topic_result['terms'], index='term'))
                else:
                    topics[topic_name] = TopTermsTopicResult(True)

            return TopTermsResult(False, topics)

        else:
            return StrategyResult(True)

    @staticmethod
    def parse_audience_breakdown_result_group(result):
        if not result['redacted']:
            results = {}

            for dimension, dimension_result in result.items():
                dimension_key = ResultParser.dimension_to_key_name(dimension)

                if not dimension_key is None:
                    results[dimension] = ResultParser.parse_result_group(dimension_result, 'segments', dimension_key)

            return AudienceBreakdownResult(False, results)

        else:
            return StrategyResult(True)

    @staticmethod
    def dimension_to_key_name(dimension):
        targets = {
            'country': 'country',
            'seniorities': 'seniority',
            'functions': 'function',
            'sectors': 'sector',
            'industries': 'industry',
            'company_sizes': 'company_size',
            'custom_segments': 'custom_segment',
            'gender': 'gender',
            'age': 'age',
            'metro_area': 'metro_area',
            'skills': 'skill',
            'occupations': 'occupation'
        }
        return targets.get(dimension, None)