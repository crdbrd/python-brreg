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

    cursor = enhetsregisteret.Client().search_enhet(
        enhetsregisteret.EnhetQuery(
            navn="Sesam",
            fra_registreringsdato_enhetsregisteret=date(2017, 10, 20),
            til_registreringsdato_enhetsregisteret=date(2017, 10, 20),
            konkurs=False,
        )
    )
    page = next(cursor.pages)

    assert page.page_size == 1
    assert page.page_number == 0
    assert page.total_elements == 1
    assert page.total_pages == 1

    assert next(cursor.items) == page.items[0]

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

    cursor = enhetsregisteret.Client().search_enhet(
        enhetsregisteret.EnhetQuery(navn="jibberish")
    )

    assert list(cursor.page_numbers) == [0]
    assert len(list(cursor.pages)) == 1
    assert list(cursor.items) == []

    page = next(cursor.pages)
    assert page.page_size == 20
    assert page.page_number == 0
    assert page.total_elements == 0
    assert page.total_pages == 0
    assert page.items == []


def test_search_enhet_with_pagination(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(  # pyright: ignore[reportUnknownMemberType]
        method="GET",
        url="https://data.brreg.no/enhetsregisteret/api/enheter?navn=Sesam&size=2",
        status_code=200,
        headers={"content-type": "application/json"},
        content=(DATA_DIR / "enheter-search-page1-response.json").read_bytes(),
    )
    httpx_mock.add_response(  # pyright: ignore[reportUnknownMemberType]
        method="GET",
        url="https://data.brreg.no/enhetsregisteret/api/enheter?navn=Sesam&page=1&size=2",
        status_code=200,
        headers={"content-type": "application/json"},
        content=(DATA_DIR / "enheter-search-page2-response.json").read_bytes(),
    )

    cursor = enhetsregisteret.Client().search_enhet(
        enhetsregisteret.EnhetQuery(
            navn="Sesam",
            size=2,
        )
    )

    assert len(httpx_mock.get_requests()) == 1  # pyright: ignore[reportUnknownMemberType]

    assert list(cursor.page_numbers) == [0, 1]

    # Fetching the same page again should not trigger any HTTP requests:
    page0 = cursor.get_page(0)
    assert page0 is not None
    assert page0.page_number == 0
    assert [org.navn for org in page0.items] == [
        "SESAM AS",
        "SESAM FAMILIEBARNEHAGE",
    ]
    assert len(httpx_mock.get_requests()) == 1  # pyright: ignore[reportUnknownMemberType]

    # Fetching a new page should trigger an HTTP request:
    page1 = cursor.get_page(1)
    assert page1 is not None
    assert page1.page_number == 1
    assert [org.navn for org in page1.items] == [
        "SESAM FILMKLUBB",
    ]
    assert len(httpx_mock.get_requests()) == 2  # pyright: ignore[reportUnknownMemberType]

    # Iterating over the pages returns all pages:
    assert list(cursor.pages) == [page0, page1]

    # Iterating over the items returns items from all pages:
    assert [org.navn for org in cursor.items] == [
        "SESAM AS",
        "SESAM FAMILIEBARNEHAGE",
        "SESAM FILMKLUBB",
    ]
    # This does not trigger any HTTP requests as we already have all the pages:
    assert len(httpx_mock.get_requests()) == 2  # pyright: ignore[reportUnknownMemberType]

    # Iterating over the items again works:
    assert [org.navn for org in cursor.items] == [
        "SESAM AS",
        "SESAM FAMILIEBARNEHAGE",
        "SESAM FILMKLUBB",
    ]
