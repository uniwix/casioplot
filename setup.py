import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.rst").read_text()

# This call to setup() does all the work
setup(
    name='casioplot',
    version='1.3.1',
    author='uniwix',
    author_email='odevlo.me@gmail.com',
    description='This module allows to use casioplot module on a computer.',
    long_description=README,
    long_description_content_type="text/x-rst",
    url='https://github.com/uniwix/casioplot',
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    project_urls={
        "Bug Tracker": "https://github.com/uniwix/casioplot/issues",
    },
    packages=["casioplot"],
    include_package_data=True,
    install_requires=["Pillow"],
)
