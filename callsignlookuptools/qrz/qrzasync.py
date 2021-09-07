"""
qrztools: asynchronous editon
---
Copyright 2021 classabbyamp, 0x5c
Released under the terms of the BSD 3-Clause license.
"""


from typing import Optional
from urllib.parse import urlencode

import aiohttp

from ..__info__ import __version__
from ..common import mixins, dataclasses, exceptions
from .qrz import QrzClientAbc


class QrzAsyncClient(mixins.AsyncXmlAuthMixin, mixins.AsyncMixin, QrzClientAbc):
    """Asynchronous QRZ API client

    :param username: QRZ username
    :type username: str
    :param password: QRZ password
    :type password: str
    :param session_key: QRZ login session key
    :type session_key: str
    :param useragent: Useragent for QRZ
    :type useragent: str
    :param session: An aiohttp session to use for requests
    :type session: Optional[aiohttp.ClientSession]
    """
    def __init__(self, username: str, password: str, session_key: str = "",
                 useragent: str = f"python-callsignlookuptools-v{__version__}",
                 session: Optional[aiohttp.ClientSession] = None):
        self._session = session
        super().__init__(username, password, session_key=session_key, useragent=useragent)

    @classmethod
    async def new(cls, username: str, password: str, session_key: str = "",
                  useragent: str = f"python-callsignlookuptools-v{__version__}",
                  session: Optional[aiohttp.ClientSession] = None) -> 'QrzAsyncClient':
        """Creates a ``QrzAsyncClient`` object and automatically starts a session if not provided.

        :param username: QRZ username
        :param password: QRZ password
        :param session_key: QRZ login session key
        :param useragent: Useragent for QRZ
        :param session: An aiohttp session to use for requests
        """
        obj = cls(username, password, session_key, useragent, session)
        if obj.session is None:
            await obj.start_session()
        return obj

    async def search(self, callsign: str) -> dataclasses.CallsignData:  # type: ignore
        if not callsign.isalnum():
            raise exceptions.CallsignLookupError("Invalid Callsign")
        try:
            await self._check_session(
                s=self._session_key
            )
        except exceptions.CallsignLookupError:
            await self._login(
                username=self._username,
                password=self._password,
                agent=self._useragent
            )

        return self._process_search(
            query=callsign.upper(),
            resp=await self._do_query(
                s=self._session_key,
                callsign=callsign.upper()
            )
        )

    async def _do_query(self, **query) -> bytes:  # type: ignore
        if self._session is not None:
            async with self._session.get(self._base_url + urlencode(query)) as resp:
                if resp.status != 200:
                    raise exceptions.CallsignLookupError(f"Unable to connect to QRZ (HTTP Error {resp.status})")
                return await resp.read()
        else:
            raise exceptions.CallsignLookupError(("Session not initialised. "
                                                  "Hint: Call `.start_session()` or use the `new()` classmethod."))
