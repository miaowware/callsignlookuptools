"""
common functions for callsignlookuptools
---
Copyright 2021-2023 classabbyamp, 0x5c
Released under the terms of the BSD 3-Clause license.
"""


from typing import Dict, Union
from io import BytesIO

from lxml import etree


def xml2dict(xml: Union[bytes, etree._Element], to_lower: bool = True) -> Dict:
    """Convert an lxml.etree node tree into a dict"""
    if isinstance(xml, bytes):
        node = etree.parse(BytesIO(xml)).getroot()
    else:
        node = xml

    result: Dict = {}

    for element in node.iterchildren():
        # Remove namespace prefix
        key = element.tag.split('}')[1] if '}' in element.tag else element.tag
        if to_lower:
            key = key.lower()

        value: Union[str, bytes, Dict]

        # Process element as tree element if the inner XML contains non-whitespace content
        if element.text and element.text.strip():
            value = element.text
        else:
            value = xml2dict(element, to_lower=to_lower)
        if key in result:
            if type(result[key]) is list:
                result[key].append(value)
            else:
                tempvalue = result[key].copy()
                result[key] = [tempvalue, value]
        else:
            result[key] = value
    return result


def is_callsign(callsign: str) -> bool:
    """Check if a callsign is valid"""
    return callsign.isascii() and callsign.replace("/", "").isalnum()
