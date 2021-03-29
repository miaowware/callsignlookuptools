"""
ABCs for callsignlookuptools
---
Copyright 2021 classabbyamp, 0x5c
Released under the terms of the BSD 3-Clause license.
"""


from importlib.util import find_spec
from abc import ABC, abstractmethod

if find_spec("requests"):
    import requests
if find_spec("aiohttp"):
    import aiohttp

from .types import CallsignData, CallsignLookupError
from .functions import xml2dict


class LookupAbc(ABC):
    """The base class for all lookup classes **This should not be used directly**."""
    _base_url: str

    @abstractmethod
    def __init__(self):
        pass

    @property  # type: ignore
    @abstractmethod
    def session(self):
        pass

    @session.setter  # type: ignore
    @abstractmethod
    def session(self, val):
        pass

    @abstractmethod
    def search(self, callsign):
        pass

    @abstractmethod
    def _process_search(self, resp: bytes) -> CallsignData:
        pass

    @abstractmethod
    def _do_query(self, **query) -> bytes:
        pass


class AuthMixinAbc(ABC):
    """adds common properties for authenticated lookups"""
    _username: str
    _password: str
    _useragent: str
    _session_key: str

    @property
    def username(self) -> str:
        """
        :getter: gets username
        :rtype: str

        :setter: sets username
        :type: str
        """
        return self._username

    @username.setter
    def username(self, val: str) -> None:
        self._username = val

    @property
    def password(self) -> str:
        """
        :getter: gets password
        :rtype: str

        :setter: sets password
        :type: str
        """
        return self._password

    @password.setter
    def password(self, val: str) -> None:
        self._password = val

    @property
    def useragent(self) -> str:
        """
        :getter: gets useragent
        :rtype: str

        :setter: sets useragent
        :type: str
        """
        return self._useragent

    @useragent.setter
    def useragent(self, val: str) -> None:
        self._useragent = val

    @property
    def session_key(self) -> str:
        """
        :getter: gets QRZ session key
        :rtype: str

        :setter: sets QRZ session key
        :type: str
        """
        return self._session_key

    @session_key.setter
    def session_key(self, val: str) -> None:
        self._session_key = val

    @abstractmethod
    def _login(self, **query):
        pass

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

    @abstractmethod
    def _check_session(self, **query):
        pass

    def _process_check_session(self, resp: bytes):
        data = xml2dict(resp).get("session", None)
        if not data:
            raise CallsignLookupError("Invalid Session")
        if "error" in data:
            raise CallsignLookupError(data["error"])


class SyncAuthMixin(AuthMixinAbc):
    def _login(self, **query):
        self._process_login(self._do_query(**query))

    def _check_session(self, **query):
        self._process_check_session(self._do_query(**query))


class AsyncAuthMixin(AuthMixinAbc):
    async def _login(self, **query):
        self._process_login(await self._do_query(**query))

    async def _check_session(self, **query):
        self._process_check_session(await self._do_query(**query))


if find_spec("requests"):
    class SyncMixin:
        @property
        def session(self) -> requests.Session:
            """
            :getter: gets the requests session
            :rtype: requests.Session

            :setter: sets the requests session
            :type: requests.Session
            """
            return self._session

        @session.setter
        def session(self, val: requests.Session):
            self._session = val


if find_spec("aiohttp"):
    class AsyncMixin:
        @property
        def session(self) -> aiohttp.ClientSession:
            """
            :getter: gets the aiohttp session
            :rtype: requests.Session

            :setter: sets the aiohttp session
            :type: requests.Session
            """
            return self._session

        @session.setter
        def session(self, val: aiohttp.ClientSession):
            self._session = val

        async def start_session(self):
            """Creates a new ``aiohttp.ClientSession``"""
            self._session = aiohttp.ClientSession()

        async def close_session(self):
            """Closes the ``aiohttp.ClientSession`` session"""
            await self._session.close()
