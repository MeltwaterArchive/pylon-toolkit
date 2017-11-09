import yaml, os, datasift
from pylon.exceptions import RedactedResults
from pylon import Strategies

config = yaml.load(open(os.path.join(os.path.dirname(__file__), 'config.yml'), 'r'))

client = datasift.Client(config['username'], config['apikey'], async=True)
strategies = Strategies(client, config['service'], config['recording_id'])

# Example of running a grouped strategy task
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

# Inspect individual result
group_result = result.group("Senior Govt Admin")

if not group_result.redacted:

    # result.result is a Pandas dataframe
    print(group_result.result)

    # Write to CSV file
    group_result.write_as_csv(os.getcwd() + '/../output.csv')

group_result_2 = result.group("Will redact")

if group_result_2.redacted:
    print('Group result is redacted')

# Inspect overall result
print(result.result())

# Write to CSV file
result.write_as_csv(os.getcwd() + '/../output.csv')
