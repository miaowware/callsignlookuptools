"""
hamqthtools: asynchronous editon
---
Copyright 2021-2023 classabbyamp, 0x5c
Released under the terms of the BSD 3-Clause license.
"""


from typing import Optional
from urllib.parse import urlencode

import aiohttp

from ..common import mixins, dataclasses, exceptions
from ..common.constants import DEFAULT_USERAGENT
from ..common.functions import is_callsign
from .hamqth import HamQthClientAbc


class HamQthAsyncClient(mixins.AsyncXmlAuthMixin, mixins.AsyncMixin, HamQthClientAbc):
    """Asynchronous HamQTH API client

    :param username: HamQTH username
    :param password: HamQTH password
    :param session_key: HamQTH login session key
    :param useragent: Useragent for HamQTH
    :param session: An aiohttp session to use for requests
    """
    def __init__(self, username: str, password: str, session_key: str = "",
                 useragent: str = DEFAULT_USERAGENT,
                 session: Optional[aiohttp.ClientSession] = None):
        self._session = session
        super().__init__(username, password, session_key=session_key, useragent=useragent)

    @classmethod
    async def new(cls, username: str, password: str, session_key: str = "",
                  useragent: str = DEFAULT_USERAGENT,
                  session: Optional[aiohttp.ClientSession] = None):
        """Creates a ``HamQthAsyncClient`` object and automatically starts a session if not provided.

        :param username: HamQTH username
        :param password: HamQTH password
        :param session_key: HamQTH login session key
        :param useragent: Useragent for HamQTH
        :param session: An aiohttp session to use for requests
        """
        obj = cls(username, password, session_key, useragent, session)
        if obj.session is None:
            await obj.start_session()
        return obj

    async def search(self, callsign: str) -> dataclasses.CallsignData:  # type: ignore[override]
        if not is_callsign(callsign):
            raise exceptions.CallsignLookupError("Invalid Callsign")
        try:
            await self._check_session(
                id=self._session_key,
                prg=self._useragent
            )
        except exceptions.CallsignLookupError:
            await self._login(
                u=self._username,
                p=self._password,
                prg=self._useragent
            )

        return self._process_search(
            query=callsign.upper(),
            resp=await self._do_query(
                id=self._session_key,
                callsign=callsign.upper(),
                prg=self._useragent
            )
        )

    async def _do_query(self, **query) -> bytes:  # type: ignore[override]
        if self._session is not None:
            async with self._session.get(self._base_url + urlencode(query)) as resp:
                if resp.status != 200:
                    raise exceptions.CallsignLookupError(f"Unable to connect to HamQTH (HTTP Error {resp.status})")
                return await resp.read()
        else:
            raise exceptions.CallsignLookupError(("Session not initialised. "
                                                  "Hint: Call `.start_session()` once or use the `new()` classmethod."))
