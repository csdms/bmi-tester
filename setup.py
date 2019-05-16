#! /usr/bin/env python
from setuptools import find_packages, setup

import versioneer

setup(
    name="bmi-tester",
    version=versioneer.get_version(),
    author="Eric Hutton",
    author_email="eric.hutton@colorado.edu",
    description="Test Python BMI bindings.",
    long_description=open("README.md").read(),
    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Cython",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    install_requires=[
        "cfunits",
        "click",
        "model_metadata",
        "netCDF4",
        "numpy",
        "py-scripting",
        "pytest",
        "standard_names",
    ],
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
