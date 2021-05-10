# callsignlookuptools

An API interface for various ham radio callsign lookup sites in Python, including [QRZ](https://qrz.com) and [callook.info](https://callook.info)

[![PyPI](https://img.shields.io/pypi/v/callsignlookuptools)](https://pypi.org/project/callsignlookuptools/) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/callsignlookuptools) ![PyPI - License](https://img.shields.io/pypi/l/callsignlookuptools) [![Documentation Status](https://readthedocs.org/projects/callsignlookuptools/badge/?version=latest)](https://callsignlookuptools.readthedocs.io/en/latest/?badge=latest)

## Installation

`callsignlookuptools` requires Python 3.9 at minimum.

```sh
# synchronous requests only
$ pip install callsignlookuptools

# asynchronous aiohttp only
$ pip install callsignlookuptools[async]

# both sync and async
$ pip install callsignlookuptools[all]

# enable the CLI
$ pip install callsignlookuptools[cli]
```

**Note:** If `requests`, `aiohttp`, or `rich` are installed another way, you will also have access to the sync, async, or command-line interface, respectively.

## Documentation

Documentation is available on [ReadTheDocs](https://callsignlookuptools.miaow.io/).

## Copyright

Copyright 2021 classabbyamp, 0x5c  
Released under the BSD 3-Clause License.  
See [`LICENSE`](LICENSE) for the full license text.
