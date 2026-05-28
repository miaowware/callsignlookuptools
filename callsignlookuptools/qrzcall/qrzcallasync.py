"""
qrzcalltools: asynchronous edition
---
Released under the terms of the BSD 3-Clause license.
"""


from typing import Optional

import aiohttp

from ..common import mixins, dataclasses, exceptions
from ..common.constants import DEFAULT_USERAGENT
from ..common.functions import is_callsign
from .qrzcall import QrzcallClientAbc


class QrzcallAsyncClient(mixins.AsyncMixin, QrzcallClientAbc):
    """Asynchronous QRZCALL.EU API client

    :param token: QRZCALL.EU Personal Access Token (``pat_…``). Generate one
        at https://qrzcall.eu/ → My Profile → Account → API Tokens. Requires
        a Data or Extra subscription on the account.
    :param useragent: Useragent for QRZCALL.EU
    :param session: An aiohttp session to use for requests
    """
    def __init__(self, token: str, useragent: str = DEFAULT_USERAGENT,
                 session: Optional[aiohttp.ClientSession] = None):
        self._session = session
        super().__init__(token, useragent=useragent)

    @classmethod
    async def new(cls, token: str, useragent: str = DEFAULT_USERAGENT,
                  session: Optional[aiohttp.ClientSession] = None) -> "QrzcallAsyncClient":
        """Creates a ``QrzcallAsyncClient`` and automatically starts a
        session if one is not provided.

        :param token: QRZCALL.EU Personal Access Token (``pat_…``)
        :param useragent: Useragent for QRZCALL.EU
        :param session: An aiohttp session to use for requests
        """
        obj = cls(token, useragent, session)
        if obj.session is None:
            await obj.start_session()
        return obj

    async def search(self, callsign: str) -> dataclasses.CallsignData:  # type: ignore[override]
        if not is_callsign(callsign):
            raise exceptions.CallsignLookupError("Invalid Callsign")
        return self._process_search(
            query=callsign.upper(),
            resp=await self._do_query(callsign=callsign.upper()),
        )

    async def _do_query(self, **query) -> bytes:  # type: ignore[override]
        if self._session is None:
            raise exceptions.CallsignLookupError(
                "No aiohttp session — use QrzcallAsyncClient.new() or call start_session() first"
            )
        headers = {
            "Authorization": f"Bearer {self._token}",
            "User-Agent": self._useragent,
            "Accept": "application/json",
        }
        async with self._session.get(self._base_url, params={"callsign": query["callsign"]},
                                     headers=headers) as resp:
            if resp.status == 200:
                return await resp.read()
            if resp.status == 401:
                raise exceptions.CallsignLookupError(
                    "QRZCALL.EU token is invalid or has been revoked"
                )
            if resp.status == 403:
                raise exceptions.CallsignLookupError(
                    "QRZCALL.EU subscription required (Data or Extra tier)"
                )
            if resp.status == 404:
                raise exceptions.CallsignLookupError(f"{query['callsign']} not found")
            if resp.status == 429:
                raise exceptions.CallsignLookupError("QRZCALL.EU rate limit exceeded")
            raise exceptions.CallsignLookupError(
                f"Unable to connect to QRZCALL.EU (HTTP Error {resp.status})"
            )
