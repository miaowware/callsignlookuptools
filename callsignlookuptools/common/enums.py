"""
common enums for callsignlookuptools
---
Copyright 2021-2023 classabbyamp, 0x5c
Released under the terms of the BSD 3-Clause license.
"""


from enum import Enum


class DataSource(Enum):
    """Describes the callsign data lookup source"""
    CALLOOK = "callook.info"
    HAMQTH = "hamqth.com"
    QRZ = "qrz.com"
    QRZCQ = "qrzcq.com"


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


class CallsignType(Enum):
    """Describes what kind of license the license holder has"""
    CLUB = "CLUB"
    MILITARY = "MILITARY"
    RACES = "RACES"
    RECREATION = "RECREATION"
    PERSON = "PERSON"
    NONE = "NONE"


class LicenseClass(Enum):
    """Describes the class of a license"""
    NOVICE = "NOVICE"
    TECHNICIAN = "TECHNICIAN"
    TECHNICIAN_PLUS = "TECHNICIAN PLUS"
    GENERAL = "GENERAL"
    ADVANCED = "ADVANCED"
    EXTRA = "EXTRA"
    NONE = ""


class GeoLocSource(Enum):
    """Describes where the lat/long data in a :class:`QrzCallsignData` object comes from"""
    USER = "user"
    GEOCODE = "geocode"
    GRID = "grid"
    ZIP = "zip"
    STATE = "state"
    DXCC = "dxcc"
    NONE = "none"


class QslStatus(Enum):
    """Describes whether a type of QSL is accepted"""
    YES = True
    NO = False
    UNKNOWN = None

    def __str__(self) -> str:
        return self.name.title()


class CallookStatus(Enum):
    VALID = "VALID"
    INVALID = "INVALID"
    UPDATING = "UPDATING"
