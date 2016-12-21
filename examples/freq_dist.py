import yaml, os, sys
from pylon import Analysis

config = yaml.load(open(os.path.join(os.path.dirname(__file__), 'config.yml'), 'r'))

pylon = Analysis(config['username'], config['apikey'], config['service'], config['recording_id'],
    filter='li.user.member.country == "United States"')

task = pylon.freq_dist('Interaction types', 'li.type', filter='li.user.member.gender == "male"')
df = task.run()

print(df)