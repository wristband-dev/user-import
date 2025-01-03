# setup.py
from setuptools import setup, find_packages

setup(
    name='wristband-user-import',
    version='3.0.2',
    description='A package for fetching data from the Wristband API',
    author='Donato Di Ferdinando',
    author_email='fddiferd@gmail.com',
    url='https://github.com/wristband-dev/user-import.git',
    packages=find_packages(),
    # entry_points={
    #     'console_scripts': [
    #         'create_token=wristband.oauth2:main',
    #     ],
    # },
    install_requires=[
        'requests', 'pandas', 'python-dotenv'
    ],  # Add any dependencies here
)
