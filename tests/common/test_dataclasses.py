import pytest

from callsignlookuptools.common import dataclasses as dc
from callsignlookuptools.common.enums import QslStatus


dxcc_test_data = [
    pytest.param(1, "Test",
                 "Test (1)", id="full"),
    pytest.param(50, None,
                 "50", id="id_only"),
    pytest.param(None, "Test",
                 "Test", id="name_only"),
    pytest.param(None, None,
                 "", id="empty"),
]


@pytest.mark.parametrize("id,name,expected", dxcc_test_data)
def test_dxcc_str(id, name, expected):
    assert str(dc.Dxcc(id=id, name=name)) == expected


address_test_data = [
    pytest.param("Someone", "123 Main St", "Apt 102B", "Room 3", "New York", "NY", "12345", "United States", 10,
                 "Someone\n123 Main St\nApt 102B\nRoom 3\nNew York, NY 12345\nUnited States", id="full"),
    pytest.param(None, "123 Main St", "Apt 102B", "Room 3", "New York", "NY", "12345", "United States", 10,
                 "123 Main St\nApt 102B\nRoom 3\nNew York, NY 12345\nUnited States", id="no_attn"),
    pytest.param("Someone", None, "Apt 102B", "Room 3", "New York", "NY", "12345", "United States", 10,
                 "Someone\nApt 102B\nRoom 3\nNew York, NY 12345\nUnited States", id="no_line1"),
    pytest.param("Someone", "123 Main St", None, "Room 3", "New York", "NY", "12345", "United States", 10,
                 "Someone\n123 Main St\nRoom 3\nNew York, NY 12345\nUnited States", id="no_line2"),
    pytest.param("Someone", "123 Main St", "Apt 102B", None, "New York", "NY", "12345", "United States", 10,
                 "Someone\n123 Main St\nApt 102B\nNew York, NY 12345\nUnited States", id="no_line3"),
    pytest.param("Someone", "123 Main St", "Apt 102B", "Room 3", None, "NY", "12345", "United States", 10,
                 "Someone\n123 Main St\nApt 102B\nRoom 3\nNY 12345\nUnited States", id="no_city"),
    pytest.param("Someone", "123 Main St", "Apt 102B", "Room 3", "New York", None, "12345", "United States", 10,
                 "Someone\n123 Main St\nApt 102B\nRoom 3\nNew York, 12345\nUnited States", id="no_state"),
    pytest.param("Someone", "123 Main St", "Apt 102B", "Room 3", "New York", "NY", None, "United States", 10,
                 "Someone\n123 Main St\nApt 102B\nRoom 3\nNew York, NY\nUnited States", id="no_zip"),
    pytest.param("Someone", "123 Main St", "Apt 102B", "Room 3", "New York", "NY", "12345", None, 10,
                 "Someone\n123 Main St\nApt 102B\nRoom 3\nNew York, NY 12345", id="no_country"),
    pytest.param("Someone", "123 Main St", "Apt 102B", "Room 3", "New York", "NY", "12345", "United States", None,
                 "Someone\n123 Main St\nApt 102B\nRoom 3\nNew York, NY 12345\nUnited States", id="no_country_code"),
    pytest.param("Someone", "123 Main St", "Apt 102B", "Room 3", None, None, None, "United States", 10,
                 "Someone\n123 Main St\nApt 102B\nRoom 3\nUnited States", id="no_city_state_zip"),
    pytest.param("Someone", "123 Main St", "Apt 102B", "Room 3", None, None, "12345", "United States", 10,
                 "Someone\n123 Main St\nApt 102B\nRoom 3\n12345\nUnited States", id="no_city_state"),
    pytest.param("Someone", "123 Main St", "Apt 102B", "Room 3", "New York", None, None, "United States", 10,
                 "Someone\n123 Main St\nApt 102B\nRoom 3\nNew York\nUnited States", id="no_state_zip"),
    pytest.param("Someone", "123 Main St", "Apt 102B", "Room 3", None, "NY", None, "United States", 10,
                 "Someone\n123 Main St\nApt 102B\nRoom 3\nNY\nUnited States", id="no_city_zip"),
    pytest.param(None, None, None, None, None, None, None, None, None,
                 "", id="empty"),
]


