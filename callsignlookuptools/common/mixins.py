"""
Mixins for callsignlookuptools
---
Copyright 2021-2023 classabbyamp, 0x5c
Released under the terms of the BSD 3-Clause license.
"""


from importlib.util import find_spec
from typing import Optional

if find_spec("requests"):
    import requests
if find_spec("aiohttp"):
    import aiohttp

from .abcs import AuthMixinAbc
from .exceptions import CallsignLookupError
from .functions import xml2dict


if find_spec("requests"):
    class SyncXmlAuthMixin(AuthMixinAbc):
        def _login(self, **query):
            self._process_login(self._do_query(**query))

        def _check_session(self, **query):
            self._process_check_session(self._do_query(**query))

        def _process_login(self, resp: bytes):
            data = xml2dict(resp).get("session", None)
            if not data:
                raise CallsignLookupError("Login Failed")
            if "error" in data:
                raise CallsignLookupError(f"Login Failed: {data['error']}")
            if "key" in data:
                self._session_key = data["key"]
            elif "session_id" in data:
                self._session_key = data["session_id"]

        def _process_check_session(self, resp: bytes):
            data = xml2dict(resp).get("session", None)
            if not data:
                raise CallsignLookupError("Invalid Session")
            if "error" in data:
                raise CallsignLookupError(data["error"])

    class SyncMixin:
        @property
        def session(self) -> requests.Session:
            """
            :getter: gets the requests session

            :setter: sets the requests session
            """
            return self._session

        @session.setter
        def session(self, val: requests.Session):
            self._session = val


if find_spec("aiohttp"):
    class AsyncXmlAuthMixin(AuthMixinAbc):
        async def _login(self, **query):
            self._process_login(await self._do_query(**query))

        async def _check_session(self, **query):
            self._process_check_session(await self._do_query(**query))

        def _process_login(self, resp: bytes):
            data = xml2dict(resp).get("session", None)
            if not data:
                raise CallsignLookupError("Login Failed")
            if "error" in data:
                raise CallsignLookupError(f"Login Failed: {data['error']}")
            if "key" in data:
                self._session_key = data["key"]
            elif "session_id" in data:
                self._session_key = data["session_id"]

        def _process_check_session(self, resp: bytes):
            data = xml2dict(resp).get("session", None)
            if not data:
                raise CallsignLookupError("Invalid Session")
            if "error" in data:
                raise CallsignLookupError(data["error"])

    class AsyncMixin:
        @property
        def session(self) -> Optional[aiohttp.ClientSession]:
            """
            :getter: gets the aiohttp session

            :setter: sets the aiohttp session
            """
            return self._session

        @session.setter
        def session(self, val: Optional[aiohttp.ClientSession]):
            self._session = val

        async def start_session(self):
            """Creates a new ``aiohttp.ClientSession``"""
            self._session = aiohttp.ClientSession()

        async def close_session(self):
            """Closes the ``aiohttp.ClientSession`` session"""
            await self._session.close()
