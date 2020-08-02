#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'enum34;python_version<"3.4"',
    'six',
]

setup_requirements = []

setup(
    name='choicesenum',
    version='0.6.0',
    description="Python's Enum with extra powers to play nice with labels and choices fields",
    long_description=readme + '\n\n' + history,
    author="Fernando Macedo",
    author_email='fgmacedo@gmail.com',
    url='https://github.com/loggi/python-choicesenum',
    packages=find_packages(include=['choicesenum']),
    include_package_data=True,
    install_requires=requirements,
    license="BSD license",
    zip_safe=False,
    keywords='choicesenum',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    setup_requires=setup_requirements,
)
