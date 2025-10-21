from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="anime-recommender",
    version="0.1",
    author="infernodragon456",
    packages=find_packages(),
    install_requires = requirements,
)