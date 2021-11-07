from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='casioplot',
    version='1.0.9',
    author='uniwix',
    author_email='odevlo.me@gmail.com',
    description='This module allows to use casioplot module on a computer.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/uniwix/casioplot',
    project_urls={
        "Bug Tracker": "https://github.com/uniwix/casioplot/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    package_data={
        "": ["images/*.png"],
    },
    include_package_data=True,
    python_requires=">=3.10",

)
