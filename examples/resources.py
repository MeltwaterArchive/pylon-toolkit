import yaml, os, sys, datasift
from pylon import Resources
from pylon.exceptions import ResourceNotFound

config = yaml.load(open(os.path.join(os.path.dirname(__file__), 'config.yml'), 'r'))
client = datasift.Client(config['username'], config['apikey'], async=True)
resource_client = Resources(client, 'linkedin')

# No filter
print('---- Seniority breakdown, last month -----')
seniorities = resource_client.get('userMemberSeniorities')
print(seniorities.result)

# Period filter
print('---- Seniority breakdown, last week -----')
seniorities_week = resource_client.get('userMemberSeniorities', period='week')
print(seniorities_week.result)

# Country filter
print('---- Seniority breakdown, Germany -----')
german_seniorities = resource_client.get('userMemberSeniorities', country='germany')
print(german_seniorities.result)

# Handle resource not found
try:
    resource_client.get('noSuchSlug')
except ResourceNotFound as e:
    print('Failed to find resource: ' + e.slug)
