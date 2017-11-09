import yaml, os, datasift
from pylon import Strategies

config = yaml.load(open(os.path.join(os.path.dirname(__file__), 'config.yml'), 'r'))

client = datasift.Client(config['username'], config['apikey'], async=True)
strategies = Strategies(client, config['service'], config['recording_id'])

# Example of running a strategy task
params = {
    "keywords": {
        "any": ["cloud"],
    },
    "comparison_audience": "global"
}

task = strategies.top_domains('test', params)
result = task.run()

# Always check to see if the result is redacted
if not result.redacted:

    # result.result is a Pandas dataframe
    print(result.result)

    # Write to CSV file
    result.write_as_csv(os.getcwd() + '/../output.csv')


# Example of handling redacted results
redact_params = {
    "keywords": {
        "any": ["asdasdasdasdasdjlkjlaksd"],
    },
    "comparison_audience": "global"
}

task = strategies.top_urls('test', redact_params)
result = task.run()

if result.redacted:
    print('Result was redacted')
else:
    print('Result was not redacted')

