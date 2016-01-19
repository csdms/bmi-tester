#! /usr/bin/env python
from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages


setup(name='bmi-tester',
      version='0.1.0',
      author='Eric Hutton',
      author_email='eric.hutton@colorado.edu',
      description='Test Python BMI bindings.',
      long_description=open('README.md').read(),
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'bmi-tester=bmi_tester.cmd:main',
          ]
      }

)
