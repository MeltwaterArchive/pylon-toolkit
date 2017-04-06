import logging

from datasift.exceptions import DataSiftApiException
from pylon.exceptions import ResourceNotFound
from pylon.queries.clientwrapper import ClientWrapper
from pylon.queries.queryresult import QueryResult
from pylon.utils import Utils


logging.basicConfig(format="%(asctime)-15s -- %(message)s", level=logging.INFO)


class Resources(object):
    def __init__(self, client, service):
        self.client = ClientWrapper(client)
        self.service = service

    def get(self, slug, period=None, country=None):

        try:
            resource = self.client.get_resource(slug, service=self.service, period=period, country=country).process()

            return QueryResult(Utils.pylon_response_to_dataframes(resource)[0],
                               resource['result']['unique_authors'], resource['result']['interactions'])

        except DataSiftApiException as e:

            if e.response.status_code == 404:
                logging.warning(
                    'The requested resource was not found (slug: {0}, period: {1}, country: {2})'.format(slug, period,
                                                                                                         country))
                raise ResourceNotFound('The requested resource was not found.', slug, period, country)
            else:
                logging.warning('Failed to fetch resource: ' + str(e.response.status_code) + ', ' + str(e))
                raise e
