import pathlib
from setuptools import setup, find_packages  # type: ignore
import callsignlookuptools.__info__ as info

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name=info.__project__,
    version=info.__version__,
    description=info.__summary__,
    long_description=README,
    long_description_content_type="text/markdown",
    url=info.__webpage__,
    author=info.__author__,
    author_email=info.__email__,
    license=info.__license__,
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Communications :: Ham Radio",
        "Framework :: AsyncIO",
    ],
    packages=find_packages(exclude=["tests", "docs"]),
    package_data={
        "callsignlookuptools": ["py.typed"]
    },
    install_requires=[
        "lxml",
        "gridtools",
        "pydantic",
        "requests; extra != 'async'"
    ],
    extras_require={
        "cli": ["typer[all]", "click-help-colors"],
        "async": ["aiohttp"],
        "all": ["aiohttp"]
    },
    python_requires=">=3.9",
)