@pytest.mark.parametrize("attn,line1,line2,line3,city,state,zip,country,country_code,expected", address_test_data)
def test_address_str(attn, line1, line2, line3, city, state, zip, country, country_code, expected):
    addr = dc.Address(
        attn=attn,
        line1=line1,
        line2=line2,
        line3=line3,
        city=city,
        state=state,
        zip=zip,
        country=country,
        country_code=country_code,
    )
    assert str(addr) == expected


name_test_data = [
    pytest.param("Margaret H", "Hamilton", "Maggie", 'Margaret H "Maggie" Hamilton',
                 'Margaret H "Maggie" Hamilton', id="full"),
    pytest.param("Margaret H", "Hamilton", "Maggie", None,
                 'Margaret H "Maggie" Hamilton', id="no_fmt"),
    pytest.param(None, "Hamilton", "Maggie", None,
                 '"Maggie" Hamilton', id="no_fmt_first"),
    pytest.param("Margaret H", None, "Maggie", None,
                 'Margaret H "Maggie"', id="no_fmt_name"),
    pytest.param("Margaret H", "Hamilton", None, None,
                 "Margaret H Hamilton", id="no_fmt_nickname"),
    pytest.param(None, None, "Maggie", None,
                 "Maggie", id="no_fmt_first_name"),
    pytest.param(None, "Hamilton", None, None,
                 "Hamilton", id="no_fmt_first_nickname"),
    pytest.param("Margaret H", None, None, None,
                 "Margaret H", id="no_fmt_name_nickname"),
    pytest.param(None, None, None, None,
                 "", id="empty"),
]


@pytest.mark.parametrize("first,name,nickname,formatted_name,expected", name_test_data)
def test_name_str(first, name, nickname, formatted_name, expected):
    n = dc.Name(
        first=first,
        name=name,
        nickname=nickname,
        formatted_name=formatted_name
    )
    assert str(n) == expected


trustee_test_data = [
    pytest.param("N0CALL", "Grace Hopper",
                 "Grace Hopper (N0CALL)", id="full"),
    pytest.param("N0CALL", None,
                 "N0CALL", id="callsign_only"),
    pytest.param(None, "Grace Hopper",
                 "Grace Hopper", id="name_only"),
    pytest.param(None, None,
                 "", id="empty"),
]


@pytest.mark.parametrize("callsign,name,expected", trustee_test_data)
def test_trustee_str(callsign, name, expected):
    assert str(dc.Trustee(callsign=callsign, name=name)) == expected


qsl_test_data = [
    pytest.param("SASE Please", "No Bureau", QslStatus.YES, QslStatus.NO, QslStatus.UNKNOWN, QslStatus.UNKNOWN,
                 "SASE Please\nNo Bureau\nMail: Yes\nBureau: No\nLotW: Unknown\neQSL: Unknown", id="full"),
    pytest.param(None, "No Bureau", QslStatus.YES, QslStatus.NO, QslStatus.UNKNOWN, QslStatus.UNKNOWN,
                 "No Bureau\nMail: Yes\nBureau: No\nLotW: Unknown\neQSL: Unknown", id="full"),
    pytest.param("SASE Please", None, QslStatus.YES, QslStatus.NO, QslStatus.UNKNOWN, QslStatus.UNKNOWN,
                 "SASE Please\nMail: Yes\nBureau: No\nLotW: Unknown\neQSL: Unknown", id="full"),
    pytest.param(None, None, QslStatus.UNKNOWN, QslStatus.UNKNOWN, QslStatus.UNKNOWN, QslStatus.UNKNOWN,
                 "Mail: Unknown\nBureau: Unknown\nLotW: Unknown\neQSL: Unknown", id="empty"),
]


@pytest.mark.parametrize("info,bureau_info,mail,bureau,lotw,eqsl,expected", qsl_test_data)
def test_qsl_str(info, bureau_info, mail, bureau, lotw, eqsl, expected):
    qsl = dc.Qsl(
        info=info,
        bureau_info=bureau_info,
        eqsl=eqsl,
        lotw=lotw,
        mail=mail,
        bureau=bureau,
    )
    assert str(qsl) == expected
