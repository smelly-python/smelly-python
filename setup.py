from setuptools import setup, find_packages

setup (
    name='Smelly Python', 
    version='0.0.1-snapshot',
    packages=find_packages(),
    entry_points = {
        'console_scripts': ['smelly_python=smelly_python.command_line:main'],
    }
)