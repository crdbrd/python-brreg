import datetime as dt

from pydantic import BaseModel, ConfigDict, Field
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
    kode: str | None = None

    #: Tekstlig beskrivelse av sektorkoden
    beskrivelse: str | None = None


class Adresse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    #: Adresse
    adresse: list[str | None] = Field(default_factory=list)

    #: Postnummer
    postnummer: str | None = None

    #: Poststed
    poststed: str | None = None

    #: Kommunenummer
    kommunenummer: str | None = None

    #: Kommune
    kommune: str | None = None

    #: Landkode
    landkode: str | None = None

    #: Land
    land: str | None = None


class Naering(BaseModel):
    """Næringskode.

    Næringskoden skal vise virksomhetens hovedaktivitet, og den skal primært
    dekke statistiske behov for Statistisk sentralbyrå (SSB).
    """

    model_config = ConfigDict(alias_generator=to_camel)

    #: Næringskoden
    kode: str | None = None

    #: Tekstlig beskrivelse av næringskoden
    beskrivelse: str | None = None


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
    hjemmeside: str | None = None

    #: Enhetens postadresse
    postadresse: Adresse | None = None

    #: Registreringsdato i Enhetsregisteret
    registreringsdato_enhetsregisteret: DateOrNone = None

    #: Hvorvidt enheten er registrert i MVA-registeret
    registrert_i_mvaregisteret: bool | None = None

    #: Enheter som i utgangspunktet ikke er mva-pliktig, kan søke om frivillig
    #: registrering i Merverdiavgiftsregisteret
    frivillig_mva_registrert_beskrivelser: list[str] = Field(default_factory=list)

    #: Næringskode 1
    naeringskode1: Naering | None = None

    #: Næringskode 2
    naeringskode2: Naering | None = None

    #: Næringskode 3
    naeringskode3: Naering | None = None

    #: Hjelpeenhetskode
    hjelpeenhetskode: Naering | None = None

    #: Antall ansatte
    antall_ansatte: int | None = None

    #: Angir om enheten har registrert ansatte
    har_registrert_antall_ansatte: bool | None = None

    #: Organisasjonsnummeret til overordnet enhet i offentlig sektor
    overordnet_enhet: str | None = None

    #: Forretningsadresse
    forretningsadresse: Adresse | None = None

    #: Stiftelsesdato
    stiftelsesdato: DateOrNone = None

    #: Sektorkode
    institusjonell_sektorkode: InstitusjonellSektor | None = None

    #: Hvorvidt enheten er registrert i Foretaksregisteret
    registrert_i_foretaksregisteret: bool | None = None

    #: Hvorvidt enheten er registrert i Stiftelsesregisteret
    registrert_i_stiftelsesregisteret: bool | None = None

    #: Hvorvidt enheten er registrert i Frivillighetsregisteret
    registrert_i_frivillighetsregisteret: bool | None = None

    #: År for siste innsendte årsregnskap
    siste_innsendte_aarsregnskap: int | None = None

    #: Hvorvidt enheten er konkurs
    konkurs: bool | None = None

    #: Kjennelsesdato for konkursen
    konkursdato: DateOrNone = None

    #: Hvorvidt enheten er under avvikling
    under_avvikling: bool | None = None

    #: Hvorvidt enheten er under tvangsavvikling eller tvangsoppløsning
    under_tvangsavvikling_eller_tvangsopplosning: bool | None = None

    #: Målform
    maalform: str | None = None

    #: Enhetens vedtektsdato
    vedtektsdato: DateOrNone = None

    #: Enhetens formål
    vedtektsfestet_formaal: list[str] = Field(default_factory=list)

    #: Enhetens aktivitet
    aktivitet: list[str] = Field(default_factory=list)

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
    hjemmeside: str | None = None

    #: Underenhetens postadresse
    postadresse: Adresse | None = None

    #: Underenhetens registreringsdato i Enhetsregisteret
    registreringsdato_enhetsregisteret: DateOrNone = None

    #: Hvorvidt underenheten er registrert i MVA-registeret
    registrert_i_mvaregisteret: bool | None = None

    #: Underenheter som i utgangspunktet ikke er mva-pliktig, kan søke om
    #: frivillig registrering i Merverdiavgiftsregisteret
    frivillig_mva_registrert_beskrivelser: list[str] = Field(default_factory=list)

    #: Næringskode 1
    naeringskode1: Naering | None = None

    #: Næringskode 2
    naeringskode2: Naering | None = None

    #: Næringskode 3
    naeringskode3: Naering | None = None

    #: Hjelpeenhetskode
    hjelpeenhetskode: Naering | None = None

    #: Antall ansatte
    antall_ansatte: int | None = None

    #: Angir om enheten har registrert ansatte
    har_registrert_antall_ansatte: bool | None = None

    #: Underenhetens overordnede enhet
    overordnet_enhet: str | None = None

    #: Underenhetens beliggenhetsadresse
    beliggenhetsadresse: Adresse | None = None

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
    mellomnavn: str | None = None

    #: Personens etternavn
    etternavn: str


class RollePerson(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    #: Personens fødselsdato
    fodselsdato: dt.date

    #: Personens fulle navn
    navn: RollePersonNavn

    #: Hvorvidt personen er død
    er_doed: bool


class RolleEnhet(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    #: Unik id-nummer tilhørende enheten
    organisasjonsnummer: str

    #: Organisasjonsformen til enheten
    organisasjonsform: Organisasjonsform

    #: Enhetens navn
    navn: list[str] = Field(default_factory=list)

    #: Hvorvidt enheten er slettet
    er_slettet: bool


class Rolle(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    #: Rolletype, og beskrivelse av typen
    type: RolleType

    #: Person som innehar rollen
    person: RollePerson | None = None

    #: Enhet som innehar rollen
    enhet: RolleEnhet | None = None

    #: Hvorvidt rollen er avregistrert
    avregistrert: bool

    #: Rollens ansvarsandel for selskapets forpliktelser, i brøk eller prosent
    ansvarsandel: str | None = None

    #: Kode og beskrivelse av hvem rollen representerer (ikke innehaver)
    valgt_av: RolleType | None = None

    #: Rekkefølgen på rollen i gruppen
    rekkefolge: int | None = None


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
    roller: list[Rolle]


class RollerResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    #: Liste med rollegrupper knyttet til enheten
    rollegrupper: list[RolleGruppe]
