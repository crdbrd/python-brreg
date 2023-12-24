from datetime import date
from pathlib import Path

from pytest_httpx import HTTPXMock

from brreg import enhetsregisteret

DATA_DIR = Path(__file__).parent.parent / "data"


def test_enhet_query() -> None:
    query = enhetsregisteret.EnhetQuery(
        navn="Sesam",
        konkurs=False,
        fra_registreringsdato_enhetsregisteret=date(2017, 10, 20),
        til_registreringsdato_enhetsregisteret=date(2017, 10, 20),
    )

    assert query.navn == "Sesam"
    assert query.konkurs is False
    assert query.fra_registreringsdato_enhetsregisteret == date(2017, 10, 20)
    assert query.til_registreringsdato_enhetsregisteret == date(2017, 10, 20)

    assert query.as_url_query() == (
        "navn=Sesam"
        "&konkurs=false"
        "&fraRegistreringsdatoEnhetsregisteret=2017-10-20"
        "&tilRegistreringsdatoEnhetsregisteret=2017-10-20"
    )


def test_search_enhet(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(  # pyright: ignore[reportUnknownMemberType]
        method="GET",
        url=(
            "https://data.brreg.no/enhetsregisteret/api/enheter"
            "?navn=Sesam"
            "&konkurs=false"
            "&fraRegistreringsdatoEnhetsregisteret=2017-10-20"
            "&tilRegistreringsdatoEnhetsregisteret=2017-10-20"
        ),
        status_code=200,
        headers={"content-type": "application/json"},
        content=(DATA_DIR / "enheter-search-response.json").read_bytes(),
    )

    page = enhetsregisteret.Client().search_enhet(
        enhetsregisteret.EnhetQuery(
            navn="Sesam",
            fra_registreringsdato_enhetsregisteret=date(2017, 10, 20),
            til_registreringsdato_enhetsregisteret=date(2017, 10, 20),
            konkurs=False,
        )
    )

    assert page.page_size == 1
    assert page.page_number == 0
    assert page.total_elements == 1
    assert page.total_pages == 1

    org = page.items[0]

    assert org is not None
    assert org.organisasjonsnummer == "112233445"
    assert org.navn == "SESAM STASJON"
    assert org.hjemmeside is None
    assert org.registreringsdato_enhetsregisteret == date(2017, 10, 20)
    assert org.registrert_i_mvaregisteret is True
    assert org.naeringskode1 == enhetsregisteret.Naering(
        kode="52.292", beskrivelse="Skipsmegling"
    )
    assert org.antall_ansatte == 50
    assert org.har_registrert_antall_ansatte is None
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


def test_search_enhet_with_empty_response(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(  # pyright: ignore[reportUnknownMemberType]
        method="GET",
        url=("https://data.brreg.no/enhetsregisteret/api/enheter" "?navn=jibberish"),
        status_code=200,
        headers={"content-type": "application/json"},
        content=(DATA_DIR / "enheter-search-empty-response.json").read_bytes(),
    )

    page = enhetsregisteret.Client().search_enhet(
        enhetsregisteret.EnhetQuery(navn="jibberish")
    )

    assert page.page_size == 20
    assert page.page_number == 0
    assert page.total_elements == 0
    assert page.total_pages == 0
    assert page.items == []
