"""API client for Brønnøysundregistrene's open API."""

from importlib.metadata import (  # pyright: ignore[reportMissingImports]
    PackageNotFoundError,  # pyright: ignore[reportUnknownVariableType]
    version,  # pyright: ignore[reportUnknownVariableType]
)

from brreg._exceptions import BrregError, BrregRestError

__all__ = [
    # From _exceptions module:
    "BrregError",
    "BrregRestError",
]

try:
    __version__: str = version(__name__)  # pyright: ignore[reportUnknownVariableType]
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
