from typing import Optional

import requests

from brreg import BrregException, BrregRestException
from brreg.enhetsregisteret.types import Enhet


__all__ = ['get_enhet']


BASE_URL = 'https://data.brreg.no/enhetsregisteret/api'


def get_enhet(organisasjonsnummer: str) -> Optional[Enhet]:
    """Get :class:`Enhet` given an organization number.

    TODO: Document error cases.
    """

    try:
        res = requests.get(f'{BASE_URL}/enheter/{organisasjonsnummer}')

        if res.status_code in (404, 410):
            return None

        res.raise_for_status()

        return Enhet.from_json(res.json())
    except requests.RequestException as exc:
        raise BrregRestException(
            exc,
            method=exc.request.method,
            url=exc.request.url,
            status=getattr(exc.response, 'status_code', None),
        ) from exc
    except Exception as exc:
        raise BrregException(exc)
