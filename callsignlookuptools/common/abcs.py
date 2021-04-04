"""
ABCs for callsignlookuptools
---
Copyright 2021 classabbyamp, 0x5c
Released under the terms of the BSD 3-Clause license.
"""


from abc import ABC, abstractmethod

from .dataclasses import CallsignData


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
        :getter: gets API session key
        :rtype: str

        :setter: sets API session key
        :type: str
        """
        return self._session_key

    @session_key.setter
    def session_key(self, val: str) -> None:
        self._session_key = val

    @abstractmethod
    def _login(self, **query):
        pass

    @abstractmethod
    def _process_login(self, resp: bytes):
        pass

    @abstractmethod
    def _check_session(self, **query):
        pass

    @abstractmethod
    def _process_check_session(self, resp: bytes):
        pass
