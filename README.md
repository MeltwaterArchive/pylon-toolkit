# pylon-toolkit

PYLON analysis utilities, written in Python.

## Requirements

This library has been tested using **Python 3.5.2**.

Additional required libraries:

* [DataSift Python client library](https://github.com/datasift/datasift-python)

		pip install datasift

* Recent version of pyOpenSSL

		pip install pyOpenSSL==16.2.0

## Usage

To make a PYLON analysis request.

1. Install the requirements listed above.

2. Create a DataSift client.

		import datasift

		client = datasift.Client(YOUR_USERNAME, YOUR_API_KEY, async=True)

3. To make a PYLON analysis request.

		# Import handler for PYLON analysis requests
		from pylon import Analysis

		pylon = Analysis(client, 'linkedin', RECORDING_ID, filter='li.user.member.country == "United States"')

		task = pylon.freq_dist('Interaction types', 'li.type', filter='li.user.member.gender == "male"')

		result = task.run()

## Examples

See example of using the library in the `/examples` folder of the repo.

To run the examples you will first need to complete the details in the `/examples/config.yml` file.
