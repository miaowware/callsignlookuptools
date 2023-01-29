# callsignlookuptools

A [QRZ](https://www.qrz.com), [Callook](https://callook.info), [HamQTH](https://www.hamqth.com), and [QRZCQ](https://www.qrzcq.com) API interface in Python with sync and async support.

[![PyPI](https://img.shields.io/pypi/v/callsignlookuptools)](https://pypi.org/project/callsignlookuptools/) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/callsignlookuptools) ![PyPI - License](https://img.shields.io/pypi/l/callsignlookuptools) [![Documentation Status](https://readthedocs.org/projects/callsignlookuptools/badge/?version=stable)](https://callsignlookuptools.readthedocs.io/en/stable/?badge=stable)

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

**Note:** If `requests`, `aiohttp`, or `typer[all]` and `click-help-colors` are installed another way, you will also have access to the sync, async, or command-line interface, respectively.

## Usage and Documentation

Documentation is available on [ReadTheDocs](https://callsignlookuptools.miaow.io/).

## API Support

Some of the supported callsign lookup APIs require accounts and/or paid subscriptions to be used.

| Site                             | Requirements                                                                                                   |
|----------------------------------|----------------------------------------------------------------------------------------------------------------|
| [QRZ](https://www.qrz.com)       | QRZ account and [XML Logbook Data or QRZ Premium subscription](https://shop.qrz.com/collections/subscriptions) |
| [Callook](https://callook.info)  | None                                                                                                           |
| [HamQTH](https://www.hamqth.com) | HamQTH account                                                                                                 |
| [QRZCQ](https://www.qrzcq.com)   | QRZCQ account and [QRZCQ Premium subscription](https://www.qrzcq.com/page/premium)                             |

## Copyright

Copyright 2021-2023 classabbyamp, 0x5c  
Released under the BSD 3-Clause License.  
See [`LICENSE`](LICENSE) for the full license text.
