import yaml, os, sys, datasift
from pylon import Analysis

config = yaml.load(open(os.path.join(os.path.dirname(__file__), 'config.yml'), 'r'))

client = datasift.Client(config['username'], config['apikey'], async=True)
pylon = Analysis(client, config['service'], config['recording_id'])

two_level = pylon.nested_freq_dist('Nested example', 'li.user.member.gender', 2, 'li.user.member.age', 5)
print(two_level.run())

three_level = pylon.nested_freq_dist('Nested example', 'li.user.member.country', 2, 'li.user.member.gender', 2, level3='li.user.member.age', threshold3=5)
print(three_level.run())