"""
callooktools: synchronous editon
---
Copyright 2021-2023 classabbyamp, 0x5c
Released under the terms of the BSD 3-Clause license.
"""


from typing import Optional

import requests

from ..common import mixins, dataclasses, exceptions
from ..common.functions import is_callsign
from .callook import CallookClientAbc


class CallookSyncClient(mixins.SyncMixin, CallookClientAbc):
    """Synchronous Callook API client

    :param session: A requests session to use for requests
    """
    def __init__(self, session: Optional[requests.Session] = None):
        if session is None:
            self._session = requests.Session()
        else:
            self._session = session
        super().__init__()

    def search(self, callsign: str) -> dataclasses.CallsignData:
        if not is_callsign(callsign):
            raise exceptions.CallsignLookupError("Invalid Callsign")

        return self._process_search(
            query=callsign.upper(),
            resp=self._do_query(
                callsign=callsign.upper()
            )
        )

    def _do_query(self, **query) -> bytes:
        with self._session.get(self._base_url.format(query["callsign"])) as resp:
            if resp.status_code != 200:
                raise exceptions.CallsignLookupError(f"Unable to connect to Callook (HTTP Error {resp.status_code})")
            return resp.content
