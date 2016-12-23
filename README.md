# pylon-toolkit

PYLON analysis utilities, written in Python.

## Requirements

This library has been tested using **Python 3.5.2**.

The `setup.py` file in the root of the repository lists the required pip packages required. You can install all required packages by running:

	python setup.py develop

## Examples

See example of using the library in the `/examples` folder of the repo.

To run the examples you will first need to complete the details in the `/examples/config.yml` file.

## Tests

Install pip packages:

	pip install nose
	pip install coverage

Run tests:

	nosetests

Run tests and report on code coverage:

	nosetests --with-coverage --cover-erase --cover-package=pylon --cover-html