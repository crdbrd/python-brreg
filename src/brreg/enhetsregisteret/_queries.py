import datetime as dt
from typing import Literal
from urllib.parse import urlencode

from pydantic import BaseModel, Field, NonNegativeInt, PositiveInt

from brreg.enhetsregisteret._types import (
    CommaList,
    Kommunenummer,
    Naeringskode,
    Organisasjonsnummer,
    Postnummer,
    Sektorkode,
)

__all__ = [
    "EnhetQuery",
    "UnderenhetQuery",
]


class Query(BaseModel):
    """The fields here are available on all queries."""

    #: Sortering av resultatsett
    sort: Literal["ASC", "DESC"] | None = None

    #: Sidestørrelse
    size: PositiveInt | None = None

    #: Sidenummer
    page: NonNegativeInt | None = None

    def as_url_query(self) -> str:
        params = self.model_dump(
            mode="json",
            by_alias=True,
            exclude_defaults=True,
        )
        for key, value in params.items():
            if isinstance(value, bool):
                params[key] = str(value).lower()
        return urlencode(params)


class EnhetQuery(Query):
    """The query type for enhet search."""

    #: Enhetens navn
    navn: str | None = None

    #: Organisasjonsnummeret til enheten
    organisasjonsnummer: CommaList[Organisasjonsnummer] = Field(
        default_factory=list,
    )

    #: Organisasjonsnummeret til enhetens overordnede enhet
    overordnet_enhet: Organisasjonsnummer | None = Field(
        default=None,
        serialization_alias="overordnetEnhet",
    )

    #: Minste antall ansatte hos enheten
    fra_antall_ansatte: PositiveInt | None = Field(
        default=None,
        serialization_alias="fraAntallAnsatte",
    )

    #: Største antall ansatte hos enheten
    til_antall_ansatte: PositiveInt | None = Field(
        default=None,
        serialization_alias="tilAntallAnsatte",
    )

    #: Hvorvidt enheten er registrert som konkurs
    konkurs: bool | None = None

    #: Hvorvidt enheten er registrert i Mva-registeret
    registrert_i_mvaregisteret: bool | None = Field(
        default=None,
        serialization_alias="registrertIMvaregisteret",
    )

    #: Hvorvidt enheten er registrert i Foretaksregisteret
    registrert_i_foretaksregisteret: bool | None = Field(
        default=None,
        serialization_alias="registrertIForetaksregisteret",
    )

    #: Hvorvidt enheten er registrert i Stiftelsesregisteret
    registrert_i_stiftelsesregisteret: bool | None = Field(
        default=None,
        serialization_alias="registrertIStiftelsesregisteret",
    )

    #: Hvorvidt enheten er registrert i Frivillighetsregisteret
    registrert_i_frivillighetsregisteret: bool | None = Field(
        default=None,
        serialization_alias="registrertIFrivillighetsregisteret",
    )

    #: Frivillig registrert i Merverdiavgiftsregisteret
    frivillig_registrert_i_mvaregisteret: CommaList[str] = Field(
        default_factory=list,
        serialization_alias="frivilligRegistrertIMvaregisteret",
    )

    #: Hvorvidt enheten er registrert som under tvangsavvikling eller
    #: tvangsoppløsning
    under_tvangsavvikling_eller_tvangsopplosning: bool | None = None

    #: Hvorvidt enheten er registrert som under avvikling
    under_avvikling: bool | None = None

    #: Tidligste registreringsdato i Enhetsregisteret
    fra_registreringsdato_enhetsregisteret: dt.date | None = Field(
        default=None,
        serialization_alias="fraRegistreringsdatoEnhetsregisteret",
    )

    #: Seneste registreringsdato i Enhetsregisteret
    til_registreringsdato_enhetsregisteret: dt.date | None = Field(
        default=None,
        serialization_alias="tilRegistreringsdatoEnhetsregisteret",
    )

    #: Tidligste stiftelsesdato for enheten
    fra_stiftelsesdato: dt.date | None = Field(
        default=None,
        serialization_alias="fraStiftelsesdato",
    )

    #: Seneste stiftelsesdato for enheten
    til_stiftelsesdato: dt.date | None = Field(
        default=None,
        serialization_alias="tilStiftelsesdato",
    )

    #: Enhetens organisasjonsform
    organisasjonsform: CommaList[str] = Field(
        default_factory=list,
    )

    #: Enhetens hjemmeside
    hjemmeside: str | None = None

    #: Enhetens institusjonelle sektorkode
    institusjonell_sektorkode: CommaList[Sektorkode] = Field(
        default_factory=list,
    )

    #: Kommunenummer til enhetens postadresse
    postadresse_kommunenummer: CommaList[Kommunenummer] = Field(
        default_factory=list,
        serialization_alias="postadresse.kommunenummer",
    )

    #: Postnummeret til enhetens postadresse
    postadresse_postnummer: CommaList[Postnummer] = Field(
        default_factory=list,
        serialization_alias="postadresse.postnummer",
    )

    #: Poststedet til enhetens postadresse
    postadresse_poststed: str | None = Field(
        default=None,
        serialization_alias="postadresse.poststed",
    )

    #: Landkode til enhetens postadresse
    postadresse_landkode: CommaList[str] = Field(
        default_factory=list,
        serialization_alias="postadresse.landkode",
    )

    #: Adresse til enhetens postadresse
    postadresse_adresse: str | None = Field(
        default=None,
        serialization_alias="postadresse.adresse",
    )

    #: Kommunenummer til enhetens forretningsadresse
    kommunenummer: CommaList[Kommunenummer] = Field(
        default_factory=list,
        serialization_alias="kommunenummer",
    )

    #: Postnummeret til enhetens forretningsadresse
    forretningsadresse_postnummer: CommaList[Postnummer] = Field(
        default_factory=list,
        serialization_alias="forretningsadresse.postnummer",
    )

    #: Poststedet til enhetens forretningsadresse
    forretningsadresse_poststed: str | None = Field(
        default=None,
        serialization_alias="forretningsadresse.poststed",
    )

    #: Landkode til enhetens forretningsadresse
    forretningsadresse_landkode: CommaList[str] = Field(
        default_factory=list,
        serialization_alias="forretningsadresse.landkode",
    )

    #: Adresse til enhetens forretningsadresse
    forretningsadresse_adresse: str | None = Field(
        default=None,
        serialization_alias="forretningsadresse.adresse",
    )

    #: Enhetens næringskode
    naeringskode: CommaList[Naeringskode] = Field(
        default_factory=list,
    )

    #: Årstall for siste innsendte årsregnskap for enheten
    siste_innsendte_aarsregnskap: CommaList[str] = Field(
        default_factory=list,
        serialization_alias="sisteInnsendteAarsregnskap",
    )


