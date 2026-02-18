"""Setup configuration for rfpintelligence package."""

from setuptools import setup, find_packages

setup(
    name='rfpintelligence',
    version='0.1.0',
    description='RFP Intelligence',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[],
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pytest-cov>=2.0',
        ]
    },
)
