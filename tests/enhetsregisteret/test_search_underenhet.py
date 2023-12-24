from datetime import date
from pathlib import Path

from pytest_httpx import HTTPXMock

from brreg import enhetsregisteret

DATA_DIR = Path(__file__).parent.parent / "data"


def test_underenhet_query() -> None:
    query = enhetsregisteret.UnderenhetQuery(
        navn="Sesam",
        fra_registreringsdato_enhetsregisteret=date(2015, 1, 1),
        naeringskode=["90.012", "90.013"],
    )

    assert query.navn == "Sesam"
    assert query.fra_registreringsdato_enhetsregisteret == date(2015, 1, 1)
    assert query.naeringskode == ["90.012", "90.013"]

    assert query.as_url_query() == (
        "navn=Sesam"
        "&fraRegistreringsdatoEnhetsregisteret=2015-01-01"
        "&naeringskode=90.012%2C90.013"
    )


def test_search_underenhet(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(  # pyright: ignore[reportUnknownMemberType]
        method="GET",
        url=(
            "https://data.brreg.no/enhetsregisteret/api/underenheter"
            "?navn=Sesam"
            "&fraRegistreringsdatoEnhetsregisteret=2015-01-01"
            "&naeringskode=90.012"
        ),
        status_code=200,
        headers={"content-type": "application/json"},
        content=(DATA_DIR / "underenheter-search-response.json").read_bytes(),
    )

    page = enhetsregisteret.Client().search_underenhet(
        enhetsregisteret.UnderenhetQuery(
            navn="Sesam",
            fra_registreringsdato_enhetsregisteret=date(2015, 1, 1),
            naeringskode=["90.012"],
        )
    )

    assert page.page_size == 1
    assert page.page_number == 0
    assert page.total_elements == 1
    assert page.total_pages == 1

    org = page.items[0]

    assert org is not None
    assert org.organisasjonsnummer == "334455660"
    assert org.navn == "TRYLLEBUTIKKEN SESAM"
    assert org.hjemmeside is None
    assert org.registreringsdato_enhetsregisteret == date(2017, 10, 20)
    assert org.registrert_i_mvaregisteret is True
    assert org.naeringskode1 == enhetsregisteret.Naering(
        kode="90.012",
        beskrivelse="Utøvende kunstnere og underholdsningsvirksomhet innen scenekunst",
    )
    assert org.antall_ansatte is None
    assert org.har_registrert_antall_ansatte is False
    assert org.overordnet_enhet == "443322119"
    assert org.beliggenhetsadresse == enhetsregisteret.Adresse(
        land="Norge",
        landkode="NO",
        postnummer="2120",
        poststed="NORD-ODAL",
        adresse=["Sagstua", None, None],
        kommune="NORD-ODAL",
        kommunenummer="0418",
    )
    assert org.slettedato is None


def test_search_underenhet_with_empty_response(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(  # pyright: ignore[reportUnknownMemberType]
        method="GET",
        url=(
            "https://data.brreg.no/enhetsregisteret/api/underenheter" "?navn=jibberish"
        ),
        status_code=200,
        headers={"content-type": "application/json"},
        content=(DATA_DIR / "underenheter-search-empty-response.json").read_bytes(),
    )

    page = enhetsregisteret.Client().search_underenhet(
        enhetsregisteret.UnderenhetQuery(navn="jibberish")
    )

    assert page.page_size == 20
    assert page.page_number == 0
    assert page.total_elements == 0
    assert page.total_pages == 0

    assert page.items == []
