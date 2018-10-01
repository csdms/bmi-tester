#! /usr/bin/env python
from setuptools import setup, find_packages

import versioneer


setup(
    name="bmi-tester",
    version=versioneer.get_version(),
    author="Eric Hutton",
    author_email="eric.hutton@colorado.edu",
    description="Test Python BMI bindings.",
    long_description=open("README.md").read(),
    packages=find_packages(),
    cmdclass=versioneer.get_cmdclass(),
    entry_points={
        "console_scripts": [
            # 'bmi-tester=bmi_tester.cmd:main',
            "bmi-test=bmi_tester.bmipytest:main"
        ],
        "bmi.plugins": ["bmi_test=bmi_tester.bmipytest:configure_parser_test"],
    },
)
