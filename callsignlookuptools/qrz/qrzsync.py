"""
qrztools: synchronous editon
---
Copyright 2021 classabbyamp, 0x5c
Released under the terms of the BSD 3-Clause license.
"""


from urllib.parse import urlencode

import requests

from ..__info__ import __version__
from ..common import mixins, dataclasses, exceptions
from .qrz import QrzClientAbc


class QrzSyncClient(mixins.SyncXmlAuthMixin, mixins.SyncMixin, QrzClientAbc):
    """A synchronous QRZ API client

    :param username: QRZ username
    :type username: str
    :param password: QRZ password
    :type password: str
    :param session_key: QRZ login session key
    :type session_key: str
    :param useragent: Useragent for QRZ
    :type useragent: str
    :param session: A requests session to use for requests
    :type session: requests.Session
    """
    def __init__(self, username: str, password: str, session_key: str = "",
                 useragent: str = f"python-callsignlookuptools-v{__version__}",
                 session: requests.Session = requests.Session()):
        self._session = session
        super().__init__(username, password, session_key=session_key, useragent=useragent)

    def search(self, callsign: str) -> dataclasses.CallsignData:
        if not callsign.isalnum():
            raise exceptions.CallsignLookupError("Invalid Callsign")
        try:
            self._check_session(
                s=self._session_key
            )
        except exceptions.CallsignLookupError:
            self._login(
                username=self._username,
                password=self._password,
                agent=self._useragent
            )

        return self._process_search(
            query=callsign.upper(),
            resp=self._do_query(
                s=self._session_key,
                callsign=callsign.upper()
            )
        )

    def _do_query(self, **query) -> bytes:
        with self._session.get(self._base_url + urlencode(query)) as resp:
            if resp.status_code != 200:
                raise exceptions.CallsignLookupError(f"Unable to connect to QRZ (HTTP Error {resp.status_code})")
            return resp.content
