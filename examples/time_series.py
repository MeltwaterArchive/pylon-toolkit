import yaml, os, sys
from pylon import Analysis

config = yaml.load(open(os.path.join(os.path.dirname(__file__), 'config.yml'), 'r'))

pylon = Analysis(config['username'], config['apikey'], config['service'], config['recording_id'])

task = pylon.time_series('ts', 'day')
df = task.run()
print(df)