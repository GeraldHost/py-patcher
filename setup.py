import os
from setuptools import setup

requirementPath = 'requirements.txt'

if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()


setup(
        name="py-patcher", 
        packages=["pypatcher"],
        entry_points={
            "console_scripts": ['pypatcher = pypatcher.pypatcher:run']
        },
        install_requires=install_requires)
