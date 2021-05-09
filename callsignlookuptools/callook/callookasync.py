"""
callooktools: asynchronous editon
---
Copyright 2021 classabbyamp, 0x5c
Released under the terms of the BSD 3-Clause license.
"""


from typing import Optional

import aiohttp

from ..common import mixins, dataclasses, exceptions
from .callook import CallookClientAbc


class CallookAsyncClient(mixins.AsyncMixin, CallookClientAbc):
    """Asynchronous Callook API client

    :param session: An aiohttp session to use for requests
    :type session: Optional[aiohttp.ClientSession]
    """
    def __init__(self, session: Optional[aiohttp.ClientSession] = None):
        self._session = session
        super().__init__()

    async def search(self, callsign: str) -> dataclasses.CallsignData:  # type: ignore
        if not callsign.isalnum():
            raise exceptions.CallsignLookupError("Invalid Callsign")

        return self._process_search(
            query=callsign.upper(),
            resp=await self._do_query(
                callsign=callsign.upper()
            )
        )

    async def _do_query(self, **query) -> bytes:  # type: ignore
        if self._session is None:
            await self.start_session()
        async with self._session.get(self._base_url.format(query["callsign"])) as resp:  # type: ignore
            if resp.status != 200:
                raise exceptions.CallsignLookupError(f"Unable to connect to Callook (HTTP Error {resp.status})")
            return await resp.read()
