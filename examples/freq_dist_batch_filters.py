import yaml, os, sys
from pylon import Analysis

config = yaml.load(open(os.path.join(os.path.dirname(__file__), 'config.yml'), 'r'))

pylon = Analysis(config['username'], config['apikey'], config['service'], config['recording_id'],
    filter='li.user.member.country == "United States"')

filters = {
    'male': 'li.user.member.gender == "male"',
    'female': 'li.user.member.gender == "female"'
}

batch = pylon.freq_dist_batch_filters('li.user.member.age', 10, filters=filters)
df = batch.run()

print(df)