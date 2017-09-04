import yaml, os, datasift
from pylon.exceptions import RedactedResults
from pylon import Strategies

config = yaml.load(open(os.path.join(os.path.dirname(__file__), 'config.yml'), 'r'))

client = datasift.Client(config['username'], config['apikey'], async=True)
strategies = Strategies(client, config['service'], config['recording_id'])

# Example of running a strategy task
params = {
    "groups": {
        "custom": {
            "Senior Govt Admin": {
                "audience": {
                    "industries": ["government administration"],
                    "seniorities": ["vp", "cxo", "partner", "director", "senior"]
                }
            },
            "Will redact": {
                "keywords": {
                    "any": ["asdasdasdaasadsa"]
                }
            }
        }
    },
    "comparison_audience": "global"
}

task = strategies.top_domains('test', params)
result = task.run()

print('The following groups had redacted results: ')
print(result.redacted_groups)

# result.result is a Pandas dataframe
# print(result.result)

# Write to CSV file
result.write_as_csv(os.getcwd() + '/output.csv')

# Example of handling redacted results
redact_params = {
    "groups": {
        "custom": {
            "Will redact": {
                "keywords": {
                    "any": ["asdasdasdaasadsa"]
                }
            }
        }
    },
    "comparison_audience": "global"
}

try:
    task = strategies.top_urls('test', redact_params)
    result = task.run()
except RedactedResults as e:
    print('Result was redacted')
