import os
from setuptools import setup

requirementPath = 'requirements.txt'

if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()
setup(name="py-patcher", install_requires=install_requires)
