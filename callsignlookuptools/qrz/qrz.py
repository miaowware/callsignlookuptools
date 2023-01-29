"""
qrztools
---
Copyright 2021-2023 classabbyamp, 0x5c
Released under the terms of the BSD 3-Clause license.
"""


from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime

from gridtools import Grid, LatLong
from pydantic import BaseModel, Field, validator

from ..common import abcs, enums, functions, dataclasses, exceptions
from ..common.constants import DEFAULT_USERAGENT


class QrzDataModel(BaseModel):
    call: Optional[str] = None
    xref: Optional[str] = None
    aliases: Optional[list[str]] = None
    trustee: Optional[str] = None
    dxcc: Optional[int] = None
    fname: Optional[str] = None
    name: Optional[str] = None
    nickname: Optional[str] = None
    name_fmt: Optional[str] = None
    attn: Optional[str] = None
    addr1: Optional[str] = None
    addr2: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    country: Optional[str] = None
    ccode: Optional[int] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    grid: Optional[Grid] = None
    county: Optional[str] = None
    fips: Optional[str] = None
    land: Optional[str] = None
    efdate: Optional[datetime] = None
    expdate: Optional[datetime] = None
    p_call: Optional[str] = None
    class_: Optional[str] = Field(default=None, alias="class")
    codes: Optional[str] = None
    qslmgr: Optional[str] = None
    email: Optional[str] = None
    url: Optional[str] = None
    u_views: Optional[int] = None
    bio: Optional[int] = None
    biodate: Optional[datetime] = None
    image: Optional[str] = None
    imageinfo: Optional[tuple[int, int, int]] = None
    serial: Optional[str] = None
    moddate: Optional[datetime] = None
    MSA: Optional[str] = None
    AreaCode: Optional[str] = None
    TimeZone: Optional[str] = None
    GMTOffset: Optional[str] = None
    DST: Optional[bool] = None
    eqsl: enums.QslStatus = enums.QslStatus.UNKNOWN
    mqsl: enums.QslStatus = enums.QslStatus.UNKNOWN
    cqzone: Optional[int] = None
    ituzone: Optional[int] = None
    born: Optional[int] = None
    user: Optional[str] = None
    lotw: enums.QslStatus = enums.QslStatus.UNKNOWN
    iota: Optional[str] = None
    geoloc: enums.GeoLocSource = enums.GeoLocSource.NONE

    @validator("aliases", pre=True)
    def _split_str(cls, v):
        if isinstance(v, str):
            return v.split(",")
        return v

    @validator("grid", pre=True)
    def _to_grid(cls, v):
        if isinstance(v, str):
            return Grid(v)
        return v

    @validator("efdate", "expdate", pre=True)
    def _parse_date(cls, v):
        if isinstance(v, str):
            try:
                return datetime.strptime(v, "%Y-%m-%d")
            except ValueError:
                return None
        return v

    @validator("eqsl", "mqsl", "lotw", pre=True)
    def _parse_qsl_status(cls, v):
        if v == "1":
            return True
        elif v == "0":
            return False
        else:
            return None

    @validator("DST", pre=True)
    def _parse_DST(cls, v):
        if v == "Y":
            return True
        elif v == "N":
            return False
        else:
            return None

    @validator("imageinfo", pre=True)
    def _parse_image_info(cls, v):
        return tuple(v.split(":"))

    class Config:
        anystr_strip_whitespace = True
        arbitrary_types_allowed = True


class QrzClientAbc(abcs.LookupAbc, ABC):
    """The base class for QrzSync and QrzAsync. **This should not be used directly.**"""
    _base_url = "https://xmldata.qrz.com/xml/current/?"

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

        if "Session" in data and "Error" in data["Session"]:
            raise exceptions.CallsignLookupError(data["Session"]["Error"])

        if "Callsign" not in data:
            raise exceptions.CallsignLookupError("No data found for query " + query)

        model_data = QrzDataModel.parse_obj(data["Callsign"])

        calldata = dataclasses.CallsignData(
            query=query,
            raw_data=model_data,
            data_source=enums.DataSource.QRZ
        )

        calldata.callsign = model_data.call
        if model_data.xref:
            calldata.query = model_data.xref
        calldata.aliases = model_data.aliases
        if model_data.trustee:
            calldata.trustee = dataclasses.Trustee(
                callsign=model_data.trustee
            )
        calldata.lic_class = model_data.class_
        calldata.lic_codes = model_data.codes
        calldata.effective_date = model_data.efdate
        calldata.expire_date = model_data.expdate
        calldata.prev_call = model_data.p_call
        calldata.modified_date = model_data.moddate
        calldata.name = dataclasses.Name(
            first=model_data.fname,
            name=model_data.name,
            nickname=model_data.nickname,
            formatted_name=model_data.name_fmt
        )
        calldata.address = dataclasses.Address(
            attn=model_data.attn,
            line1=model_data.addr1,
            city=model_data.addr2,
            state=model_data.state,
            zip=model_data.zip,
            country=model_data.country,
            country_code=model_data.ccode
        )
        calldata.dxcc = dataclasses.Dxcc(
            id=model_data.dxcc,
            name=model_data.land
        )
        if model_data.lat is not None and model_data.lon is not None:
            calldata.latlong = LatLong(lat=model_data.lat, long=model_data.lon)
        calldata.grid = model_data.grid
        calldata.county = model_data.county
        calldata.fips = model_data.fips
        calldata.msa = model_data.MSA
        calldata.area_code = model_data.AreaCode
        calldata.cq_zone = model_data.cqzone
        calldata.itu_zone = model_data.ituzone
        calldata.iota = model_data.iota
        calldata.geoloc_src = model_data.geoloc
        calldata.timezone = dataclasses.Timezone(
            utc_offset=model_data.GMTOffset,
            us_timezone=model_data.TimeZone,
            observes_dst=model_data.DST
        )
        calldata.qsl = dataclasses.Qsl(
            info=model_data.qslmgr,
            eqsl=model_data.eqsl,
            lotw=model_data.lotw,
            mail=model_data.mqsl
        )
        calldata.born = model_data.born
        calldata.email = model_data.email
        calldata.username = model_data.user
        calldata.url = model_data.url if model_data.url else f"https://www.qrz.com/db/{model_data.call}"
        calldata.page_views = model_data.u_views
        calldata.db_serial = model_data.serial
        calldata.bio = dataclasses.Bio(
            size=model_data.bio,
            updated=model_data.biodate
        )
        if model_data.imageinfo is not None and model_data.image:
            calldata.image = dataclasses.Image(
                url=model_data.image,
                size=model_data.imageinfo[2],
                height=model_data.imageinfo[0],
                width=model_data.imageinfo[1]
            )
        elif model_data.image:
            calldata.image = dataclasses.Image(url=model_data.image)

        return calldata
