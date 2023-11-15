from __future__ import annotations

from typing import TYPE_CHECKING, Optional

import httpx

from brreg import BrregError, BrregRestError
from brreg.enhetsregisteret._types import Enhet

if TYPE_CHECKING:
    from types import TracebackType


class Client:
    _client: httpx.Client

    def __init__(self) -> None:
        self.open()

    def __enter__(self) -> Client:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: TracebackType | None = None,
    ) -> None:
        self.close()

    def open(self) -> None:
        self._client = httpx.Client(
            base_url="https://data.brreg.no/enhetsregisteret/api",
        )

    def close(self) -> None:
        self._client.close()

    def get_enhet(self, organisasjonsnummer: str) -> Optional[Enhet]:
        """Get :class:`Enhet` given an organization number.

        Returns :class:`None` if Enhet is gone or not found.
        Returns :class:`Enhet` if Enhet is found.

        Raises :class:`BrregRestError` if a REST error occurs.
        Raises :class:`BrregError` if an unhandled exception occurs.
        """
        res: Optional[httpx.Response] = None
        try:
            res = self._client.get(f"/enheter/{organisasjonsnummer}")
            if res.status_code in (404, 410):
                return None
            res.raise_for_status()
            return Enhet.from_json(res.json())
        except httpx.HTTPError as exc:
            raise BrregRestError(
                str(exc),
                method=(exc.request.method if exc.request else None),
                url=(str(exc.request.url) if exc.request else None),
                status_code=(res.status_code if res else None),
            ) from exc
        except Exception as exc:
            raise BrregError(exc) from exc
