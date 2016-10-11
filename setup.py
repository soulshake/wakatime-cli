#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='wakatime-cli',
    version='0.1.0',
    author='AJ Bowen',
    license='MIT',
    author_email='aj@soulshake.net',
    packages=find_packages(),
    description='Wakatime CLI',
    long_description=open('README.rst').read(),
    url='https://github.com/soulshake/wakatime-cli',
    keywords='wakatime cli',
    install_requires=['click==6.0',
                      'arrow==0.5.4',
                      'requests==2.7.0',
                      'tabulate==0.7.5'],
    entry_points="""\
[console_scripts]
swag = wakatime.__main__:main
""",
    )
