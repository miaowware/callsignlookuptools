"""
callsignlookuptools
---
QRZ and callook.info API interface in Python

Copyright 2021 classabbyamp, 0x5c
Released under the terms of the BSD 3-Clause license.
"""


from importlib.util import find_spec

from .__info__ import __version__  # noqa: F401

from .common.dataclasses import CallsignData  # noqa: F401
from .common.exceptions import CallsignLookupError  # noqa: F401

if find_spec("requests"):
    from .qrz.qrzsync import QrzSyncClient  # noqa: F401
    from .callook.callooksync import CallookSyncClient  # noqa: F401
    pass
if find_spec("aiohttp"):
    from .qrz.qrzasync import QrzAsyncClient  # noqa: F401
    from .callook.callookasync import CallookAsyncClient  # noqa: F401
    pass
if not find_spec("requests") and not find_spec("aiohttp"):
    raise ModuleNotFoundError("At least one of requests or aiohttp needs to be installed to use callsignlookuptools")
