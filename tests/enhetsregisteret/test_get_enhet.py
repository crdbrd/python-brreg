from datetime import date
from pathlib import Path

import httpx
import pytest
from pytest_httpx import HTTPXMock

import brreg
from brreg import BrregError, BrregRestError, enhetsregisteret

DATA_DIR = Path(__file__).parent.parent / "data"


def test_get_enhet(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(  # pyright: ignore[reportUnknownMemberType]
        method="GET",
        url="https://data.brreg.no/enhetsregisteret/api/enheter/112233445",
        status_code=200,
        headers={"content-type": "application/json"},
        content=(DATA_DIR / "enheter-details-response.json").read_bytes(),
    )

    org = enhetsregisteret.Client().get_enhet("112233445")

    requests = httpx_mock.get_requests()  # pyright: ignore[reportUnknownMemberType]
    assert len(requests) == 1
    assert (
        requests[0].headers["user-agent"]
        == f"python-brreg/{brreg.__version__} python-httpx/{httpx.__version__}"
    )

    assert org is not None
    assert org.organisasjonsnummer == "112233445"
    assert org.navn == "SESAM STASJON"
    assert org.hjemmeside is None
    assert org.registreringsdato_enhetsregisteret == date(2017, 10, 20)
    assert org.registrert_i_mvaregisteret is True
    assert org.naeringskode1 == enhetsregisteret.Naering(
        kode="52.292",
        beskrivelse="Skipsmegling",
    )
    assert org.antall_ansatte == 50
    assert org.har_registrert_antall_ansatte is True
    assert org.forretningsadresse == enhetsregisteret.Adresse(
        land="Norge",
        landkode="NO",
        postnummer="0101",
        poststed="OSLO",
        adresse=["Tyvholmen 1", None, None, ""],
        kommune="OSLO",
        kommunenummer="0301",
    )
    assert org.stiftelsesdato == date(2017, 10, 20)
    assert org.institusjonell_sektorkode is None
    assert org.registrert_i_foretaksregisteret is True
    assert org.registrert_i_stiftelsesregisteret is False
    assert org.registrert_i_frivillighetsregisteret is False
    assert org.siste_innsendte_aarsregnskap is None
    assert org.konkurs is False
    assert org.under_avvikling is False
    assert org.under_tvangsavvikling_eller_tvangsopplosning is False
    assert org.maalform == "Bokmål"
    assert org.slettedato is None


def test_get_enhet_with_spaces_in_organisasjonsnummer(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(  # pyright: ignore[reportUnknownMemberType]
        method="GET",
        url="https://data.brreg.no/enhetsregisteret/api/enheter/112233445",
        status_code=200,
        headers={"content-type": "application/json"},
        content=(DATA_DIR / "enheter-details-response.json").read_bytes(),
    )

    org = enhetsregisteret.Client().get_enhet("112 233 445")

    assert org is not None
    assert org.organisasjonsnummer == "112233445"


def test_get_enhet_when_deleted(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(  # pyright: ignore[reportUnknownMemberType]
        method="GET",
        url="https://data.brreg.no/enhetsregisteret/api/enheter/123456789",
        status_code=200,
        headers={"content-type": "application/json"},
        content=(DATA_DIR / "enheter-details-deleted-response.json").read_bytes(),
    )

    org = enhetsregisteret.Client().get_enhet("123456789")

    assert org is not None
    assert org.organisasjonsnummer == "123456789"
    assert org.navn == "SLETTET ENHET AS"
    assert org.organisasjonsform == enhetsregisteret.Organisasjonsform(
        kode="UTBG",
        beskrivelse="Frivillig registrert utleiebygg",
        utgaatt=date(2017, 7, 17),
    )
    assert org.slettedato == date(2017, 10, 20)


@pytest.mark.parametrize("status_code", [404, 410])
def test_get_enhet_when_4xx(httpx_mock: HTTPXMock, status_code: int) -> None:
    httpx_mock.add_response(  # pyright: ignore[reportUnknownMemberType]
        method="GET",
        url="https://data.brreg.no/enhetsregisteret/api/enheter/818511752",
        status_code=status_code,
        headers={"content-type": "application/json"},
    )

    org = enhetsregisteret.Client().get_enhet("818511752")

    assert org is None


def test_get_enhet_when_bad_request(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(  # pyright: ignore[reportUnknownMemberType]
        method="GET",
        url="https://data.brreg.no/enhetsregisteret/api/enheter/818511752",
        status_code=400,
        headers={"content-type": "application/json"},
    )

    with pytest.raises(BrregRestError) as exc_info:
        enhetsregisteret.Client().get_enhet("818511752")

    assert "REST API exception" in str(exc_info.value)
    assert "Bad Request" in str(exc_info.value)

    assert exc_info.value.method == "GET"
    assert (
        exc_info.value.url
        == "https://data.brreg.no/enhetsregisteret/api/enheter/818511752"
    )
    assert exc_info.value.status_code == 400


def test_get_enhet_when_http_timeout(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_exception(  # pyright: ignore[reportUnknownMemberType]
        httpx.ConnectTimeout("Connection refused"),
    )

    with pytest.raises(BrregRestError) as exc_info:
        enhetsregisteret.Client().get_enhet("818511752")

    assert "REST API exception" in str(exc_info.value)
    assert "Connection refused" in str(exc_info.value)

    assert exc_info.value.method == "GET"
    assert (
        exc_info.value.url
        == "https://data.brreg.no/enhetsregisteret/api/enheter/818511752"
    )
    assert exc_info.value.status_code is None


def test_get_enhet_when_other_error(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_exception(  # pyright: ignore[reportUnknownMemberType]
        RuntimeError("Something else than HTTP failed"),
    )

    with pytest.raises(BrregError) as exc_info:
        enhetsregisteret.Client().get_enhet("818511752")

    assert "Something else than HTTP failed" in str(exc_info.value)

    # The BrregError wraps the original exception
    assert isinstance(exc_info.value.__cause__, RuntimeError)
