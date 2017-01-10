import pandas as pd
from collections import defaultdict
from concurrent.futures import as_completed
from time import sleep
from datetime import datetime
import pytz


class Utils:
    @staticmethod
    def flatten_pylon_response(j):
        bucketkeys = ['key', 'unique_authors', 'interactions']
        nestingkey = 'key'  # the name of the key that needs to reflect the nesting

        if 'results' in j:
            retval = list()
            for result in j['results']:
                if 'child' in result:
                    child = Utils.flatten_pylon_response(result['child'])
                    if child:
                        # prepend current value of the nestingkey to that of the child
                        retval += [{k: (result[nestingkey],) + v if k == nestingkey else v
                                    for k, v in bucket.items()}
                                   for bucket in child]
                # tuple-ise the value when the key is the nesting key so we can append to it
                retval.append({k: (v,) if k == nestingkey else v for k, v in result.items() if k in bucketkeys})
            return retval

    @staticmethod
    def extract_targets(j, result):
        if 'target' in j['parameters']:
            result.append(j['parameters']['target'])
        elif 'interval' in j['parameters']:
            result.append('datetime')
        else:
            raise "No target or interval"
        if 'child' in j:
            Utils.extract_targets(j['child'], result)

    @staticmethod
    def cast_(key, names):
        return tuple([datetime.fromtimestamp(i, tz=pytz.UTC) if names[e] == 'datetime' else i
                      for e, i in enumerate(key)])

    @staticmethod
    def pylon_response_to_dataframes(response):
        groups = defaultdict(list)
        for i in Utils.flatten_pylon_response(response['result']['analysis']):
            groups[len(i['key'])].append(i)
        result = list()
        targets = list()
        Utils.extract_targets(response['parameters']['parameters'], targets)
        for g in sorted(groups):
            names = targets[:g]
            index = pd.MultiIndex.from_tuples([Utils.cast_(i['key'], names) for i in groups[g]], names=names)
            result.append(pd.DataFrame([{k: v for k, v in i.items() if k != 'key'} for i in groups[g]],
                                       index=index))
        return result

    @staticmethod
    def join_filters(operator, f1=None, f2=None):

        if f1 is None and f2 is None:
            return None

        if f1 is None:
            f1 = ''

        if f2 is None:
            f2 = ''

        if len(f1) > 0 and len(f2) > 0:
            return '(' + f1 + ') ' + operator + ' (' + f2 + ')'
        elif len(f1) > 0:
            return f1
        elif len(f2) > 0:
            return f2
        else:
            return ''
