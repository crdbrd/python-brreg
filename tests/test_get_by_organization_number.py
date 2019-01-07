import pytest

import responses

from brreg.client import Client
from brreg.exceptions import BrregRestException


@responses.activate
def test_get_by_organization_number(organization_details_response):
    responses.add(
        responses.GET,
        'https://data.brreg.no/enhetsregisteret/api/enheter/818511752',
        body=organization_details_response,
        status=200,
        content_type='application/json',
    )

    org = Client.get_by_organization_number('818511752')

    assert org.organisasjonsnummer == '818511752'


@responses.activate
def test_get_by_organization_number_deleted_organization(
    deleted_organization_details_response
):
    responses.add(
        responses.GET,
        'https://data.brreg.no/enhetsregisteret/api/enheter/815597222',
        body=deleted_organization_details_response,
        status=200,
        content_type='application/json',
    )

    org = Client.get_by_organization_number('815597222')

    assert org.organisasjonsnummer == '815597222'


@responses.activate
def test_get_by_organization_number_gone_organization():
    responses.add(
        responses.GET,
        'https://data.brreg.no/enhetsregisteret/api/enheter/818511752',
        status=410,
        content_type='application/json',
    )

    org = Client.get_by_organization_number('818511752')

    assert org is None


@responses.activate
def test_get_by_organization_returns_none_if_not_found():
    responses.add(
        responses.GET,
        'https://data.brreg.no/enhetsregisteret/api/enheter/818511752',
        status=404,
        content_type='application/json',
    )

    org = Client.get_by_organization_number('818511752')

    assert org is None


@responses.activate
def test_get_by_organization_raises_exception_if_http_error():
    responses.add(
        responses.GET,
        'https://data.brreg.no/enhetsregisteret/api/enheter/818511752',
        status=400,
        content_type='application/json',
    )

    with pytest.raises(BrregRestException) as exc:
        Client.get_by_organization_number('818511752')

    assert 'Bad Request' in str(exc.value)


@responses.activate
def test_get_by_organization_raises_exception_if_http_timeout():
    with pytest.raises(BrregRestException) as exc:
        Client.get_by_organization_number('818511752')

    assert 'Connection refused' in str(exc.value)
