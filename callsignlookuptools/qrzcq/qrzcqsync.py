"""
qrzcqtools: synchronous editon
---
Copyright 2021-2023 classabbyamp, 0x5c
Released under the terms of the BSD 3-Clause license.
"""


from urllib.parse import urlencode
from typing import Optional

import requests

from ..common import mixins, dataclasses, exceptions
from ..common.constants import DEFAULT_USERAGENT
from ..common.functions import is_callsign
from .qrzcq import QrzCqClientAbc


class QrzCqSyncClient(mixins.SyncXmlAuthMixin, mixins.SyncMixin, QrzCqClientAbc):
    """Synchronous QRZCQ API client

    :param username: QRZCQ username
    :param password: QRZCQ password
    :param session_key: QRZCQ login session key
    :param useragent: Useragent for QRZCQ
    :param session: A requests session to use for requests
    """
    def __init__(self, username: str, password: str, session_key: str = "",
                 useragent: str = DEFAULT_USERAGENT,
                 session: Optional[requests.Session] = None):
        if session is None:
            self._session = requests.Session()
        else:
            self._session = session
        super().__init__(username, password, session_key=session_key, useragent=useragent)

    def search(self, callsign: str) -> dataclasses.CallsignData:
        if not is_callsign(callsign):
            raise exceptions.CallsignLookupError("Invalid Callsign")
        try:
            self._check_session(
                s=self._session_key,
                agent=self._useragent
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
                callsign=callsign.upper(),
                agent=self._useragent
            )
        )

    def _do_query(self, **query) -> bytes:
        with self._session.get(self._base_url + urlencode(query)) as resp:
            if resp.status_code != 200:
                raise exceptions.CallsignLookupError(f"Unable to connect to QRZCQ (HTTP Error {resp.status_code})")
            return resp.content
