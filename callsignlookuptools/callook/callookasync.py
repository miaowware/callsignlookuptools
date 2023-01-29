"""
callooktools: asynchronous editon
---
Copyright 2021-2023 classabbyamp, 0x5c
Released under the terms of the BSD 3-Clause license.
"""


from typing import Optional

import aiohttp

from ..common import mixins, dataclasses, exceptions
from ..common.functions import is_callsign
from .callook import CallookClientAbc


class CallookAsyncClient(mixins.AsyncMixin, CallookClientAbc):
    """Asynchronous Callook API client

    :param session: An aiohttp session to use for requests
    """
    def __init__(self, session: Optional[aiohttp.ClientSession] = None):
        self._session = session
        super().__init__()

    @classmethod
    async def new(cls, session: Optional[aiohttp.ClientSession] = None) -> 'CallookAsyncClient':
        """Creates a ``CallookAsyncClient`` object and automatically starts a session if not provided.

        :param session: An aiohttp session to use for requests
        """
        obj = cls(session)
        if obj.session is None:
            await obj.start_session()
        return obj

    async def search(self, callsign: str) -> dataclasses.CallsignData:  # type: ignore[override]
        if not is_callsign(callsign):
            raise exceptions.CallsignLookupError("Invalid Callsign")

        return self._process_search(
            query=callsign.upper(),
            resp=await self._do_query(
                callsign=callsign.upper()
            )
        )

    async def _do_query(self, **query) -> bytes:  # type: ignore[override]
        if self._session is not None:
            async with self._session.get(self._base_url.format(query["callsign"])) as resp:
                if resp.status != 200:
                    raise exceptions.CallsignLookupError(f"Unable to connect to Callook (HTTP Error {resp.status})")
                return await resp.read()
        else:
            raise exceptions.CallsignLookupError(("Session not initialised. "
                                                  "Hint: Call `.start_session()` once or use the `new()` classmethod."))
