"""
common dataclasses for callsignlookuptools
---
Copyright 2021-2023 classabbyamp, 0x5c
Released under the terms of the BSD 3-Clause license.
"""


from dataclasses import dataclass
from typing import Union, Optional
from datetime import datetime

from pydantic import BaseModel
from gridtools import LatLong, Grid

from .enums import DataSource, Continent, CallsignType, LicenseClass, GeoLocSource, QslStatus


@dataclass
class Dxcc:
    """Represents a DXCC entity"""
    #: entity ID
    id: Optional[int] = None
    #: entity name
    name: Optional[str] = None

    def __str__(self) -> str:
        if self.name and self.id:
            return self.name + f" ({self.id})"
        elif self.name:
            return self.name
        elif self.id:
            return str(self.id)
        return ""


@dataclass
class Address:
    """Represents a mailing address"""
    #: Attention address line, this line should be prepended to the address
    attn: Optional[str] = None
    #: address line 1
    line1: Optional[str] = None
    #: address line 2
    line2: Optional[str] = None
    #: address line 3
    line3: Optional[str] = None
    #: city
    city: Optional[str] = None
    #: state (USA Only)
    state: Optional[str] = None
    #: Zip/postal code
    zip: Optional[str] = None
    #: country name for the QSL mailing address
    country: Optional[str] = None
    #: dxcc entity code for the mailing address country
    country_code: Optional[int] = None

    def __str__(self) -> str:
        # attn
        # line1
        # line2
        # line3
        # city, state zip (= locale)
        # country
        locale = self.city if self.city else ""
        locale += (", " if self.city and (self.state or self.zip) else "") + (self.state if self.state else "")
        locale += (" " if self.state else "") + (self.zip if self.zip else "")
        locale = locale.strip()

        addr = [self.attn, self.line1, self.line2, self.line3, locale, self.country]
        return "\n".join([ln for ln in addr if ln])


@dataclass
class Name:
    """Represents a name"""
    #: first name(s)
    first: Optional[str] = None
    #: last name or full name
    name: Optional[str] = None
    #: A different or shortened name used on the air
    nickname: Optional[str] = None
    #: Combined full name and nickname in the format used by QRZ. This format is subject to change.
    formatted_name: Optional[str] = None

    def __str__(self) -> str:
        if self.formatted_name:
            return self.formatted_name
        # only first
        if self.first and not self.name and not self.nickname:
            return self.first
        # only name
        elif not self.first and self.name and not self.nickname:
            return self.name
        # only nickname
        elif not self.first and not self.name and self.nickname:
            return self.nickname
        # first + name
        elif self.first and self.name and not self.nickname:
            return self.first + " " + self.name
        # first + nickname
        elif self.first and not self.name and self.nickname:
            return self.first + ' "' + self.nickname + '"'
        # name + nickname
        elif not self.first and self.name and self.nickname:
            return '"' + self.nickname + '" ' + self.name
        # all
        elif self.first and self.name and self.nickname:
            return self.first + ' "' + self.nickname + '" ' + self.name
        return ""


@dataclass
class Trustee:
    """Represents a club callsign trustee (USA only)"""
    #: trustee callsign
    callsign: Optional[str] = None
    #: trustee name
    name: Optional[str] = None

    def __str__(self) -> str:
        if self.callsign and self.name:
            return self.name + " (" + self.callsign + ")"
        elif self.callsign:
            return self.callsign
        elif self.name:
            return self.name
        return ""


@dataclass
class Qsl:
    """Represents information about QSL methods"""
    #: info about QSLing, e.g. QSL manager info
    info: Optional[str] = None
    #: info about QSLing via bureau
    bureau_info: Optional[str] = None
    #: whether eQSL is accepted
    eqsl: QslStatus = QslStatus.UNKNOWN
    #: whether Logbook of the World QSL is accepted
    lotw: QslStatus = QslStatus.UNKNOWN
    #: whether direct mail QSL is accepted
    mail: QslStatus = QslStatus.UNKNOWN
    #: whether bureau QSL is accepted
    bureau: QslStatus = QslStatus.UNKNOWN

    def __str__(self) -> str:
        out = []
        if self.info:
            out.append(self.info)
        if self.bureau_info:
            out.append(self.bureau_info)
        out += [
            "Mail: " + self.mail.name.title(),
            "Bureau: " + self.bureau.name.title(),
            "LotW: " + self.lotw.name.title(),
            "eQSL: " + self.eqsl.name.title(),
        ]
        return "\n".join(out)


@dataclass
class Bio:
    """Represents metadata for a QRZ bio"""
    #: approximate size in bytes
    size: Optional[int] = None
    #: when the bio was last updated
    updated: Optional[datetime] = None


