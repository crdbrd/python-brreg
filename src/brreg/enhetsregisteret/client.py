from typing import Optional

import requests

from brreg import BrregException, BrregRestException
from brreg.enhetsregisteret.types import Enhet


__all__ = ['get_enhet']


BASE_URL = 'https://data.brreg.no/enhetsregisteret/api'


def get_enhet(organisasjonsnummer: str) -> Optional[Enhet]:
    """Get :class:`Enhet` given an organization number.

    Returns :class:`None` if Enhet is gone or not found
    Returns :class:`Enhet` if Enhet is found

    Raises :class:`BrregRestException` if a REST exception occures
    Raises :class:`BrregException` if an unhandled exception occures
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
