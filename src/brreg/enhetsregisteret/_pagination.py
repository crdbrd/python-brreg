from typing import Generic, List, TypeVar

from pydantic import (
    AliasPath,
    BaseModel,
    Field,
)

from brreg.enhetsregisteret._responses import Enhet, Underenhet

__all__ = [
    "EnhetPage",
    "UnderenhetPage",
]


T = TypeVar("T", bound=BaseModel)


class Page(BaseModel, Generic[T]):
    """The fields here are available on all page objects."""

    #: The items on this page.
    items: List[T]

    #: The number of elements on this page.
    page_size: int = Field(
        validation_alias=AliasPath("page", "size"),
    )

    #: The page number, starting at 0.
    page_number: int = Field(
        validation_alias=AliasPath("page", "number"),
    )

    #: The total number of elements available.
    total_elements: int = Field(
        validation_alias=AliasPath("page", "totalElements"),
    )

    #: The total number of pages available.
    total_pages: int = Field(
        validation_alias=AliasPath("page", "totalPages"),
    )


class EnhetPage(Page[Enhet]):
    """Response type for enhet search."""

    items: List[Enhet] = Field(
        validation_alias=AliasPath("_embedded", "enheter"),
    )


class UnderenhetPage(Page[Underenhet]):
    """Response type for underenhet search."""

    items: List[Underenhet] = Field(
        validation_alias=AliasPath("_embedded", "underenheter"),
    )
