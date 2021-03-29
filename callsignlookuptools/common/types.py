"""
common types for callsignlookuptools
---
Copyright 2021 classabbyamp, 0x5c
Released under the terms of the BSD 3-Clause license.
"""


from enum import Enum
from dataclasses import dataclass
from typing import Optional

from gridtools import LatLong, Grid


class CallsignLookupError(Exception):
    """The exception raised when something goes wrong in qrztools"""
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


@dataclass
class Dxcc:
    """Represents a DXCC entity"""
    #: entity ID
    id: int = 0
    #: entity name
    name: str = ""


@dataclass
class Address:
    """Represents a mailing address"""
    #: Attention address line, this line should be prepended to the address
    attn: Optional[str] = None
    #: address line 1 (i.e. house # and street)
    line1: Optional[str] = None
    #: address line 2 (i.e, city name)
    line2: Optional[str] = None
    #: state (USA Only)
    state: Optional[str] = None
    #: Zip/postal code
    zip: Optional[str] = None
    #: country name for the QSL mailing address
    country: Optional[str] = None
    #: dxcc entity code for the mailing address country
    ccode: Optional[int] = None
    #: county name (USA only)
    county: Optional[str] = None


@dataclass
class Name:
    """Represents a name"""
    #: first name(s)
    first: Optional[str] = None
    #: last name or full name
    name: Optional[str] = None
    #: A different or shortened name used on the air
    nickname: Optional[str] = None
    #: Combined full name and nickname in the format used by QRZ. This fortmat is subject to change.
    formatted_name: Optional[str] = None


class Continent(Enum):
    """Represents a continent"""
    AF = "Africa"
    AN = "Antarctica"
    AS = "Asia"
    EU = "Europe"
    NA = "North America"
    OC = "Oceania"
    SA = "South America"
    NONE = None


@dataclass
class CallsignData:
    """Represents a callsign lookup result"""
    #: callsign
    call: str
    #: address
    address: Address = Address()
    #: name
    name: Name = Name()
    #: approximate lat/long
    latlong: LatLong = LatLong(0, 0)
    #: approximate grid
    grid: Grid = Grid(LatLong(0, 0))
