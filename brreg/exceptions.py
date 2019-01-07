__all__ = ['BrregException', 'BrregRestException']


class BrregException(Exception):
    """Top-level exception.

    All exceptions raised by the :mod:`brreg` library are subclasses of this
    exception.
    """

    pass


class BrregRestException(BrregException):
    """REST API exception."""

    def __init__(self, msg, *, method, url, status):
        super().__init__(f'REST API exception: {msg}')
        self.method = method
        self.url = url
        self.status = status
