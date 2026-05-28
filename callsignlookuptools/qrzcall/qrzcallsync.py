"""
qrzcalltools: synchronous edition
---
Released under the terms of the BSD 3-Clause license.
"""


from typing import Optional

import requests

from ..common import mixins, dataclasses, exceptions
from ..common.constants import DEFAULT_USERAGENT
from ..common.functions import is_callsign
from .qrzcall import QrzcallClientAbc


class QrzcallSyncClient(mixins.SyncMixin, QrzcallClientAbc):
    """Synchronous QRZCALL.EU API client

    :param token: QRZCALL.EU Personal Access Token (``pat_…``). Generate one
        at https://qrzcall.eu/ → My Profile → Account → API Tokens. Requires
        a Data or Extra subscription on the account.
    :param useragent: Useragent for QRZCALL.EU
    :param session: A requests session to use for requests
    """
    def __init__(self, token: str, useragent: str = DEFAULT_USERAGENT,
                 session: Optional[requests.Session] = None):
        if session is None:
            self._session = requests.Session()
        else:
            self._session = session
        super().__init__(token, useragent=useragent)

    def search(self, callsign: str) -> dataclasses.CallsignData:
        if not is_callsign(callsign):
            raise exceptions.CallsignLookupError("Invalid Callsign")
        return self._process_search(
            query=callsign.upper(),
            resp=self._do_query(callsign=callsign.upper()),
        )

    def _do_query(self, **query) -> bytes:
        headers = {
            "Authorization": f"Bearer {self._token}",
            "User-Agent": self._useragent,
            "Accept": "application/json",
        }
        with self._session.get(self._base_url, params={"callsign": query["callsign"]},
                               headers=headers) as resp:
            if resp.status_code == 200:
                return resp.content
            if resp.status_code == 401:
                raise exceptions.CallsignLookupError(
                    "QRZCALL.EU token is invalid or has been revoked"
                )
            if resp.status_code == 403:
                raise exceptions.CallsignLookupError(
                    "QRZCALL.EU subscription required (Data or Extra tier)"
                )
            if resp.status_code == 404:
                raise exceptions.CallsignLookupError(f"{query['callsign']} not found")
            if resp.status_code == 429:
                raise exceptions.CallsignLookupError("QRZCALL.EU rate limit exceeded")
            raise exceptions.CallsignLookupError(
                f"Unable to connect to QRZCALL.EU (HTTP Error {resp.status_code})"
            )
