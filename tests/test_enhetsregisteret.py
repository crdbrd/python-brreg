from datetime import date

import pytest

import responses

from brreg import BrregRestException
from brreg import enhetsregisteret


@responses.activate
def test_get_enhet(organization_details_response):
    responses.add(
        responses.GET,
        'https://data.brreg.no/enhetsregisteret/api/enheter/818511752',
        body=organization_details_response,
        status=200,
        content_type='application/json',
    )

    org = enhetsregisteret.get_enhet('818511752')

    assert org.organisasjonsnummer == '818511752'
    assert org.navn == 'SESAM STASJON'
    assert org.hjemmeside is None
    assert org.registreringsdato_enhetsregisteret == date(2017, 10, 20)
    assert org.registrert_i_mvaregisteret is True
    assert org.naeringskode1 == enhetsregisteret.Naeringskode(
        kode='52.292', beskrivelse='Skipsmegling'
    )
    assert org.antall_ansatte == 50
    assert org.forretningsadresse == enhetsregisteret.Adresse(
        land='Norge',
        landkode='NO',
        postnummer='0101',
        poststed='OSLO',
        adresse=['Tyvholmen 1', None, None, ''],
        kommune='OSLO',
        kommunenummer='0301',
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
    assert org.maalform == 'Bokmål'
    assert org.slettedato is None


@responses.activate
def test_get_enhet_when_deleted(deleted_organization_details_response):
    responses.add(
        responses.GET,
        'https://data.brreg.no/enhetsregisteret/api/enheter/815597222',
        body=deleted_organization_details_response,
        status=200,
        content_type='application/json',
    )

    org = enhetsregisteret.get_enhet('815597222')

    assert org.organisasjonsnummer == '815597222'
    assert org.navn == 'SLETTET ENHET AS'
    assert org.organisasjonsform == enhetsregisteret.Organisasjonsform(
        kode='UTBG', beskrivelse='Frivillig registrert utleiebygg'
    )
    assert org.slettedato == date(2017, 10, 20)


@responses.activate
def test_get_enhet_when_gone():
    responses.add(
        responses.GET,
        'https://data.brreg.no/enhetsregisteret/api/enheter/818511752',
        status=410,
        content_type='application/json',
    )

    org = enhetsregisteret.get_enhet('818511752')

    assert org is None


@responses.activate
def test_get_enhet_when_not_found():
    responses.add(
        responses.GET,
        'https://data.brreg.no/enhetsregisteret/api/enheter/818511752',
        status=404,
        content_type='application/json',
    )

    org = enhetsregisteret.get_enhet('818511752')

    assert org is None


@responses.activate
def test_get_enhet_when_http_error():
    responses.add(
        responses.GET,
        'https://data.brreg.no/enhetsregisteret/api/enheter/818511752',
        status=400,
        content_type='application/json',
    )

    with pytest.raises(BrregRestException) as exc_info:
        enhetsregisteret.get_enhet('818511752')

    assert 'REST API exception' in str(exc_info.value)
    assert 'Bad Request' in str(exc_info.value)

    assert exc_info.value.method == 'GET'
    assert (
        exc_info.value.url
        == 'https://data.brreg.no/enhetsregisteret/api/enheter/818511752'
    )
    assert exc_info.value.status == 400


@responses.activate
def test_get_organization_by_number_when_http_timeout():
    with pytest.raises(BrregRestException) as exc_info:
        enhetsregisteret.get_enhet('818511752')

    assert 'REST API exception' in str(exc_info.value)
    assert 'Connection refused' in str(exc_info.value)

    assert exc_info.value.method == 'GET'
    assert (
        exc_info.value.url
        == 'https://data.brreg.no/enhetsregisteret/api/enheter/818511752'
    )
    assert exc_info.value.status is None
