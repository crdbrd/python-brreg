from typing import (
    Callable,
    Dict,
    Generic,
    Iterator,
    List,
    Optional,
    TypeVar,
)

from pydantic import (
    AliasPath,
    BaseModel,
    Field,
)

from brreg.enhetsregisteret._queries import Query
from brreg.enhetsregisteret._responses import Enhet, Underenhet

__all__ = [
    "EnhetPage",
    "UnderenhetPage",
]


T = TypeVar("T", bound=BaseModel)
Q = TypeVar("Q", bound=Query)


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


class Cursor(Generic[T, Q]):
    """Cursor for iterating over multiple pages of items."""

    _operation: Callable[[Q], "Cursor[T, Q]"]
    _query: Q
    _pages: Dict[int, Page[T]]
    _current_page_number: int

    #: Iterate over all page numbers in this cursor.
    page_numbers: range

    def __init__(
        self,
        operation: Callable[[Q], "Cursor[T, Q]"],
        query: Q,
        page: Page[T],
    ) -> None:
        self._operation = operation
        self._query = query
        self._pages = {page.page_number: page}
        # Expose the empty first page, even if it says the totalt number of pages is 0.
        self.page_numbers = range(max(1, page.total_pages))

    def get_page(self, page_number: int) -> Optional[Page[T]]:
        """Get a page by its 0-indexed page number."""
        if page_number not in self.page_numbers:
            return None

        if page_number not in self._pages:
            # We need to fetch the page.
            new_cursor = self._operation(
                self._query.model_copy(update={"page": page_number})
            )
            new_page = new_cursor.get_page(page_number)
            assert new_page is not None
            self._pages[page_number] = new_page

        return self._pages[page_number]

    @property
    def pages(self) -> Iterator[Page[T]]:
        """Iterator over all pages in this cursor."""
        for page_number in self.page_numbers:
            page = self.get_page(page_number)
            assert page is not None
            yield page

    @property
    def items(self) -> Iterator[T]:
        """Iterator over all items in this cursor."""
        for page in self.pages:
            yield from page.items


class EnhetPage(Page[Enhet]):
    """Response type for enhet search."""

    items: List[Enhet] = Field(
        default_factory=list,
        validation_alias=AliasPath("_embedded", "enheter"),
    )


class UnderenhetPage(Page[Underenhet]):
    """Response type for underenhet search."""

    items: List[Underenhet] = Field(
        default_factory=list,
        validation_alias=AliasPath("_embedded", "underenheter"),
    )
