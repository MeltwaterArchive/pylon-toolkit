import yaml, os, sys, datasift
from pylon import Analysis

config = yaml.load(open(os.path.join(os.path.dirname(__file__), 'config.yml'), 'r'))

client = datasift.Client(config['username'], config['apikey'], async=True)
pylon = Analysis(client, config['service'], config['recording_id'], filter='li.user.member.country == "United States"')

task = pylon.freq_dist('Interaction types', 'li.type', filter='li.user.member.gender == "male"')
df = task.run()

print(df)