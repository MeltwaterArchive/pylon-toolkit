import yaml, os, sys, datasift
from pylon import Analysis

config = yaml.load(open(os.path.join(os.path.dirname(__file__), 'config.yml'), 'r'))

client = datasift.Client(config['username'], config['apikey'], async=True)
pylon = Analysis(client, config['service'], config['recording_id'])

filters = {
    'male': 'li.user.member.gender == "male"',
    'female': 'li.user.member.gender == "female"'
}

batch = pylon.freq_dist_batch_filters('li.user.member.age', 10, filters=filters)
df = batch.run()

print(df)