"""
API client for `Enhetsregisteret <https://w2.brreg.no/enhet/sok/>`_.

See https://data.brreg.no/enhetsregisteret/api/docs/index.html for API details.
"""


from brreg.enhetsregisteret.types import *  # noqa: Reexport
from brreg.enhetsregisteret.client import *  # noqa: Reexport


from brreg.enhetsregisteret import (  # noqa: Must come after reexport
    client,
    types,
)


__all__ = client.__all__ + types.__all__
