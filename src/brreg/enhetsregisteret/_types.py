import datetime as dt
from typing import List, Optional, TypeVar

from pydantic import (
    BeforeValidator,
    Field,
    PlainSerializer,
    TypeAdapter,
)
from typing_extensions import Annotated

T = TypeVar("T")

# A list that serializes to a comma-separated string.
CommaList = Annotated[
    List[T],
    PlainSerializer(
        lambda v: ",".join(v),
        return_type=str,
        when_used="json",
    ),
]

# Same as `Optional[dt.date]`, except that this version deserializes empty
# strings to `None`.
DateOrNone = Annotated[
    Optional[dt.date], BeforeValidator(lambda v: v if v != "" else None)
]

Kommunenummer = Annotated[
    str,
    Field(min_length=4, max_length=4, pattern=r"^\d{4}$"),
]
KommunenummerValidator = TypeAdapter(Kommunenummer)

Naeringskode = Annotated[
    str,
    Field(min_length=6, max_length=6, pattern=r"^\d{2}\.\d{3}$"),
]
NaeringskodeValidator = TypeAdapter(Naeringskode)

Organisasjonsnummer = Annotated[
    str,
    BeforeValidator(lambda v: v.replace(" ", "")),
    Field(min_length=9, max_length=9, pattern=r"^\d{9}$"),
]
OrganisasjonsnummerValidator = TypeAdapter(Organisasjonsnummer)

Postnummer = Annotated[
    str,
    Field(min_length=4, max_length=4, pattern=r"^\d{4}$"),
]
PostnummerValidator = TypeAdapter(Postnummer)

Sektorkode = Annotated[
    str,
    Field(min_length=4, max_length=4, pattern=r"^\d{4}$"),
]
SektorkodeValidator = TypeAdapter(Sektorkode)
