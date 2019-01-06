from typing import Optional

import requests

from brreg.exceptions import BrregException, BrregRestException
from brreg.types import Organisasjon


class Client:
    BASE_URL = 'https://data.brreg.no'

    @classmethod
    def get_by_organization_number(
        cls, organization_number: str
    ) -> Optional[Organisasjon]:
        url = f'{cls.BASE_URL}/enhetsregisteret/api/enheter/'

        try:
            res = requests.get(url + organization_number)

            if res.status_code in (404, 410):
                return None

            res.raise_for_status()

            return Organisasjon.from_json(res.json())
        except requests.RequestException as exc:
            raise BrregRestException(exc)
        except Exception as exc:
            raise BrregException(exc)
