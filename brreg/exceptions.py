__all__ = ['BrregException', 'BrregRestException']


class BrregException(Exception):
    """Top-level exception.

    All exceptions raised by the :mod:`brreg` library are subclasses of this
    exception.
    """

    pass


class BrregRestException(BrregException):
    """REST API exception."""

    # TODO Expose HTTP status code, etc.

    pass
