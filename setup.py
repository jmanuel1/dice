# Borrowed from
# https://pythonhosted.org/an_example_pypi_project/setuptools.html

import os
from setuptools import setup, find_packages


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="dice",
    version="0.0.1",
    author="Jason Manuel",
    author_email="jama.indo@hotmail.com",
    description=("A D&D dice roller CLI written in Python."),
    license="MIT",
    keywords="dice d&d cli",
    url="https://github.com/jmanuel1/dice",
    packages=find_packages(),
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Topic :: Games/Entertainment :: Board Games"
    ],
    entry_points={
        'console_scripts': [
            'dice = dice:main'
        ]
    }
)
