from unittest import TestCase
from io import BytesIO

import pytest
from lxml import etree

from callsignlookuptools.common import functions


with open("tests/common/xml2dict_input.xml", "rb") as f:
    xml2dict_input_bytes = f.read()
    xml2dict_input_etree = etree.parse(BytesIO(xml2dict_input_bytes)).getroot()


xml2dict_expected = {
    "Callsign": {
        "call": "W1AW",
        "dxcc": "291",
        "attn": "JOSEPH P CARCIA III",
        "name": "ARRL HQ OPERATORS CLUB",
        "addr1": "225 MAIN ST",
        "addr2": "NEWINGTON",
        "MSA": "3280",
        "AreaCode": "860",
        "TimeZone": "Eastern",
        "GMTOffset": "-5",
    },
    "Session": {
        "Key": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "Count": "3543",
        "SubExp": "Fri Oct 15 17:21:54 2021",
        "GMTime": "Wed Apr 28 02:24:54 2021",
        "Remark": "cpu: 0.041s",
    },
}


xml2dict_lower_expected = {
    "callsign": {
        "call": "W1AW",
        "dxcc": "291",
        "attn": "JOSEPH P CARCIA III",
        "name": "ARRL HQ OPERATORS CLUB",
        "addr1": "225 MAIN ST",
        "addr2": "NEWINGTON",
        "msa": "3280",
        "areacode": "860",
        "timezone": "Eastern",
        "gmtoffset": "-5",
    },
    "session": {
        "key": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "count": "3543",
        "subexp": "Fri Oct 15 17:21:54 2021",
        "gmtime": "Wed Apr 28 02:24:54 2021",
        "remark": "cpu: 0.041s",
    },
}


xml2dict_test_data = [
    pytest.param(xml2dict_input_bytes, False,
                 xml2dict_expected, id="preserve_key_case_bytes"),
    pytest.param(xml2dict_input_bytes, True,
                 xml2dict_lower_expected, id="lower_keys_bytes"),
    pytest.param(xml2dict_input_etree, False,
                 xml2dict_expected, id="preserve_key_case_etree"),
    pytest.param(xml2dict_input_etree, True,
                 xml2dict_lower_expected, id="lower_keys_etree"),
]


@pytest.mark.parametrize("xml,to_lower,expected", xml2dict_test_data)
def test_xml2dict(xml, to_lower, expected):
    tc = TestCase()
    tc.maxDiff = None
    tc.assertDictEqual(functions.xml2dict(xml, to_lower=to_lower), expected)
