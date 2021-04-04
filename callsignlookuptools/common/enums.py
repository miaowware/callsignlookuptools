"""
common enums for callsignlookuptools
---
Copyright 2021 classabbyamp, 0x5c
Released under the terms of the BSD 3-Clause license.
"""


from enum import Enum


class DataSource(Enum):
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
    CLUB = "Club"
    MILITARY = "Military"
    RACES = "RACES"
    RECREATION = "Military Recration"
    PERSON = "Individual"
    NONE = "None"


class LicenseClass(Enum):
    """Describes the class of a license"""
    NOVICE = "Novice"
    TECHNICIAN = "Technician"
    TECHNICIAN_PLUS = "Technician Plus"
    GENERAL = "General"
    ADVANCED = "Advanced"
    EXTRA = "Amateur Extra"
    NONE = "None"


class GeoLocSource(Enum):
    """Describes where the lat/long data in a :class:`QrzCallsignData` object comes from"""
    USER = "User"
    GEOCODE = "Geocode"
    GRID = "Grid"
    ZIP = "Zip Code"
    STATE = "State"
    DXCC = "DXCC"
    NONE = "None"
