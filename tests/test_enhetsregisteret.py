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

    # TODO Test all other fields

    assert org.stiftelsesdato == date(2017, 10, 20)
    assert org.siste_innsendte_aarsregnskap is None


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
