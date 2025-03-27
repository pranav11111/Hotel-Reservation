from setuptools import setup, find_packages


with open('requirements.txt') as f:
    requiremnts = f.read().splitlines() 


setup(
    name = "Hotel Reservation",
    version = '0.0.1',
    author= 'Pranav',
    packages= find_packages(),
    install_requires = requiremnts
)