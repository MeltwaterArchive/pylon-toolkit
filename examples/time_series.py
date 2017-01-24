import yaml, os, sys, datasift
from pylon import Analysis

config = yaml.load(open(os.path.join(os.path.dirname(__file__), 'config.yml'), 'r'))

client = datasift.Client(config['username'], config['apikey'], async=True)
pylon = Analysis(client, config['service'], config['recording_id'])

task = pylon.time_series('ts', 'day')
result = task.run()

print(result.unique_authors)
print(result.interactions)
print(result.result)