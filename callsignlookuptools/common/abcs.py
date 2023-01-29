"""
ABCs for callsignlookuptools
---
Copyright 2021-2023 classabbyamp, 0x5c
Released under the terms of the BSD 3-Clause license.
"""


from abc import ABC, abstractmethod

from .dataclasses import CallsignData


class LookupAbc(ABC):
    """The base class for all lookup classes **This should not be used directly**."""
    @abstractmethod
    def __init__(self):
        pass

    @property  # type: ignore[misc]
    @abstractmethod
    def session(self):
        pass

    @session.setter  # type: ignore[misc]
    @abstractmethod
    def session(self, val):
        pass

    @abstractmethod
    def search(self, callsign: str) -> CallsignData:
        """Search for a callsign

        :param callsign: the callsign to look up
        :return: the callsign data from the lookup service
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

        :setter: sets username
        """
        return self._username

    @username.setter
    def username(self, val: str) -> None:
        self._username = val

    @property
    def password(self) -> str:
        """
        :getter: gets password

        :setter: sets password
        """
        return self._password

    @password.setter
    def password(self, val: str) -> None:
        self._password = val

    @property
    def useragent(self) -> str:
        """
        :getter: gets useragent

        :setter: sets useragent
        """
        return self._useragent

    @useragent.setter
    def useragent(self, val: str) -> None:
        self._useragent = val

    @property
    def session_key(self) -> str:
        """
        :getter: gets API session key

        :setter: sets API session key
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