class UnderenhetQuery(Query):
    """The query type for underenhet search."""

    #: Underenhetens navn
    navn: str | None = None

    #: Organisasjonsnummeret til underenheten
    organisasjonsnummer: CommaList[Organisasjonsnummer] = Field(
        default_factory=list,
    )

    #: Organisasjonsnummeret til underenhetens overordnede enhet
    overordnet_enhet: Organisasjonsnummer | None = Field(
        default=None,
        serialization_alias="overordnetEnhet",
    )

    #: Minste antall ansatte hos underenheten
    fra_antall_ansatte: PositiveInt | None = Field(
        default=None,
        serialization_alias="fraAntallAnsatte",
    )

    #: Største antall ansatte hos underenheten
    til_antall_ansatte: PositiveInt | None = Field(
        default=None,
        serialization_alias="tilAntallAnsatte",
    )

    #: Hvorvidt underenheten er registrert i Mva-registeret
    registrert_i_mvaregisteret: bool | None = Field(
        default=None,
        serialization_alias="registrertIMvaregisteret",
    )

    #: Tidligste registreringsdato i Enhetsregisteret
    fra_registreringsdato_enhetsregisteret: dt.date | None = Field(
        default=None,
        serialization_alias="fraRegistreringsdatoEnhetsregisteret",
    )

    #: Seneste registreringsdato i Enhetsregisteret
    til_registreringsdato_enhetsregisteret: dt.date | None = Field(
        default=None,
        serialization_alias="tilRegistreringsdatoEnhetsregisteret",
    )

    #: Tidligste oppstartsdato for enheten
    fra_oppstartsdato: dt.date | None = Field(
        default=None,
        serialization_alias="fraOppstartsdato",
    )

    #: Seneste oppstartsdato for enheten
    til_oppstartsdato: dt.date | None = Field(
        default=None,
        serialization_alias="tilOppstartsdato",
    )

    #: Tidligste registreringsdato for eierskifte
    fra_dato_eierskifte: dt.date | None = Field(
        default=None,
        serialization_alias="fraDatoEierskifte",
    )

    #: Seneste registreringsdato for eierskifte
    til_dato_eierskifte: dt.date | None = Field(
        default=None,
        serialization_alias="tilDatoEierskifte",
    )

    #: Tidligste nedleggelsesdato for enheten
    fra_nedleggelsesdato: dt.date | None = Field(
        default=None,
        serialization_alias="fraNedleggelsesdato",
    )

    #: Seneste nedleggelsesdato for enheten
    til_nedleggelsesdato: dt.date | None = Field(
        default=None,
        serialization_alias="tilNedleggelsesdato",
    )

    #: Underenhetens organisasjonsform
    organisasjonsform: CommaList[str] = Field(
        default_factory=list,
    )

    #: Enhetens hjemmeside
    hjemmeside: str | None = None

    #: Kommunenummer til underenhetens postadresse
    postadresse_kommunenummer: CommaList[Kommunenummer] = Field(
        default_factory=list,
        serialization_alias="postadresse.kommunenummer",
    )

    #: Postnummeret til underenhetens postadresse
    postadresse_postnummer: CommaList[Postnummer] = Field(
        default_factory=list,
        serialization_alias="postadresse.postnummer",
    )

    #: Poststedet til underenhetens postadresse
    postadresse_poststed: str | None = Field(
        default=None,
        serialization_alias="postadresse.poststed",
    )

    #: Landkode til underenhetens postadresse
    postadresse_landkode: CommaList[str] = Field(
        default_factory=list,
        serialization_alias="postadresse.landkode",
    )

    #: Adresse til underenhetens postadresse
    postadresse_adresse: str | None = Field(
        default=None,
        serialization_alias="postadresse.adresse",
    )

    #: Kommunenummer til enhetens beliggenhetsadresse
    kommunenummer: CommaList[Kommunenummer] = Field(
        default_factory=list,
        serialization_alias="kommunenummer",
    )

    #: Postnummeret til enhetens beliggenhetsadresse
    beliggenhetsadresse_postnummer: CommaList[Postnummer] = Field(
        default_factory=list,
        serialization_alias="beliggenhetsadresse.postnummer",
    )

    #: Poststedet til enhetens beliggenhetsadresse
    beliggenhetsadresse_poststed: str | None = Field(
        default=None,
        serialization_alias="beliggenhetsadresse.poststed",
    )

    #: Landkode til enhetens beliggenhetsadresse
    beliggenhetsadresse_landkode: CommaList[str] = Field(
        default_factory=list,
        serialization_alias="beliggenhetsadresse.landkode",
    )

    #: Adresse til enhetens beliggenhetsadresse
    beliggenhetsadresse_adresse: str | None = Field(
        default=None,
        serialization_alias="beliggenhetsadresse.adresse",
    )

    #: Underenhetens næringskode
    naeringskode: CommaList[Naeringskode] = Field(
        default_factory=list,
    )
