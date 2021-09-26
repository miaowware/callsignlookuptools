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
    @abstractmethod
    def __init__(self):
        pass

    @property
    @abstractmethod
    def session(self):
        pass

    @session.setter  # type: ignore[attr-defined] # python/mypy#1465
    @abstractmethod
    def set_session(self, val):
        pass

    @abstractmethod
    def search(self, callsign: str) -> CallsignData:
        """Search for a callsign

        :param callsign: the callsign to look up
        :type callsign: str
        :return: the callsign data from the lookup service
        :rtype: :class:`CallsignData`
        :raises: :class:`common.exceptions.CallsignLookupError` on network or parsing error
        """
        pass

    @abstractmethod
    def _process_search(self, query: str, resp: bytes) -> CallsignData:
        pass

    @abstractmethod
    def _do_query(self, **query) -> bytes:
        pass


class AuthMixinAbc(ABC):
    """adds common properties for authenticated lookups"""
    @property
    def username(self) -> str:
        """
        :getter: gets username
        :rtype: str

        :setter: sets username
        :type: str
        """
        return self._username

    @username.setter  # type: ignore[attr-defined] # python/mypy#1465
    def set_username(self, val: str) -> None:
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

    @password.setter  # type: ignore[attr-defined] # python/mypy#1465
    def set_password(self, val: str) -> None:
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

    @useragent.setter  # type: ignore[attr-defined] # python/mypy#1465
    def set_useragent(self, val: str) -> None:
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

    @session_key.setter  # type: ignore[attr-defined] # python/mypy#1465
    def set_session_key(self, val: str) -> None:
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
