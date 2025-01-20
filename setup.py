"""Python setup.py for portfolio_manager package"""
import io
import os
from setuptools import find_packages, setup


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("portfolio_manager", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="portfolio_manager",
    version=read("portfolio_manager", "VERSION"),
    description="Awesome portfolio_manager created by ekinbasarkomur",
    url="https://github.com/ekinbasarkomur/portfolio_manager/",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="ekinbasarkomur",
    packages=find_packages(exclude=["tests", ".github"]),
    install_requires=read_requirements("requirements.txt"),
    entry_points={
        "console_scripts": ["portfolio_manager = portfolio_manager.__main__:main"]
    },
    #extras_require={"test": read_requirements("requirements-test.txt")},
)