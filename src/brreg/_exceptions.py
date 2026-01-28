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
        method: str | None,
        url: str | None,
        status_code: int | None,
    ) -> None:
        super().__init__(f"REST API exception: {msg}")
        self.method = method
        self.url = url
        self.status_code = status_code
