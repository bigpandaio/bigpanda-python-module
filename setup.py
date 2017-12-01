#!/usr/bin/env python

from setuptools import setup

requires = open('requirements.txt').readlines()
setup(name='bigpanda',
      version='2.2',
      description='Python module for integration with BigPanda',
      author='BigPanda',
      author_email='support@bigpanda.io',
      url='https://bigpanda.io',
      packages=['bigpanda'],
      install_requires=requires
)
