"""
qrzcalltools
---
Released under the terms of the BSD 3-Clause license.
"""


from abc import ABC, abstractmethod
import json
from typing import Optional
from datetime import datetime

from gridtools import Grid, LatLong
from pydantic import BaseModel, Field, validator

from ..common import abcs, enums, dataclasses, exceptions
from ..common.constants import DEFAULT_USERAGENT


class QrzcallDataModel(BaseModel):
    """Pydantic model matching the ``data`` object returned by the
    QRZCALL.EU JSON endpoint (``/v1/pub/callsign_json.php``).

    Fields are nullable because the server emits ``null`` for any column it
    has no data for.
    """
    callsign: Optional[str] = None
    prev_call: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    nickname: Optional[str] = None
    born: Optional[int] = None
    email: Optional[str] = None
    url: Optional[str] = None
    address1: Optional[str] = None
    address2: Optional[str] = None
    zip: Optional[str] = None
    qth: Optional[str] = None
    state: Optional[str] = None
    county: Optional[str] = None
    country: Optional[str] = None
    dxcc: Optional[int] = None
    dxcc_country: Optional[str] = None
    continent: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    ituzone: Optional[int] = None
    cqzone: Optional[int] = None
    gridsquare: Optional[Grid] = None
    iota: Optional[str] = None
    pota: Optional[str] = None
    sota: Optional[str] = None
    wwff: Optional[str] = None
    lic_class: Optional[str] = None
    lic_efdate: Optional[datetime] = None
    lic_expdate: Optional[datetime] = None
    lotw: enums.QslStatus = enums.QslStatus.UNKNOWN
    eqsl: enums.QslStatus = enums.QslStatus.UNKNOWN
    mqsl: enums.QslStatus = enums.QslStatus.UNKNOWN
    qslinfo: Optional[str] = None
    image: Optional[str] = None
    views: Optional[int] = None
    created: Optional[datetime] = None
    updated: Optional[datetime] = None

    @validator("gridsquare", pre=True)
    def _to_grid(cls, v):
        if not v:
            return None
        if isinstance(v, str):
            return Grid(v)
        return v

    @validator("lic_efdate", "lic_expdate", "created", "updated", pre=True)
    def _parse_date(cls, v):
        if v in (None, "", "0000-00-00"):
            return None
        if isinstance(v, str):
            # Server emits dates as 'YYYY-MM-DD' and datetimes as
            # 'YYYY-MM-DD HH:MM:SS'. Try both, in that order.
            for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S"):
                try:
                    return datetime.strptime(v, fmt)
                except ValueError:
                    continue
            return None
        return v

    @validator("lotw", "eqsl", "mqsl", pre=True)
    def _parse_qsl_status(cls, v):
        # Server emits 0/1 as ints (per callsign_json.php's mapCallsign cast).
        if v == 1 or v == "1" or v is True:
            return enums.QslStatus.YES
        if v == 0 or v == "0" or v is False:
            return enums.QslStatus.NO
        return enums.QslStatus.UNKNOWN

    @validator("dxcc", "born", "ituzone", "cqzone", "views", pre=True)
    def _empty_int(cls, v):
        # Coerce empty string / null to None so int parsing doesn't fail.
        if v in (None, ""):
            return None
        return v

    @validator("lat", "lon", pre=True)
    def _empty_float(cls, v):
        if v in (None, ""):
            return None
        return v

    class Config:
        str_strip_whitespace = True
        arbitrary_types_allowed = True


def _continent_to_enum(code: Optional[str]) -> enums.Continent:
    """Map the QRZCALL 2-letter continent code (e.g. 'EU') to the
    Continent enum member. Returns ``Continent.NONE`` on miss."""
    if not code:
        return enums.Continent.NONE
    try:
        return enums.Continent[code.upper()]
    except KeyError:
        return enums.Continent.NONE


