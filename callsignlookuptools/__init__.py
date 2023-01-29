"""
callsignlookuptools
---
QRZ and callook.info API interface in Python

Copyright 2021-2023 classabbyamp, 0x5c
Released under the terms of the BSD 3-Clause license.
"""


from importlib.util import find_spec

from .__info__ import __version__

from .common.dataclasses import CallsignData
from .common.exceptions import CallsignLookupError

if find_spec("requests"):
    from .qrz.qrzsync import QrzSyncClient
    from .callook.callooksync import CallookSyncClient
    from .hamqth.hamqthsync import HamQthSyncClient
    from .qrzcq.qrzcqsync import QrzCqSyncClient
    pass
if find_spec("aiohttp"):
    from .qrz.qrzasync import QrzAsyncClient
    from .callook.callookasync import CallookAsyncClient
    from .hamqth.hamqthasync import HamQthAsyncClient
    from .qrzcq.qrzcqasync import QrzCqAsyncClient
    pass
if not find_spec("requests") and not find_spec("aiohttp"):
    raise ModuleNotFoundError("At least one of requests or aiohttp needs to be installed to use callsignlookuptools")
