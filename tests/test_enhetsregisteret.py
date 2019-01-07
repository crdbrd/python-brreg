from datetime import date

import pytest

import responses

from brreg import BrregRestException
from brreg import enhetsregisteret


@responses.activate
def test_get_organization_by_number(organization_details_response):
    responses.add(
        responses.GET,
        'https://data.brreg.no/enhetsregisteret/api/enheter/818511752',
        body=organization_details_response,
        status=200,
        content_type='application/json',
    )

    org = enhetsregisteret.get_organization_by_number('818511752')

    assert org.organisasjonsnummer == '818511752'

    # TODO Test all other fields

    assert org.stiftelsesdato == date(2017, 10, 20)
    assert org.siste_innsendte_aarsregnskap is None


@responses.activate
def test_get_organization_by_number_when_deleted(
    deleted_organization_details_response
):
    responses.add(
        responses.GET,
        'https://data.brreg.no/enhetsregisteret/api/enheter/815597222',
        body=deleted_organization_details_response,
        status=200,
        content_type='application/json',
    )

    org = enhetsregisteret.get_organization_by_number('815597222')

    assert org.organisasjonsnummer == '815597222'


@responses.activate
def test_get_organization_by_number_when_gone():
    responses.add(
        responses.GET,
        'https://data.brreg.no/enhetsregisteret/api/enheter/818511752',
        status=410,
        content_type='application/json',
    )

    org = enhetsregisteret.get_organization_by_number('818511752')

    assert org is None


@responses.activate
def test_get_organization_by_number_when_not_found():
    responses.add(
        responses.GET,
        'https://data.brreg.no/enhetsregisteret/api/enheter/818511752',
        status=404,
        content_type='application/json',
    )

    org = enhetsregisteret.get_organization_by_number('818511752')

    assert org is None


@responses.activate
def test_get_organization_by_number_when_http_error():
    responses.add(
        responses.GET,
        'https://data.brreg.no/enhetsregisteret/api/enheter/818511752',
        status=400,
        content_type='application/json',
    )

    with pytest.raises(BrregRestException) as exc:
        enhetsregisteret.get_organization_by_number('818511752')

    assert 'Bad Request' in str(exc.value)


@responses.activate
def test_get_organization_by_number_when_http_timeout():
    with pytest.raises(BrregRestException) as exc:
        enhetsregisteret.get_organization_by_number('818511752')

    assert 'Connection refused' in str(exc.value)
