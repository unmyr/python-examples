"""Example of setup.py."""
import setuptools


setuptools.setup(
    name="example-package",
    version="0.0.1",
    packages=setuptools.find_packages(
        include=["example_package"]
    )
)
