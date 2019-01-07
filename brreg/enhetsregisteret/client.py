from typing import Optional

import requests

from brreg import BrregException, BrregRestException
from brreg.enhetsregisteret import Organisasjon


__all__ = ['get_organization_by_number']


BASE_URL = 'https://data.brreg.no/enhetsregisteret/api'


def get_organization_by_number(
    organization_number: str
) -> Optional[Organisasjon]:
    """Get :class:`Organisasjon` given an organization number.

    TODO: Document error cases.
    """

    try:
        res = requests.get(f'{BASE_URL}/enheter/{organization_number}')

        if res.status_code in (404, 410):
            return None

        res.raise_for_status()

        return Organisasjon.from_json(res.json())
    except requests.RequestException as exc:
        raise BrregRestException(exc)
    except Exception as exc:
        raise BrregException(exc)
