"""
Tests for the QRZCALL.EU provider — parsing the JSON envelope returned by
``/v1/pub/callsign_json.php`` into the unified ``CallsignData`` shape.

Fixture-based (no network). Mirrors the existing project test style.
"""


import pytest

from callsignlookuptools.common.enums import (
    Continent,
    DataSource,
    QslStatus,
)
from callsignlookuptools.common.exceptions import CallsignLookupError
from callsignlookuptools.qrzcall.qrzcall import (
    QrzcallDataModel,
    _continent_to_enum,
)
from callsignlookuptools.qrzcall.qrzcallsync import QrzcallSyncClient


# A real production response for PA4R (Data-tier PAT, captured live).
PA4R_BODY = (
    b'{"success":true,"api":"QRZCALL JSON API v1.0","data":{'
    b'"callsign":"PA4R","prev_call":null,"firstname":"Ronald","lastname":"DHer",'
    b'"nickname":"Ron","born":1965,"email":"deheer.r@gmail.com",'
    b'"url":"http://www.qrzcall.eu","address1":"address 1","address2":"address 2",'
    b'"zip":"zip","qth":"Wijk en Aalburg","state":"NB","county":null,'
    b'"country":"Netherlands","dxcc":263,"dxcc_country":"Netherlands","continent":"EU",'
    b'"lat":51.760403,"lon":5.111732,"ituzone":"27","cqzone":"14",'
    b'"gridsquare":"JO21NS","iota":null,"pota":null,"sota":null,"wwff":null,'
    b'"lic_class":"F","lic_efdate":"2019-01-09","lic_expdate":null,'
    b'"lotw":1,"eqsl":0,"mqsl":1,"qslinfo":"Via Buro (Veron)",'
    b'"image":"https://qrzcall.eu/uploads/callsigns/PA4R.___","views":247,'
    b'"created":"2026-02-12 13:11:08","updated":"2026-03-13 12:02:39"}}'
)


def _client():
    """A real ``QrzcallSyncClient`` instance for calling ``_process_search``
    directly. The constructor does not make any network requests — it only
    stashes the token and constructs a ``requests.Session`` — so this is
    safe in unit tests without mocks."""
    return QrzcallSyncClient(token="unused-for-parsing-tests")


# ── happy path ─────────────────────────────────────────────────────────────

class TestHappyPath:
    @classmethod
    def setup_class(cls):
        cls.data = _client()._process_search(query="PA4R", resp=PA4R_BODY)

    def test_data_source_is_qrzcall(self):
        assert self.data.data_source is DataSource.QRZCALL

    def test_callsign_returned_from_server(self):
        assert self.data.callsign == "PA4R"

    def test_query_preserved(self):
        assert self.data.query == "PA4R"

    def test_raw_data_is_pydantic_model(self):
        assert isinstance(self.data.raw_data, QrzcallDataModel)

    def test_name_fields(self):
        assert self.data.name.first == "Ronald"
        assert self.data.name.name == "DHer"
        assert self.data.name.nickname == "Ron"

    def test_address_city_is_from_qth(self):
        # QRZCALL keeps city separate from street address1/address2 — qth → city
        assert self.data.address.line1 == "address 1"
        assert self.data.address.line2 == "address 2"
        assert self.data.address.city == "Wijk en Aalburg"
        assert self.data.address.state == "NB"
        assert self.data.address.zip == "zip"
        assert self.data.address.country == "Netherlands"
        assert self.data.address.country_code == 263

    def test_dxcc(self):
        assert self.data.dxcc.id == 263
        assert self.data.dxcc.name == "Netherlands"

    def test_continent_maps_to_enum(self):
        assert self.data.continent is Continent.EU

    def test_latlong_set(self):
        assert self.data.latlong is not None
        assert self.data.latlong.lat == pytest.approx(51.760403)
        assert self.data.latlong.long == pytest.approx(5.111732)

    def test_grid_is_gridtools_grid(self):
        # gridtools `Grid` normalises subsquare letters to lowercase (the
        # conventional Maidenhead form), so we compare case-insensitively.
        assert self.data.grid is not None
        assert str(self.data.grid).upper() == "JO21NS"

    def test_zones(self):
        assert self.data.cq_zone == 14
        assert self.data.itu_zone == 27

    def test_license_class_passthrough(self):
        # QRZCALL returns free-form strings (e.g. 'F', 'Full', country-specific
        # codes); the field stores the string as-is.
        assert self.data.lic_class == "F"

    def test_license_dates(self):
        assert self.data.effective_date.isoformat() == "2019-01-09T00:00:00"
        assert self.data.expire_date is None

    def test_qsl_statuses(self):
        assert self.data.qsl.lotw is QslStatus.YES
        assert self.data.qsl.eqsl is QslStatus.NO
        assert self.data.qsl.mail is QslStatus.YES
        assert self.data.qsl.info == "Via Buro (Veron)"

    def test_email_and_url_top_level(self):
        # These live on CallsignData directly, not under social_media
        assert self.data.email == "deheer.r@gmail.com"
        assert self.data.url == "http://www.qrzcall.eu"

    def test_image_url(self):
        assert self.data.image.url == "https://qrzcall.eu/uploads/callsigns/PA4R.___"

    def test_born(self):
        assert self.data.born == 1965

    def test_views(self):
        assert self.data.page_views == 247

    def test_modified_date(self):
        assert self.data.modified_date.isoformat() == "2026-03-13T12:02:39"


