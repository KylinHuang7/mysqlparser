from setuptools import setup
from setuptools import find_packages


VERSION = '1.0.0'

setup(
    name='mysqlparser',  # package name
    version=VERSION,  # package version
    description='SQL parser',  # package description
    packages=find_packages(),
    zip_safe=False,
)
