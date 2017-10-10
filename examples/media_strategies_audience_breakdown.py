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
    "dimensions": ["occupations", "functions"],
    "comparison_audience": "global"
}

task = strategies.audience_breakdown('test', params)
result = task.run()

# Check overall result is not redacted
if not result.redacted:

    # Inspect individual dimension result
    dimension_result = result.dimension("occupations")

    if not dimension_result.redacted:

        # result.result is a Pandas dataframe
        print(dimension_result.result)

        # Write to CSV file
        dimension_result.write_as_csv(os.getcwd() + '/../output.csv')

    # Inspect overall result
    print(result.result())

    # Write to CSV file
    result.write_as_csv(os.getcwd() + '/../output.csv')

else:
    print('Overall result redacted')

