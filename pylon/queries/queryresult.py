
class QueryResult(object):

    def __init__(self, result, unique_authors, interactions):
        self.result = result
        self.unique_authors = unique_authors
        self.interactions = interactions