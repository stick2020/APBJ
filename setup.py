__author__ = 'stick2020'

from setuptools import setup
import ast
import re


_version_re = re.compile(r'__version__\s+=\s+(.*)'),

with open('apbj/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(name='apbj',
        version = version,
        description='',
        author='stick2020',
        author_email='stick2020@yahoo.com.com',
        packages=['apbj'],
        test_suite='nose.collector',
        tests_requires=['nose'])
