import datetime as dt
from typing import List, Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)
from pydantic.alias_generators import to_camel

from brreg.enhetsregisteret._types import DateOrNone

__all__ = [
    "Adresse",
    "Enhet",
    "InstitusjonellSektor",
    "Naering",
    "Organisasjonsform",
]


class InstitusjonellSektor(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    #: Sektorkoden
    kode: Optional[str] = None

    #: Tekstlig beskrivelse av sektorkoden
    beskrivelse: Optional[str] = None


class Adresse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    #: Adresse
    adresse: List[Optional[str]] = Field(default_factory=list)

    #: Postnummer
    postnummer: Optional[str] = None

    #: Poststed
    poststed: Optional[str] = None

    #: Kommunenummer
    kommunenummer: Optional[str] = None

    #: Kommune
    kommune: Optional[str] = None

    #: Landkode
    landkode: Optional[str] = None

    #: Land
    land: Optional[str] = None


class Naering(BaseModel):
    """Næringskode.

    Næringskoden skal vise virksomhetens hovedaktivitet, og den skal primært
    dekke statistiske behov for Statistisk sentralbyrå (SSB).
    """

    model_config = ConfigDict(alias_generator=to_camel)

    #: Næringskoden
    kode: Optional[str] = None

    #: Tekstlig beskrivelse av næringskoden
    beskrivelse: Optional[str] = None


class Organisasjonsform(BaseModel):
    """Organisasjonsform er virksomhetens formelle organisering.

    Organisasjonsform gir retningslinjer overfor blant annet ansvarsforhold,
    skatt, revisjonsplikt, rettigheter og plikter.
    """

    model_config = ConfigDict(alias_generator=to_camel)

    #: Organisasjonsformen
    kode: str

    #: Tekstlig beskrivelse av organisasjonsformen
    beskrivelse: str

    #: Dato når organisasjonsformen evt. ble ugyldig
    utgaatt: DateOrNone = None


class Enhet(BaseModel):
    """Enhet på øverste nivå i registreringsstrukturen i Enhetsregisteret.

    Eksempelvis enkeltpersonforetak, foreninger, selskap, sameier og andre som
    er registrert i Enhetsregisteret. Identifiseres med organisasjonsnummer.
    """

    model_config = ConfigDict(alias_generator=to_camel)

    #: Organisasjonsnummer
    organisasjonsnummer: str

    #: Navn
    navn: str

    #: Organisasjonsform
    organisasjonsform: Organisasjonsform

    #: Hjemmeside
    hjemmeside: Optional[str] = None

    #: Enhetens postadresse
    postadresse: Optional[Adresse] = None

    #: Registreringsdato i Enhetsregisteret
    registreringsdato_enhetsregisteret: DateOrNone = None

    #: Hvorvidt enheten er registrert i MVA-registeret
    registrert_i_mvaregisteret: Optional[bool] = None

    #: Enheter som i utgangspunktet ikke er mva-pliktig, kan søke om frivillig
    #: registrering i Merverdiavgiftsregisteret
    frivillig_mva_registrert_beskrivelser: List[str] = Field(default_factory=list)

    #: Næringskode 1
    naeringskode1: Optional[Naering] = None

    #: Næringskode 2
    naeringskode2: Optional[Naering] = None

    #: Næringskode 3
    naeringskode3: Optional[Naering] = None

    #: Hjelpeenhetskode
    hjelpeenhetskode: Optional[Naering] = None

    #: Antall ansatte
    antall_ansatte: Optional[int] = None

    #: Angir om enheten har registrert ansatte
    har_registrert_antall_ansatte: Optional[bool] = None

    #: Organisasjonsnummeret til overordnet enhet i offentlig sektor
    overordnet_enhet: Optional[str] = None

    #: Forretningsadresse
    forretningsadresse: Optional[Adresse] = None

    #: Stiftelsesdato
    stiftelsesdato: DateOrNone = None

    #: Sektorkode
    institusjonell_sektorkode: Optional[InstitusjonellSektor] = None

    #: Hvorvidt enheten er registrert i Foretaksregisteret
    registrert_i_foretaksregisteret: Optional[bool] = None

    #: Hvorvidt enheten er registrert i Stiftelsesregisteret
    registrert_i_stiftelsesregisteret: Optional[bool] = None

    #: Hvorvidt enheten er registrert i Frivillighetsregisteret
    registrert_i_frivillighetsregisteret: Optional[bool] = None

    #: År for siste innsendte årsregnskap
    siste_innsendte_aarsregnskap: Optional[int] = None

    #: Hvorvidt enheten er konkurs
    konkurs: Optional[bool] = None

    #: Kjennelsesdato for konkursen
    konkursdato: DateOrNone = None

    #: Hvorvidt enheten er under avvikling
    under_avvikling: Optional[bool] = None

    #: Hvorvidt enheten er under tvangsavvikling eller tvangsoppløsning
    under_tvangsavvikling_eller_tvangsopplosning: Optional[bool] = None

    #: Målform
    maalform: Optional[str] = None

    #: Enhetens vedtektsdato
    vedtektsdato: DateOrNone = None

    #: Enhetens formål
    vedtektsfestet_formaal: List[str] = Field(default_factory=list)

    #: Enhetens aktivitet
    aktivitet: List[str] = Field(default_factory=list)

    #: Nedleggelsesdato for underenheten
    nedleggelsesdato: DateOrNone = None

    #: Dato under-/enheten ble slettet
    slettedato: DateOrNone = None


class Underenhet(BaseModel):
    """Enhet på laveste nivå i registreringsstrukturen i Enhetsregisteret.

    En underenhet kan ikke eksistere alene og har alltid knytning til en
    hovedenhet. Identifiseres med organisasjonsnummer.
    """

    model_config = ConfigDict(alias_generator=to_camel)

    #: Underenhetens organisasjonsnummer
    organisasjonsnummer: str

    #: Underenhetens navn
    navn: str

    #: Underenhetens organisasjonsform
    organisasjonsform: Organisasjonsform

    #: Underenhetens hjemmeside
    hjemmeside: Optional[str] = None

    #: Underenhetens postadresse
    postadresse: Optional[Adresse] = None

    #: Underenhetens registreringsdato i Enhetsregisteret
    registreringsdato_enhetsregisteret: DateOrNone = None

    #: Hvorvidt underenheten er registrert i MVA-registeret
    registrert_i_mvaregisteret: Optional[bool] = None

    #: Underenheter som i utgangspunktet ikke er mva-pliktig, kan søke om
    #: frivillig registrering i Merverdiavgiftsregisteret
    frivillig_mva_registrert_beskrivelser: List[str] = Field(default_factory=list)

    #: Næringskode 1
    naeringskode1: Optional[Naering] = None

    #: Næringskode 2
    naeringskode2: Optional[Naering] = None

    #: Næringskode 3
    naeringskode3: Optional[Naering] = None

    #: Hjelpeenhetskode
    hjelpeenhetskode: Optional[Naering] = None

    #: Antall ansatte
    antall_ansatte: Optional[int] = None

    #: Angir om enheten har registrert ansatte
    har_registrert_antall_ansatte: Optional[bool] = None

    #: Underenhetens overordnede enhet
    overordnet_enhet: Optional[str] = None

    #: Underenhetens beliggenhetsadresse
    beliggenhetsadresse: Optional[Adresse] = None

    #: Underenhetens oppstartsdato
    oppstartsdato: DateOrNone = None

    #: Underenhetens dato for eierskifte
    dato_eierskifte: DateOrNone = None

    #: Nedleggelsesdato for underenheten
    nedleggelsesdato: DateOrNone = None

    #: Dato under-/enheten ble slettet
    slettedato: DateOrNone = None


class RolleType(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    #: Kode for rolletype
    kode: str

    #: Beskrivelse av rolletypen
    beskrivelse: str


class RollePersonNavn(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    #: Personens fornavn
    fornavn: str

    #: Personens mellomnavn
    mellomnavn: Optional[str] = None

    #: Personens etternavn
    etternavn: str


class RollePerson(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    #: Personens fødselsdato
    fodselsdato: dt.date

    #: Personens fulle navn
    navn: RollePersonNavn

    #: Personens verge
    verge: Optional["RollePerson"] = None

    #: Hvorvidt personen er død
    er_doed: bool


class RolleEnhet(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    #: Unik id-nummer tilhørende enheten
    organisasjonsnummer: str

    #: Organisasjonsformen til enheten
    organisasjonsform: Organisasjonsform

    #: Enhetens navn
    navn: List[str] = Field(default_factory=list)

    #: Hvorvidt enheten er slettet
    er_slettet: bool


class RolleFullmektig(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    #: Navn på fullmektig
    navn: Optional[str] = None

    #: Adresser/adresselinjer knyttet til fullmektig
    adresse: List[str] = Field(default_factory=list)


class Rolle(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    #: Rolletype, og beskrivelse av typen
    type: RolleType

    #: Person som innehar rollen
    person: Optional[RollePerson] = None

    #: Enhet som innehar rollen
    enhet: Optional[RolleEnhet] = None

    #: Rollens ansvarsandel for selskapets forpliktelser, i brøk eller prosent
    ansvarsandel: Optional[str] = None

    #: Kode og beskrivelse av hvem rollen representerer (ikke innehaver)
    valgt_av: Optional[RolleType] = None

    #: Fratrådt fra rolle
    fratraadt: bool

    #: Liste over fullmektige
    fullmektige: List[RolleFullmektig] = Field(default_factory=list)

    #: Rekkefølgen på rollen i gruppen
    rekkefolge: Optional[int] = None


class RolleGruppeType(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    #: Kode for rollegruppetype
    kode: str

    #: Beskrivelse av rollegruppetypen
    beskrivelse: str


class RolleGruppe(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    #: Rollegruppetype, og beskrivelse av typen
    type: RolleGruppeType

    #: Dato for siste endring
    sist_endret: dt.date

    #: Liste med alle rollene i gruppen
    roller: List[Rolle]


class RollerResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    #: Liste med rollegrupper knyttet til enheten
    rollegrupper: List[RolleGruppe]
