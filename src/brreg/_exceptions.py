from typing import Optional


class BrregError(Exception):
    """Top-level exception.

    All exceptions raised by the :mod:`brreg` library are subclasses of this
    exception.
    """


class BrregRestError(BrregError):
    """REST API exception."""

    def __init__(
        self,
        msg: str,
        *,
        method: Optional[str],
        url: Optional[str],
        status_code: Optional[int],
    ) -> None:
        super().__init__(f"REST API exception: {msg}")
        self.method = method
        self.url = url
        self.status_code = status_code
