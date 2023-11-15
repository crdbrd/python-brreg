from datetime import date

import httpx
import pytest
from pytest_httpx import HTTPXMock

from brreg import BrregRestError, enhetsregisteret


def test_get_enhet(
    httpx_mock: HTTPXMock,
    organization_details_response: bytes,
) -> None:
    httpx_mock.add_response(  # pyright: ignore[reportUnknownMemberType]
        method="GET",
        url="https://data.brreg.no/enhetsregisteret/api/enheter/818511752",
        status_code=200,
        headers={"content-type": "application/json"},
        content=organization_details_response,
    )

    org = enhetsregisteret.Client().get_enhet("818511752")

    assert org is not None
    assert org.organisasjonsnummer == "818511752"
    assert org.navn == "SESAM STASJON"
    assert org.hjemmeside is None
    assert org.registreringsdato_enhetsregisteret == date(2017, 10, 20)
    assert org.registrert_i_mvaregisteret is True
    assert org.naeringskode1 == enhetsregisteret.Naeringskode(
        kode="52.292", beskrivelse="Skipsmegling"
    )
    assert org.antall_ansatte == 50
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


def test_get_enhet_when_deleted(
    httpx_mock: HTTPXMock,
    deleted_organization_details_response: bytes,
) -> None:
    httpx_mock.add_response(  # pyright: ignore[reportUnknownMemberType]
        method="GET",
        url="https://data.brreg.no/enhetsregisteret/api/enheter/815597222",
        status_code=200,
        headers={"content-type": "application/json"},
        content=deleted_organization_details_response,
    )

    org = enhetsregisteret.Client().get_enhet("815597222")

    assert org is not None
    assert org.organisasjonsnummer == "815597222"
    assert org.navn == "SLETTET ENHET AS"
    assert org.organisasjonsform == enhetsregisteret.Organisasjonsform(
        kode="UTBG", beskrivelse="Frivillig registrert utleiebygg"
    )
    assert org.slettedato == date(2017, 10, 20)


def test_get_enhet_when_gone(
    httpx_mock: HTTPXMock,
) -> None:
    httpx_mock.add_response(  # pyright: ignore[reportUnknownMemberType]
        method="GET",
        url="https://data.brreg.no/enhetsregisteret/api/enheter/818511752",
        status_code=410,
        headers={"content-type": "application/json"},
    )

    org = enhetsregisteret.Client().get_enhet("818511752")

    assert org is None


def test_get_enhet_when_not_found(
    httpx_mock: HTTPXMock,
) -> None:
    httpx_mock.add_response(  # pyright: ignore[reportUnknownMemberType]
        method="GET",
        url="https://data.brreg.no/enhetsregisteret/api/enheter/818511752",
        status_code=404,
        headers={"content-type": "application/json"},
    )

    org = enhetsregisteret.Client().get_enhet("818511752")

    assert org is None


def test_get_enhet_when_http_error(
    httpx_mock: HTTPXMock,
) -> None:
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


def test_get_organization_by_number_when_http_timeout(
    httpx_mock: HTTPXMock,
) -> None:
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
