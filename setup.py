# setup.py
from setuptools import setup, find_packages

setup(
    name='wristband',
    version='3.0.1',
    description='A package for fetching data from the Withings API',
    author='Donato Di Ferdinando',
    author_email='fddiferd@gmail.com',
    url='https://github.com/wristband-dev/wristband-python.git',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'create_token=wristband.oauth2:main',
        ],
    },
    install_requires=[
        'requests', 'pandas'
    ],  # Add any dependencies here
)
