"""API client for `Enhetsregisteret <https://w2.brreg.no/enhet/sok/>`_.

See https://data.brreg.no/enhetsregisteret/api/docs/index.html for API details.
"""

from brreg.enhetsregisteret._client import Client
from brreg.enhetsregisteret._types import (
    Adresse,
    Enhet,
    InstitusjonellSektorkode,
    Naeringskode,
    Organisasjonsform,
    Underenhet,
)

__all__ = [
    # From _client module:
    "Client",
    # From _types module:
    "Adresse",
    "Enhet",
    "InstitusjonellSektorkode",
    "Naeringskode",
    "Organisasjonsform",
    "Underenhet",
]
