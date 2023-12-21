from datetime import date
from pathlib import Path

from pytest_httpx import HTTPXMock

from brreg import enhetsregisteret

DATA_DIR = Path(__file__).parent.parent / "data"


def test_get_roller_with_person(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(  # pyright: ignore[reportUnknownMemberType]
        method="GET",
        url="https://data.brreg.no/enhetsregisteret/api/enheter/810004622/roller",
        status_code=200,
        headers={"content-type": "application/json"},
        content=(DATA_DIR / "enheter-roller-person-response.json").read_bytes(),
    )

    rollegrupper = enhetsregisteret.Client().get_roller("810004622")

    assert rollegrupper

    styret = rollegrupper[0]
    assert styret.type.kode == "STYR"
    assert styret.type.beskrivelse == "Styre"
    assert styret.sist_endret == date(2019, 1, 1)
    assert styret.roller

    rolle = styret.roller[0]
    assert rolle.type.kode == "LEDE"
    assert rolle.type.beskrivelse == "Styrets leder"
    assert rolle.person
    assert rolle.person.fodselsdato == date(1981, 1, 1)
    assert rolle.person.navn.fornavn == "Ove"
    assert rolle.person.navn.etternavn == "Olsen"
    assert rolle.person.er_doed is False
    assert rolle.valgt_av
    assert rolle.valgt_av.kode == "A-AK"
    assert rolle.valgt_av.beskrivelse == "Representant for A-aksjonærene"
    assert rolle.fratraadt is False
    assert rolle.rekkefolge == 0


def test_get_roller_with_enhet(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(  # pyright: ignore[reportUnknownMemberType]
        method="GET",
        url="https://data.brreg.no/enhetsregisteret/api/enheter/810004622/roller",
        status_code=200,
        headers={"content-type": "application/json"},
        content=(DATA_DIR / "enheter-roller-enhet-response.json").read_bytes(),
    )

    rollegrupper = enhetsregisteret.Client().get_roller("810004622")

    assert rollegrupper

    deltakere = rollegrupper[0]
    assert deltakere.type.kode == "DELT"
    assert deltakere.type.beskrivelse == "Deltakere"
    assert deltakere.sist_endret == date(2021, 2, 1)

    rolle = deltakere.roller[0]
    assert rolle.type.kode == "DTPR"
    assert rolle.type.beskrivelse == "Deltaker med delt ansvar"
    assert rolle.enhet
    assert rolle.enhet.organisasjonsnummer == "810006242"
    assert rolle.enhet.organisasjonsform.kode == "AS"
    assert rolle.enhet.organisasjonsform.beskrivelse == "Aksjeselskap"
    assert rolle.enhet.navn == ["Rolfsens Deltakerorganisasjon AS"]
    assert rolle.enhet.er_slettet is False
    assert rolle.ansvarsandel == "50%"
    assert rolle.fratraadt is False
    assert rolle.rekkefolge == 0

    rolle = deltakere.roller[1]
    assert rolle.type.kode == "DTPR"
    assert rolle.type.beskrivelse == "Deltaker med delt ansvar"
    assert rolle.enhet
    assert rolle.enhet.organisasjonsnummer == "810004282"
    assert rolle.enhet.organisasjonsform.kode == "AS"
    assert rolle.enhet.organisasjonsform.beskrivelse == "Aksjeselskap"
    assert rolle.enhet.navn == ["Sult AS"]
    assert rolle.enhet.er_slettet is False
    assert rolle.ansvarsandel == "50%"
    assert rolle.fratraadt is False
    assert rolle.rekkefolge == 1
