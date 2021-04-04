"""
common dataclasses for callsignlookuptools
---
Copyright 2021 classabbyamp, 0x5c
Released under the terms of the BSD 3-Clause license.
"""


from dataclasses import dataclass
from typing import Union, Optional
from datetime import datetime

from pydantic import BaseModel
from gridtools import LatLong, Grid

from .enums import DataSource, Continent, CallsignType, LicenseClass, GeoLocSource


@dataclass
class Dxcc:
    """Represents a DXCC entity"""
    #: entity ID
    id: Optional[int] = None
    #: entity name
    name: Optional[str] = None


@dataclass
class Address:
    """Represents a mailing address"""
    #: Attention address line, this line should be prepended to the address
    attn: Optional[str] = None
    #: address line 1 (i.e. house # and street)
    line1: Optional[str] = None
    #: address line 2 (i.e, city name)
    line2: Optional[str] = None
    line3: Optional[str] = None
    city: Optional[str] = None
    #: state (USA Only)
    state: Optional[str] = None
    #: Zip/postal code
    zip: Optional[str] = None
    #: country name for the QSL mailing address
    country: Optional[str] = None
    #: dxcc entity code for the mailing address country
    country_code: Optional[int] = None


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


@dataclass
class Trustee:
    callsign: Optional[str] = None
    name: Optional[str] = None


@dataclass
class Qsl:
    info: Optional[str] = None
    bureau_info: Optional[str] = None
    eqsl: Optional[bool] = None
    lotw: Optional[bool] = None
    mail: Optional[bool] = None
    bureau: Optional[bool] = None


@dataclass
class Bio:
    size: Optional[int] = None
    updated: Optional[datetime] = None


@dataclass
class Image:
    url: Optional[str] = None
    size: Optional[int] = None
    height: Optional[int] = None
    width: Optional[int] = None


@dataclass
class SocialMedia:
    website: Optional[str] = None
    jabber: Optional[str] = None
    icq: Optional[str] = None
    msn: Optional[str] = None
    skype: Optional[str] = None
    facebook: Optional[str] = None
    twitter: Optional[str] = None
    google_plus: Optional[str] = None
    youtube: Optional[str] = None
    linkedin: Optional[str] = None
    flickr: Optional[str] = None
    vimeo: Optional[str] = None


@dataclass
class Timezone:
    utc_offset: Optional[str] = None
    us_timezone: Optional[str] = None
    observes_dst: Optional[bool] = None


@dataclass
class CallsignData:
    query: str
    raw_data: BaseModel
    data_source: DataSource
    type: Optional[CallsignType] = None
    callsign: Optional[str] = None
    aliases: Optional[list[str]] = None
    trustee: Optional[Trustee] = None
    lic_class: Optional[Union[str, LicenseClass]] = None
    lic_codes: Optional[str] = None
    effective_date: Optional[datetime] = None
    expire_date: Optional[datetime] = None
    last_action_date: Optional[datetime] = None
    prev_call: Optional[str] = None
    prev_lic_class: Optional[LicenseClass] = None
    modified_date: Optional[datetime] = None
    name: Optional[Name] = None
    address: Optional[Address] = None
    dxcc: Optional[Dxcc] = None
    dxcc_prefix: Optional[str] = None
    qth: Optional[str] = None
    continent: Optional[Continent] = None
    latlong: Optional[LatLong] = None
    grid: Optional[Grid] = None
    county: Optional[str] = None
    district: Optional[str] = None
    oblast: Optional[str] = None
    dok: Optional[str] = None
    sondok: Optional[bool] = None
    plot: Optional[str] = None
    fips: Optional[str] = None
    msa: Optional[str] = None
    area_code: Optional[str] = None
    cq_zone: Optional[int] = None
    itu_zone: Optional[int] = None
    iota: Optional[str] = None
    geoloc_src: Optional[GeoLocSource] = None
    timezone: Optional[Timezone] = None
    qsl: Optional[Qsl] = None
    born: Optional[int] = None
    licensed: Optional[int] = None
    email: Optional[str] = None
    username: Optional[str] = None
    url: Optional[str] = None
    page_views: Optional[int] = None
    db_serial: Optional[int] = None
    bio: Optional[Bio] = None
    image: Optional[Image] = None
    social_media: Optional[SocialMedia] = None
    uls_url: Optional[str] = None
    frn: Optional[str] = None
