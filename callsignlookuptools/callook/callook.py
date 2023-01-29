"""
callooktools
---
Copyright 2021-2023 classabbyamp, 0x5c
Released under the terms of the BSD 3-Clause license.
"""


from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime

from gridtools import Grid, LatLong
from pydantic import BaseModel, Field, validator

from ..common import abcs, enums, dataclasses, exceptions


class CallookCallsignModel(BaseModel):
    callsign: Optional[str] = None
    operClass: enums.LicenseClass = enums.LicenseClass.NONE
    class_: enums.LicenseClass = Field(default=enums.LicenseClass.NONE, alias="class")

    class Config:
        anystr_strip_whitespace = True
        arbitrary_types_allowed = True


class CallookTrusteeModel(BaseModel):
    callsign: Optional[str] = None
    name: Optional[str] = None

    class Config:
        anystr_strip_whitespace = True
        arbitrary_types_allowed = True


class CallookAddressModel(BaseModel):
    line1: Optional[str] = None
    line2: Optional[str] = None
    attn: Optional[str] = None

    class Config:
        anystr_strip_whitespace = True
        arbitrary_types_allowed = True


class CallookLocationModel(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    gridsquare: Optional[Grid] = None

    @validator("gridsquare", pre=True)
    def _to_grid(cls, v):
        if isinstance(v, str):
            return Grid(v)
        return v

    class Config:
        anystr_strip_whitespace = True
        arbitrary_types_allowed = True


class CallookOtherInfoModel(BaseModel):
    grantDate: Optional[datetime] = None
    expiryDate: Optional[datetime] = None
    lastActionDate: Optional[datetime] = None
    frn: Optional[str] = None
    ulsUrl: Optional[str] = None

    @validator("grantDate", "expiryDate", "lastActionDate", pre=True)
    def _parse_date(cls, v):
        if isinstance(v, str):
            try:
                return datetime.strptime(v, "%m/%d/%Y")
            except ValueError:
                return None
        return v

    class Config:
        anystr_strip_whitespace = True
        arbitrary_types_allowed = True


class CallookDataModel(BaseModel):
    status: enums.CallookStatus = enums.CallookStatus.VALID
    type: enums.CallsignType = enums.CallsignType.NONE
    current: CallookCallsignModel = Field(default_factory=CallookCallsignModel)
    previous: CallookCallsignModel = Field(default_factory=CallookCallsignModel)
    trustee: CallookTrusteeModel = Field(default_factory=CallookTrusteeModel)
    name: Optional[str] = None
    address: CallookAddressModel = Field(default_factory=CallookAddressModel)
    location: CallookLocationModel = Field(default_factory=CallookLocationModel)
    otherInfo: CallookOtherInfoModel = Field(default_factory=CallookOtherInfoModel)

    class Config:
        anystr_strip_whitespace = True
        arbitrary_types_allowed = True


class CallookClientAbc(abcs.LookupAbc, ABC):
    """The base class for CallookSyncClient and CallookAsyncClient. **This should not be used directly.**"""
    _base_url = "https://callook.info/{}/json"

    def __init__(self):
        pass

    @abstractmethod
    def search(self, callsign: str) -> dataclasses.CallsignData:
        pass

    @abstractmethod
    def _do_query(self, **query) -> bytes:
        pass

    def _process_search(self, query: str, resp: bytes) -> dataclasses.CallsignData:
        model_data = CallookDataModel.parse_raw(resp)

        if model_data.status != enums.CallookStatus.VALID or not model_data.current.callsign:
            raise exceptions.CallsignLookupError("No data found for query " + query)

        calldata = dataclasses.CallsignData(
            query=query,
            raw_data=model_data,
            data_source=enums.DataSource.CALLOOK
        )

        calldata.type = model_data.type
        calldata.callsign = model_data.current.callsign
        if c := model_data.current.operClass:
            calldata.lic_class = c
        elif c := model_data.current.class_:
            calldata.lic_class = c
        calldata.prev_call = model_data.previous.callsign
        if c := model_data.previous.operClass:
            calldata.prev_lic_class = c
        elif c := model_data.previous.class_:
            calldata.prev_lic_class = c
        calldata.trustee = dataclasses.Trustee(
            callsign=model_data.trustee.callsign,
            name=model_data.trustee.name
        )
        calldata.name = dataclasses.Name(name=model_data.name)
        city = None
        state = None
        zip = None
        if model_data.address.line2:
            city, state, zip = model_data.address.line2.replace(",", "").split(" ")
        calldata.address = dataclasses.Address(
            attn=model_data.address.attn,
            line1=model_data.address.line1,
            city=city,
            state=state,
            zip=zip
        )
        if model_data.location.latitude is not None and model_data.location.longitude is not None:
            calldata.latlong = LatLong(lat=model_data.location.latitude, long=model_data.location.longitude)
        calldata.grid = model_data.location.gridsquare
        calldata.effective_date = model_data.otherInfo.grantDate
        calldata.expire_date = model_data.otherInfo.expiryDate
        calldata.last_action_date = model_data.otherInfo.lastActionDate
        calldata.frn = model_data.otherInfo.frn
        calldata.uls_url = model_data.otherInfo.ulsUrl
        calldata.url = f"https://callook.info/{model_data.current.callsign}"

        return calldata
