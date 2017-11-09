import yaml, os, datasift
from pylon import Strategies

config = yaml.load(open(os.path.join(os.path.dirname(__file__), 'config.yml'), 'r'))

client = datasift.Client(config['username'], config['apikey'], async=True)
strategies = Strategies(client, config['service'], config['recording_id'])

# Example of running a strategy task
params = {
    "topics": {
        "cloud": {
            "any": ["cloud", "azure"]
        },
        "machine learning": {
            "any": ["asdasas"]
        }
    }
}

task = strategies.top_terms('test', params)
result = task.run()

if not result.redacted:
    topic_result = result.topic("cloud")

    if not topic_result.redacted:

        print(topic_result.result)

        # Write to CSV file
        topic_result.write_as_csv(os.getcwd() + '/../output.csv')

    # Inspect overall result
    print(result.result())
    result.write_as_csv(os.getcwd() + '/../output.csv')

else:
    print('Result was redacted')