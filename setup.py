# encoding: utf-8

from setuptools import setup
import os.path

setup(
    name="pylon-toolkit",
    version="0.1.0",
    author="DataSift",
    author_email="developers@datasift.com",
    maintainer="DataSift",
    maintainer_email="developers@datasift.com",
    description="Analysis utilities for PYLON.",
    long_description = os.path.isfile("README.md") and open('README.md').read() or None,
    license=(
        "Copyright (C) 2012-Present by MediaSift Ltd. "
        "All Rights Reserved. "
    ),
    url="https://github.com/datasift/pylon-toolkit",
    packages=['pylon'],
    install_requires=[
        'pandas == 0.19.1',
        'datasift == 2.10.0',
        'PyYAML == 3.12'
    ],
    tests_require=[]
)