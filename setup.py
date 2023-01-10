import pathlib
from setuptools import setup, find_packages

from os import environ

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

package_name = "web3sdks-sdk"
if "PACKAGE_NAME" in environ:
    package_name = environ["PACKAGE_NAME"]

setup(
    name=package_name,
    version="0.5.0",
    description="Official Web3sdks sdk",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/nftlabs/nftlabs-sdk-python",
    author="Web3sdks",
    author_email="sdk@web3sdks.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "dataclasses-json",
        "web3sdks-web3",
        "requests",
        "web3sdks-contract-wrappers",
        "web3",
        "deprecation"
    ],
    py_modules=["web3sdks", "nftlabs"]
)
