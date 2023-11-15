"""API client for `Enhetsregisteret <https://w2.brreg.no/enhet/sok/>`_.

See https://data.brreg.no/enhetsregisteret/api/docs/index.html for API details.
"""

from brreg.enhetsregisteret.client import *  # noqa: F403, I001
from brreg.enhetsregisteret.types import *  # noqa: F403

# Must come after reexport imports
from brreg.enhetsregisteret import (
    client,
    types,
)

__all__ = client.__all__ + types.__all__
