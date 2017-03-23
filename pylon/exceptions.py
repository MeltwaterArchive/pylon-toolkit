class RedactedResults(Exception):
    pass

class ResourceNotFound(Exception):
    def __init__(self, message, slug, period, country):
        super(ResourceNotFound, self).__init__(message)
        self.slug = slug
        self.period = period
        self.country = country