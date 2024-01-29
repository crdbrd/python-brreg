from contextlib import contextmanager
from types import TracebackType
from typing import Any, Generator, List, Optional, Type

import httpx

from brreg import BrregError, BrregRestError
from brreg.enhetsregisteret._pagination import Cursor, EnhetPage, UnderenhetPage
from brreg.enhetsregisteret._queries import EnhetQuery, UnderenhetQuery
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

    def __enter__(self) -> "Client":
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]] = None,
        exc_value: Optional[BaseException] = None,
        traceback: Optional[TracebackType] = None,
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
        organisasjonsnummer = OrganisasjonsnummerValidator.validate_python(
            organisasjonsnummer
        )
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
        organisasjonsnummer = OrganisasjonsnummerValidator.validate_python(
            organisasjonsnummer
        )
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
        organisasjonsnummer = OrganisasjonsnummerValidator.validate_python(
            organisasjonsnummer
        )
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
    ) -> Cursor[Enhet, EnhetQuery]:
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
            page = EnhetPage.model_validate_json(res.content)
            return Cursor(self.search_enhet, query, page)

    def search_underenhet(
        self,
        query: UnderenhetQuery,
    ) -> Cursor[Underenhet, UnderenhetQuery]:
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
            page = UnderenhetPage.model_validate_json(res.content)
            return Cursor(self.search_underenhet, query, page)


@contextmanager
def error_handler() -> Generator[None, Any, None]:
    try:
        yield
    except httpx.HTTPError as exc:
        response: Optional[httpx.Response] = getattr(exc, "response", None)
        raise BrregRestError(
            str(exc),
            method=(exc.request.method if exc.request else None),
            url=(str(exc.request.url) if exc.request else None),
            status_code=(response.status_code if response else None),
        ) from exc
    except Exception as exc:
        raise BrregError(exc) from exc