class QrzcallClientAbc(abcs.LookupAbc, ABC):
    """The base class for QrzcallSyncClient and QrzcallAsyncClient.
    **This should not be used directly.**
    """
    _base_url = "https://api.qrzcall.eu/v1/pub/callsign_json.php"

    def __init__(self, token: str, useragent: str = DEFAULT_USERAGENT):
        self._token = token
        self._useragent = useragent

    @abstractmethod
    def search(self, callsign: str) -> dataclasses.CallsignData:
        pass

    @abstractmethod
    def _do_query(self, **query) -> bytes:
        pass

    def _process_search(self, query: str, resp: bytes) -> dataclasses.CallsignData:
        try:
            envelope = json.loads(resp)
        except json.JSONDecodeError as e:
            raise exceptions.CallsignLookupError(
                f"Could not parse QRZCALL.EU response: {e}"
            )

        # The endpoint returns either:
        #   { "success": true, "api": "...", "data": { ... } }   on a hit
        #   { "error": "..." }                                   on a miss/error
        # 4xx HTTP statuses also carry the error body, which _do_query has
        # raised before reaching here for non-200 codes — but in case the
        # server ever changes shape, surface a clear message.
        if "data" not in envelope or not envelope.get("data"):
            err = envelope.get("error") or "No data found"
            raise exceptions.CallsignLookupError(f"{err} for query {query}")

        model_data = QrzcallDataModel.parse_obj(envelope["data"])

        calldata = dataclasses.CallsignData(
            query=query,
            raw_data=model_data,
            data_source=enums.DataSource.QRZCALL,
        )

        calldata.callsign = model_data.callsign or query

        # prev_call is a comma-separated list on the server. Store the first
        # one as the singular ``prev_call`` and the whole split list as
        # ``aliases``, matching the convention QRZ uses for <aliases>.
        if model_data.prev_call:
            parts = [p.strip() for p in model_data.prev_call.split(",") if p.strip()]
            if parts:
                calldata.aliases = parts
                calldata.prev_call = parts[0]

        # Name
        if any((model_data.firstname, model_data.lastname, model_data.nickname)):
            calldata.name = dataclasses.Name(
                first=model_data.firstname,
                name=model_data.lastname,
                nickname=model_data.nickname,
            )

        # Address — server splits the city ('qth') from the street ('address1'/
        # 'address2'), so qth -> Address.city (not Address.attn).
        calldata.address = dataclasses.Address(
            line1=model_data.address1,
            line2=model_data.address2,
            city=model_data.qth,
            state=model_data.state,
            zip=model_data.zip,
            country=model_data.country,
            country_code=model_data.dxcc,
        )

        # DXCC
        if model_data.dxcc or model_data.dxcc_country:
            calldata.dxcc = dataclasses.Dxcc(
                id=model_data.dxcc,
                name=model_data.dxcc_country,
            )

        # Continent (enum) — server returns 2-letter code; map to enum.
        calldata.continent = _continent_to_enum(model_data.continent)

        # Geolocation
        if model_data.lat is not None and model_data.lon is not None:
            calldata.latlong = LatLong(lat=model_data.lat, long=model_data.lon)
        calldata.grid = model_data.gridsquare
        calldata.county = model_data.county
        calldata.cq_zone = model_data.cqzone
        calldata.itu_zone = model_data.ituzone
        calldata.iota = model_data.iota

        # License
        if model_data.lic_class:
            calldata.lic_class = model_data.lic_class
        calldata.effective_date = model_data.lic_efdate
        calldata.expire_date = model_data.lic_expdate

        # QSL
        calldata.qsl = dataclasses.Qsl(
            info=model_data.qslinfo,
            eqsl=model_data.eqsl,
            lotw=model_data.lotw,
            mail=model_data.mqsl,
        )

        # Bio / metadata
        calldata.born = model_data.born
        calldata.email = model_data.email
        calldata.url = model_data.url or f"https://qrzcall.eu/lookup/{calldata.callsign}"
        calldata.page_views = model_data.views
        calldata.modified_date = model_data.updated

        if model_data.image:
            calldata.image = dataclasses.Image(url=model_data.image)

        return calldata
