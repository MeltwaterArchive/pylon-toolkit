import yaml, os, sys, datasift
from pylon import Analysis

config = yaml.load(open(os.path.join(os.path.dirname(__file__), 'config.yml'), 'r'))

client = datasift.Client(config['username'], config['apikey'], async=True)
pylon = Analysis(client, config['service'], config['recording_id'])

task1 = pylon.freq_dist('Interaction types', 'li.type')
task2 = pylon.freq_dist('Interaction types', 'li.subtype')

task1.start()
task2.start()
pylon.waitAll()

print(task1.df())
print(task2.df())