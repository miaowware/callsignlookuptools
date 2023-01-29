"""
qrzcqtools
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


class QrzCqDataModel(BaseModel):
    call: Optional[str] = None
    name: Optional[str] = None
    qth: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    zip: Optional[str] = None
    license: Optional[str] = None
    continent: enums.Continent = enums.Continent.NONE
    country: Optional[str] = None
    state: Optional[str] = None
    county: Optional[str] = None
    bmanager: Optional[str] = None
    manager: Optional[str] = None
    locator: Optional[Grid] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    website: Optional[str] = None
    dxcc: Optional[int] = None
    itu: Optional[int] = None
    cq: Optional[int] = None
    iota: Optional[str] = None
    plot: Optional[str] = None
    dok: Optional[str] = None
    sondok: Optional[bool] = None
    eqsl: enums.QslStatus = enums.QslStatus.UNKNOWN
    lotw: enums.QslStatus = enums.QslStatus.UNKNOWN
    bqsl: enums.QslStatus = enums.QslStatus.UNKNOWN
    mqsl: enums.QslStatus = enums.QslStatus.UNKNOWN
    utf8: Optional[bool] = None
    qslpic: Optional[str] = None
    prefix: Optional[str] = None

    @validator("locator", pre=True)
    def _to_grid(cls, v):
        if isinstance(v, str):
            return Grid(v)
        return v

    @validator("lotw", "eqsl", "bqsl", "mqsl", "utf8", "sondok", pre=True)
    def _parse_qsl_status(cls, v):
        if v == "1":
            return True
        elif v == "0":
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


class QrzCqClientAbc(abcs.LookupAbc, ABC):
    """The base class for QrzCqSync and QrzCqAsync. **This should not be used directly.**"""
    _base_url = "https://ssl.qrzcq.com/xml?"

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

        model_data = QrzCqDataModel.parse_obj(data["Callsign"])

        calldata = dataclasses.CallsignData(
            query=query,
            raw_data=model_data,
            data_source=enums.DataSource.QRZCQ
        )

        calldata.callsign = model_data.call
        calldata.name = dataclasses.Name(name=model_data.name)
        calldata.qth = model_data.qth
        calldata.address = dataclasses.Address(
            line1=model_data.address,
            city=model_data.city,
            zip=model_data.zip,
            state=model_data.state,
            country=model_data.country,
            country_code=model_data.dxcc,
        )
        calldata.lic_class = model_data.license
        calldata.continent = model_data.continent
        calldata.dxcc = dataclasses.Dxcc(
            id=model_data.dxcc,
            name=model_data.country,
        )
        calldata.county = model_data.county
        calldata.qsl = dataclasses.Qsl(
            info=model_data.manager,
            bureau_info=model_data.bmanager,
            eqsl=model_data.eqsl,
            lotw=model_data.lotw,
            bureau=model_data.bqsl,
            mail=model_data.mqsl,
        )
        calldata.grid = model_data.locator
        if model_data.latitude is not None and model_data.longitude is not None:
            calldata.latlong = LatLong(lat=model_data.latitude, long=model_data.longitude)
        calldata.social_media = dataclasses.SocialMedia(website=model_data.website)
        calldata.itu_zone = model_data.itu
        calldata.cq_zone = model_data.cq
        calldata.iota = model_data.iota
        calldata.plot = model_data.plot
        calldata.dok = model_data.dok
        calldata.sondok = model_data.sondok
        calldata.image = dataclasses.Image(url=model_data.qslpic)
        calldata.dxcc_prefix = model_data.prefix
        calldata.url = f"https://www.qrzcq.com/call/{model_data.call}"

        return calldata
