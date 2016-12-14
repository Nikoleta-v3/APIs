from setuptools import setup, find_packages
import unittest
import doctest

# Read in the version number
exec(open('src/arcas/version.py', 'r').read())

requirements = ["requests==2.12.1",
                "requests_mock==1.1.0",
                "ratelimit==1.1.0",
                "docopt"]

def test_suite():
    """Discover all tests in the tests dir"""
    test_loader = unittest.TestLoader()
    # Read in unit tests
    test_suite = test_loader.discover('tests')

    # Read in doctests from README
    test_suite.addTests(doctest.DocFileSuite('README.md',
                                             optionflags=doctest.ELLIPSIS))
    return test_suite

setup(
    name='arcas',
    version=__version__,
    install_requires=requirements,
    author='Nikoleta Glynatsi',
    author_email=('glynatsine@cardiff.ac.uk'),
    packages=find_packages('src'),
    package_dir={"": "src"},
    scripts=['bin/arcas_scrape'],
    test_suite='setup.test_suite',
    url='',
    license='The MIT License (MIT)',
    description='A library to gather data from academic apis',
)
