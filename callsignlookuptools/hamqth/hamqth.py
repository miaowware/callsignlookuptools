"""
hamqthtools
---
Copyright 2021-2023 classabbyamp, 0x5c
Released under the terms of the BSD 3-Clause license.
"""


from abc import ABC, abstractmethod
from typing import Optional

from gridtools import Grid, LatLong
from pydantic import BaseModel, validator

from ..common import abcs, enums, functions, dataclasses, exceptions
from ..common.constants import DEFAULT_USERAGENT


class HamQthDataModel(BaseModel):
    callsign: Optional[str] = None
    nick: Optional[str] = None
    qth: Optional[str] = None
    country: Optional[str] = None
    adif: Optional[int] = None
    itu: Optional[int] = None
    cq: Optional[int] = None
    grid: Optional[Grid] = None
    adr_name: Optional[str] = None
    adr_street1: Optional[str] = None
    adr_street2: Optional[str] = None
    adr_street3: Optional[str] = None
    adr_city: Optional[str] = None
    adr_zip: Optional[str] = None
    adr_country: Optional[str] = None
    adr_adif: Optional[int] = None
    district: Optional[str] = None
    us_state: Optional[str] = None
    us_county: Optional[str] = None
    oblast: Optional[str] = None
    dok: Optional[str] = None
    iota: Optional[str] = None
    qsl_via: Optional[str] = None
    lotw: enums.QslStatus = enums.QslStatus.UNKNOWN
    eqsl: enums.QslStatus = enums.QslStatus.UNKNOWN
    qsl: enums.QslStatus = enums.QslStatus.UNKNOWN
    qsldirect: enums.QslStatus = enums.QslStatus.UNKNOWN
    email: Optional[str] = None
    jabber: Optional[str] = None
    icq: Optional[str] = None
    msn: Optional[str] = None
    skype: Optional[str] = None
    birth_year: Optional[int] = None
    lic_year: Optional[int] = None
    picture: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    continent: enums.Continent = enums.Continent.NONE
    utc_offset: Optional[str] = None
    web: Optional[str] = None
    facebook: Optional[str] = None
    twitter: Optional[str] = None
    gplus: Optional[str] = None
    youtube: Optional[str] = None
    linkedin: Optional[str] = None
    flicker: Optional[str] = None
    vimeo: Optional[str] = None

    @validator("grid", pre=True)
    def _to_grid(cls, v):
        if isinstance(v, str):
            return Grid(v)
        return v

    @validator("lotw", "eqsl", "qsl", "qsldirect", pre=True)
    def _parse_qsl_status(cls, v):
        if v == "Y":
            return True
        elif v == "N":
            return False
        else:
            return None

    @validator("continent", pre=True)
    def _continent(cls, v):
        if v:
            for c in enums.Continent:
                if c.name == v.upper():
                    return c
        return enums.Continent.NONE

    class Config:
        anystr_strip_whitespace = True
        arbitrary_types_allowed = True


class HamQthClientAbc(abcs.LookupAbc, ABC):
    """The base class for HamQthSync and HamQthAsync. **This should not be used directly.**"""
    _base_url = "https://www.hamqth.com/xml.php?"

    def __init__(self, username: str, password: str, session_key: str = "",
                 useragent: str = DEFAULT_USERAGENT):
        self._username = username
        self._password = password
        self._useragent = useragent
        self._session_key = session_key

    @abstractmethod
    def search(self, callsign: str) -> dataclasses.CallsignData:
        pass

    @abstractmethod
    def _do_query(self, **query) -> bytes:
        pass

    def _process_search(self, query: str, resp: bytes) -> dataclasses.CallsignData:
        data = functions.xml2dict(resp, to_lower=False)

        if "session" in data and "error" in data["session"]:
            raise exceptions.CallsignLookupError(data["session"]["error"])

        if "search" not in data:
            raise exceptions.CallsignLookupError("No data found for query " + query)

        model_data = HamQthDataModel.parse_obj(data["search"])

        calldata = dataclasses.CallsignData(
            query=query,
            raw_data=model_data,
            data_source=enums.DataSource.HAMQTH
        )

        calldata.callsign = model_data.callsign
        calldata.name = dataclasses.Name(
            nickname=model_data.nick,
            name=model_data.adr_name,
        )
        calldata.qth = model_data.qth
        calldata.dxcc = dataclasses.Dxcc(
            id=model_data.adif,
            name=model_data.country,
        )
        calldata.itu_zone = model_data.itu
        calldata.cq_zone = model_data.cq
        calldata.grid = model_data.grid
        calldata.address = dataclasses.Address(
            line1=model_data.adr_street1,
            line2=model_data.adr_street2,
            line3=model_data.adr_street3,
            city=model_data.adr_city,
            zip=model_data.adr_zip,
            country=model_data.adr_country,
            country_code=model_data.adr_adif,
            state=model_data.us_state,
        )
        calldata.county = model_data.us_county
        calldata.oblast = model_data.oblast
        calldata.dok = model_data.dok
        calldata.iota = model_data.iota
        calldata.qsl = dataclasses.Qsl(
            info=model_data.qsl_via,
            lotw=model_data.lotw,
            eqsl=model_data.eqsl,
            mail=model_data.qsldirect,
            bureau=model_data.qsl,
        )
        calldata.email = model_data.email
        calldata.social_media = dataclasses.SocialMedia(
            website=model_data.web,
            jabber=model_data.jabber,
            icq=model_data.icq,
            msn=model_data.msn,
            skype=model_data.skype,
            facebook=model_data.facebook,
            twitter=model_data.twitter,
            google_plus=model_data.gplus,
            youtube=model_data.youtube,
            linkedin=model_data.linkedin,
            flickr=model_data.flicker,
            vimeo=model_data.vimeo,
        )
        calldata.born = model_data.birth_year
        calldata.licensed = model_data.lic_year
        calldata.image = dataclasses.Image(url=model_data.picture)
        if model_data.latitude is not None and model_data.longitude is not None:
            calldata.latlong = LatLong(lat=model_data.latitude, long=model_data.longitude)
        calldata.continent = model_data.continent
        calldata.timezone = dataclasses.Timezone(utc_offset=model_data.utc_offset)
        calldata.url = f"https://www.hamqth.com/{model_data.callsign}"

        return calldata
