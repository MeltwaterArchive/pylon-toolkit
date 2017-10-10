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
    "dimensions": ["functions", "occupations"],
    "comparison_audience": "global",
    "groups": {
        "custom": {
            "Senior Govt Admin": {
                "audience": {
                    "industries": ["government administration"],
                    "seniorities": ["vp", "cxo", "partner", "director", "senior"]
                }
            },
            "IT decision makers": {
                "audience": {
                    "sectors": ["high-tech"],
                    "seniorities": ["vp", "cxo", "partner", "director", "senior"]
                }
            },
            "Will redact": {
                "keywords": {
                    "any": ["asdasdasdaasadsa"]
                }
            }
        }
    }
}

task = strategies.audience_breakdown('test', params)
result = task.run()

# Inspect individual result
group_result = result.group("Senior Govt Admin")

if not group_result.redacted:

    # Inspect individual dimension result
    dimension_result = group_result.dimension("functions")

    if not dimension_result.redacted:

        print(dimension_result.result)

        # Write to CSV file
        dimension_result.write_as_csv(os.getcwd() + '/../output.csv')

    # Inspect overall group result
    print(group_result.result())

    # Write to CSV file
    group_result.write_as_csv(os.getcwd() + '/../output.csv')

else:
    print('Group result was redacted')

# Inspect overall result
print(result.result())

# Write to CSV file
result.write_as_csv(os.getcwd() + '/../output.csv')