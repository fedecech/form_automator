from setuptools import setup
from auto_events.__init__ import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='auto_events',
    version=__version__,
    url="https://github.com/fedecech/auto_events",
    author="Federico Cecchinato",
    author_email="federicocech@gmail.com",  # use icloud fake email
    description="Automate tasks easily using python",
    long_description=long_description,
    license='MIT',
    packages=['auto_events'],
    py_modules=['auto_events'],
    install_requires=[],
    python_requires=">=3.8",
)
