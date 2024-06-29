from datetime import date
from pathlib import Path

import pytest
from pytest_httpx import HTTPXMock

from brreg import enhetsregisteret

DATA_DIR = Path(__file__).parent.parent / "data"


def test_get_underenhet(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(  # pyright: ignore[reportUnknownMemberType]
        method="GET",
        url="https://data.brreg.no/enhetsregisteret/api/underenheter/776655441",
        status_code=200,
        headers={"content-type": "application/json"},
        content=(DATA_DIR / "underenheter-details-response.json").read_bytes(),
    )

    org = enhetsregisteret.Client().get_underenhet("776655441")

    assert org is not None
    assert org.organisasjonsnummer == "776655441"
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
    assert org.beliggenhetsadresse == enhetsregisteret.Adresse(
        land="Norge",
        landkode="NO",
        postnummer="0122",
        poststed="OSLO",
        adresse=["Tyvholmen 1", None, None],
        kommune="OSLO",
        kommunenummer="0301",
    )
    assert org.oppstartsdato is None
    assert org.dato_eierskifte is None
    assert org.nedleggelsesdato == date(2018, 10, 20)
    assert org.slettedato is None


def test_get_underenhet_with_spaces_in_organisasjonsnummer(
    httpx_mock: HTTPXMock,
) -> None:
    httpx_mock.add_response(  # pyright: ignore[reportUnknownMemberType]
        method="GET",
        url="https://data.brreg.no/enhetsregisteret/api/underenheter/776655441",
        status_code=200,
        headers={"content-type": "application/json"},
        content=(DATA_DIR / "underenheter-details-response.json").read_bytes(),
    )

    org = enhetsregisteret.Client().get_underenhet("776 655 441")

    assert org is not None
    assert org.organisasjonsnummer == "776655441"


def test_get_underenhet_when_deleted(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(  # pyright: ignore[reportUnknownMemberType]
        method="GET",
        url="https://data.brreg.no/enhetsregisteret/api/underenheter/987123456",
        status_code=200,
        headers={"content-type": "application/json"},
        content=(DATA_DIR / "underenheter-details-deleted-response.json").read_bytes(),
    )

    org = enhetsregisteret.Client().get_underenhet("987123456")

    assert org is not None
    assert org.organisasjonsnummer == "987123456"
    assert org.navn == "SLETTET UNDERENHET AS"
    assert org.organisasjonsform == enhetsregisteret.Organisasjonsform(
        kode="AAFY",
        beskrivelse="Virksomhet til ikke-næringsdrivende person",
        utgaatt=None,
    )
    assert org.slettedato == date(2017, 10, 20)


@pytest.mark.parametrize("status_code", [404, 410])
def test_get_underenhet_when_4xx(httpx_mock: HTTPXMock, status_code: int) -> None:
    httpx_mock.add_response(  # pyright: ignore[reportUnknownMemberType]
        method="GET",
        url="https://data.brreg.no/enhetsregisteret/api/underenheter/987123456",
        status_code=status_code,
        headers={"content-type": "application/json"},
    )

    org = enhetsregisteret.Client().get_underenhet("987123456")

    assert org is None
