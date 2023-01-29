"""
common exceptions for callsignlookuptools
---
Copyright 2021-2023 classabbyamp, 0x5c
Released under the terms of the BSD 3-Clause license.
"""


class CallsignLookupError(Exception):
    """The exception raised when something goes wrong in callsignlookuptools"""
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
