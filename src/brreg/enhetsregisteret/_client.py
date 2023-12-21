from __future__ import annotations

from contextlib import contextmanager
from typing import TYPE_CHECKING, Any, Generator, List, Optional

import httpx

from brreg import BrregError, BrregRestError
from brreg.enhetsregisteret._pagination import EnhetPage, UnderenhetPage
from brreg.enhetsregisteret._responses import (
    Enhet,
    RolleGruppe,
    RollerResponse,
    Underenhet,
)
from brreg.enhetsregisteret._types import (
    Organisasjonsnummer,
    OrganisasjonsnummerValidator,
)

if TYPE_CHECKING:
    from types import TracebackType

    from brreg.enhetsregisteret._queries import EnhetQuery, UnderenhetQuery


class Client:
    """Client for the Enhetregisteret API.

    Ensures that HTTP connections are reused across requests.

    It can be used as a context manager::

        with Client() as client:
            enhet = client.get_enhet("915501680")

    Or by manually opening and closing the client::

        client = Client()
        enhet = client.get_enhet("915501680")
        client.close()
    """

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
        """Prepare the client for use.

        This is called automatically when the client is created.
        """
        self._client = httpx.Client(
            base_url="https://data.brreg.no/enhetsregisteret/api",
        )

    def close(self) -> None:
        """Close the client and any open HTTP connections.

        This is called automatically if the client is used as a context manager.
        """
        self._client.close()

    def get_enhet(
        self,
        organisasjonsnummer: Organisasjonsnummer,
    ) -> Optional[Enhet]:
        """Get :class:`Enhet` given an organization number."""
        OrganisasjonsnummerValidator.validate_python(organisasjonsnummer)
        with error_handler():
            res = self._client.get(
                f"/enheter/{organisasjonsnummer}",
                headers={
                    "accept": (
                        "application/vnd.brreg.enhetsregisteret.enhet.v2+json;"
                        "charset=UTF-8"
                    )
                },
            )
            if res.status_code in (404, 410):
                return None
            res.raise_for_status()
            return Enhet.model_validate_json(res.content)

    def get_underenhet(
        self,
        organisasjonsnummer: Organisasjonsnummer,
    ) -> Optional[Underenhet]:
        """Get :class:`Underenhet` given an organization number."""
        OrganisasjonsnummerValidator.validate_python(organisasjonsnummer)
        with error_handler():
            res = self._client.get(
                f"/underenheter/{organisasjonsnummer}",
                headers={
                    "accept": (
                        "application/vnd.brreg.enhetsregisteret.underenhet.v2+json;"
                        "charset=UTF-8"
                    )
                },
            )
            if res.status_code in (404, 410):
                return None
            res.raise_for_status()
            return Underenhet.model_validate_json(res.content)

    def get_roller(
        self,
        organisasjonsnummer: Organisasjonsnummer,
    ) -> List[RolleGruppe]:
        """Get :class:`Enhet` given an organization number."""
        OrganisasjonsnummerValidator.validate_python(organisasjonsnummer)
        with error_handler():
            res = self._client.get(
                f"/enheter/{organisasjonsnummer}/roller",
                headers={"accept": "application/json"},
            )
            if res.status_code in (404, 410):
                return []
            res.raise_for_status()
            roller_response = RollerResponse.model_validate_json(res.content)
            return roller_response.rollegrupper

    def search_enhet(
        self,
        query: EnhetQuery,
    ) -> EnhetPage:
        """Search for :class:`Enhet` that matches the given query.

        :param query: The search query.
        """
        with error_handler():
            res = self._client.get(
                f"/enheter?{query.as_url_query()}",
                headers={
                    "accept": (
                        "application/vnd.brreg.enhetsregisteret.enhet.v2+json;"
                        "charset=UTF-8"
                    )
                },
            )
            res.raise_for_status()
            return EnhetPage.model_validate_json(res.content)

    def search_underenhet(
        self,
        query: UnderenhetQuery,
    ) -> UnderenhetPage:
        """Search for :class:`Underenhet` that matches the given query.

        :param query: The search query.
        """
        with error_handler():
            res = self._client.get(
                f"/underenheter?{query.as_url_query()}",
                headers={
                    "accept": (
                        "application/vnd.brreg.enhetsregisteret.underenhet.v2+json;"
                        "charset=UTF-8"
                    )
                },
            )
            res.raise_for_status()
            return UnderenhetPage.model_validate_json(res.content)


@contextmanager
def error_handler() -> Generator[None, Any, None]:
    try:
        yield
    except httpx.HTTPError as exc:
        response: httpx.Response | None = getattr(exc, "response", None)
        raise BrregRestError(
            str(exc),
            method=(exc.request.method if exc.request else None),
            url=(str(exc.request.url) if exc.request else None),
            status_code=(response.status_code if response else None),
        ) from exc
    except Exception as exc:
        raise BrregError(exc) from exc