@dataclass
class Image:
    """Represents an image"""
    #: image url
    url: Optional[str] = None
    #: image size in bytes
    size: Optional[int] = None
    #: image height in pixels
    height: Optional[int] = None
    #: image width in pixels
    width: Optional[int] = None


@dataclass
class SocialMedia:
    """represents social media info"""
    #: website url
    website: Optional[str] = None
    #: Jabber username
    jabber: Optional[str] = None
    #: ICQ number
    icq: Optional[str] = None
    #: MSN username
    msn: Optional[str] = None
    #: Skype username
    skype: Optional[str] = None
    #: Facebook profile url
    facebook: Optional[str] = None
    #: Twitter profile url
    twitter: Optional[str] = None
    #: Google+ profile url
    google_plus: Optional[str] = None
    #: YouTube channel url
    youtube: Optional[str] = None
    #: LinkedIn profile url
    linkedin: Optional[str] = None
    #: Flickr profile url
    flickr: Optional[str] = None
    #: Vimeo profile url
    vimeo: Optional[str] = None


@dataclass
class Timezone:
    utc_offset: Optional[str] = None
    us_timezone: Optional[str] = None
    observes_dst: Optional[bool] = None


@dataclass
class CallsignData:
    """Represents the data for a callsign retrieved from a lookup service"""
    #: the callsign searched for
    query: str
    #: the raw data, as parsed by pydantic from the API response. Probably not needed for most use cases.
    raw_data: BaseModel
    #: the lookup service the data comes from
    data_source: DataSource
    #: the type of license the callsign is associated with
    type: Optional[CallsignType] = None
    #: the callsign, as received from the lookup service. Not always the same as the query.
    callsign: Optional[str] = None
    #: alias callsigns
    aliases: Optional[list[str]] = None
    #: trustee info
    trustee: Optional[Trustee] = None
    #: license class. Some lookup services have a defined set of classes.
    lic_class: Optional[Union[str, LicenseClass]] = None
    #: license codes
    lic_codes: Optional[str] = None
    #: license effective/grant date
    effective_date: Optional[datetime] = None
    #: license expiration date
    expire_date: Optional[datetime] = None
    #: license last updated date
    last_action_date: Optional[datetime] = None
    #: previous callsign
    prev_call: Optional[str] = None
    #: previous license class
    prev_lic_class: Optional[LicenseClass] = None
    #: lookup service record modification date
    modified_date: Optional[datetime] = None
    #: licensee name
    name: Optional[Name] = None
    #: licensee address
    address: Optional[Address] = None
    #: licensee DXCC entity
    dxcc: Optional[Dxcc] = None
    #: licensee DXCC's primary callsign prefix
    dxcc_prefix: Optional[str] = None
    #: licensee location
    qth: Optional[str] = None
    #: licensee continent
    continent: Optional[Continent] = None
    #: latitude and longitude of address or QTH
    latlong: Optional[LatLong] = None
    #: grid square locator of address or QTH
    grid: Optional[Grid] = None
    #: county of address or QTH
    county: Optional[str] = None
    #: district of address or QTH
    district: Optional[str] = None
    #: oblast of address or QTH (Russia only)
    oblast: Optional[str] = None
    #: DOK name (Germany only)
    dok: Optional[str] = None
    #: whether the DOK is a Sonder-DOK (Germany only)
    sondok: Optional[bool] = None
    #: Polish OT number (Poland only)
    plot: Optional[str] = None
    #: Federal Information Processing Standards number (USA only)
    fips: Optional[str] = None
    #: Metro Service Area (USA only)
    msa: Optional[str] = None
    #: telephone area code (USA only)
    area_code: Optional[str] = None
    #: CQ zone
    cq_zone: Optional[int] = None
    #: ITU zone
    itu_zone: Optional[int] = None
    #: Islands on the Air designator
    iota: Optional[str] = None
    #: geolocation information source
    geoloc_src: Optional[GeoLocSource] = None
    #: licensee time zone
    timezone: Optional[Timezone] = None
    #: QSL info
    qsl: Optional[Qsl] = None
    #: year born
    born: Optional[int] = None
    #: year licensed
    licensed: Optional[int] = None
    #: licensee email address
    email: Optional[str] = None
    #: username of license page manager
    username: Optional[str] = None
    #: url of the webpage for the callsign
    url: Optional[str] = None
    #: callsign page views
    page_views: Optional[int] = None
    #: QRZ database serial number
    db_serial: Optional[str] = None
    #: biography info
    bio: Optional[Bio] = None
    #: profile image info
    image: Optional[Image] = None
    #: social media info
    social_media: Optional[SocialMedia] = None
    #: ULS record url (USA only)
    uls_url: Optional[str] = None
    #: FRN (USA only)
    frn: Optional[str] = None