# ── error / edge paths ─────────────────────────────────────────────────────

def test_missing_data_raises():
    """The endpoint returns `{error: "..."}` (no `data`) when something
    upstream is wrong. `_process_search` should surface the message as a
    `CallsignLookupError` rather than crashing on a KeyError."""
    body = b'{"error":"Internal database error"}'
    with pytest.raises(CallsignLookupError) as exc:
        _client()._process_search(query="PA4R", resp=body)
    assert "Internal database error" in str(exc.value)


def test_404_style_body_raises_friendly_message():
    """The 404 HTTP path is normally caught in `_do_query` (network layer),
    but if a future server change ever returns a 200 with a `success:false`
    body the same error should surface cleanly."""
    body = b'{"error":"Callsign not found: XX9XX9XX"}'
    with pytest.raises(CallsignLookupError) as exc:
        _client()._process_search(query="XX9XX9XX", resp=body)
    assert "Callsign not found" in str(exc.value)


def test_malformed_json_raises():
    with pytest.raises(CallsignLookupError) as exc:
        _client()._process_search(query="PA4R", resp=b"not-json")
    assert "Could not parse" in str(exc.value)


def test_minimal_response_does_not_crash():
    """Most fields are nullable on the server. A near-empty `data` object
    should still produce a `CallsignData` populated mostly with `None` and
    no exceptions raised."""
    body = b'{"success":true,"api":"x","data":{"callsign":"PA4R","continent":"EU"}}'
    data = _client()._process_search(query="PA4R", resp=body)
    assert data.callsign == "PA4R"
    assert data.continent is Continent.EU
    # Sub-objects are still present (built from the empty source fields)
    assert data.address is not None and data.address.city is None
    assert data.qsl is not None and data.qsl.lotw is QslStatus.UNKNOWN
    assert data.email is None


# ── continent enum mapping helper ──────────────────────────────────────────

@pytest.mark.parametrize("code,expected", [
    ("EU", Continent.EU),
    ("NA", Continent.NA),
    ("SA", Continent.SA),
    ("AS", Continent.AS),
    ("AF", Continent.AF),
    ("OC", Continent.OC),
    ("AN", Continent.AN),
    ("",   Continent.NONE),
    (None, Continent.NONE),
    ("ZZ", Continent.NONE),  # unknown code falls through to NONE
])
def test_continent_to_enum(code, expected):
    assert _continent_to_enum(code) is expected
