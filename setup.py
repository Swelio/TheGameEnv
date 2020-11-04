import os

import setuptools

import the_game

with open(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"), "r"
) as description_file:
    long_description = description_file.read()

setuptools.setup(
    name=the_game.__package_name__,
    description=the_game.__description__,
    long_description=long_description,
    version=the_game.__version__,
    author=the_game.__author__,
    license=the_game.__license__,
    url=the_game.__url__,
    python_requires="",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[],
)
