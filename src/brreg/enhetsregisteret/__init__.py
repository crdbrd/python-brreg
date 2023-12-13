"""API client for `Enhetsregisteret <https://w2.brreg.no/enhet/sok/>`_.

See https://data.brreg.no/enhetsregisteret/api/docs/index.html for API details.
"""

from brreg.enhetsregisteret._client import Client
from brreg.enhetsregisteret._pagination import EnhetPage
from brreg.enhetsregisteret._queries import EnhetQuery
from brreg.enhetsregisteret._responses import (
    Adresse,
    Enhet,
    InstitusjonellSektor,
    Naering,
    Organisasjonsform,
    Underenhet,
)
from brreg.enhetsregisteret._types import (
    Kommunenummer,
    KommunenummerValidator,
    Organisasjonsnummer,
    OrganisasjonsnummerValidator,
    Postnummer,
    PostnummerValidator,
    Sektorkode,
    SektorkodeValidator,
)

__all__ = [
    # From _client module:
    "Client",
    # From _pagination module:
    "EnhetPage",
    # From _queries module:
    "EnhetQuery",
    # From _responses module:
    "Adresse",
    "Enhet",
    "InstitusjonellSektor",
    "Naering",
    "Organisasjonsform",
    "Underenhet",
    # From _types module:
    "Kommunenummer",
    "KommunenummerValidator",
    "Organisasjonsnummer",
    "OrganisasjonsnummerValidator",
    "Postnummer",
    "PostnummerValidator",
    "Sektorkode",
    "SektorkodeValidator",
]
