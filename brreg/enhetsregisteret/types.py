# -*- coding: future_fstrings -*-
from datetime import date, datetime
from typing import List, Optional
import typing

import attr


__all__ = [
    'Adresse',
    'Enhet',
    'InstitusjonellSektorkode',
    'Naeringskode',
    'Organisasjonsform',
]


@attr.s()
class InstitusjonellSektorkode:

    #: Sektorkoden
    kode  = attr.ib(type=str)

    #: Tekstlig beskrivelse av sektorkoden
    beskrivelse  = attr.ib(type=str)

    def __str__(self):
        return f'{self.beskrivelse} ({self.kode})'

    @classmethod
    def from_json(
        cls, json: Optional[dict]
    ) -> Optional['InstitusjonellSektorkode']:
        if not json:
            return None

        return cls(kode=json['kode'], beskrivelse=json['beskrivelse'])


@attr.s()
class Adresse:
    #: Land
    land = attr.ib(type=str)

    #: Landkode
    landkode  = attr.ib(type=str)

    #: Postnummer
    postnummer  = attr.ib(type=str)

    #: Poststed
    poststed  = attr.ib(type=str)

    #: Adresse
    adresse = attr.ib(type=List[str])

    #: Kommune
    kommune  = attr.ib(type=str)

    #: Kommunenummer
    kommunenummer  = attr.ib(type=str)

    def __str__(self):
        return self.adresse[0]

    @classmethod
    def from_json(cls, json: Optional[dict]) -> Optional['Adresse']:
        if not json:
            return None

        return cls(
            land=json['land'],
            landkode=json['landkode'],
            postnummer=json['postnummer'],
            poststed=json['poststed'],
            adresse=json['adresse'],
            kommune=json['kommune'],
            kommunenummer=json['kommunenummer'],
        )


@attr.s()
class Naeringskode:

    #: Næringskoden
    kode  = attr.ib(type=str)

    #: Tekstlig beskrivelse av næringskoden
    beskrivelse  = attr.ib(type=str)

    def __str__(self):
        return f'{self.beskrivelse} ({self.kode})'

    @classmethod
    def from_json(cls, json: Optional[dict]) -> Optional['Naeringskode']:
        if not json:
            return None
        return cls(kode=json['kode'], beskrivelse=json['beskrivelse'])


@attr.s()
class Organisasjonsform:

    #: Organisasjonsformen
    kode  = attr.ib(type=str)

    #: Tekstlig beskrivelse av organisasjonsformen
    beskrivelse  = attr.ib(type=str)

    def __str__(self):
        return f'{self.beskrivelse} ({self.kode})'

    @classmethod
    def from_json(cls, json: dict) -> 'Organisasjonsform':
        return cls(kode=json['kode'], beskrivelse=json['beskrivelse'])


@attr.s()
class Enhet:
    #: Organisasjonsnummer
    organisasjonsnummer  = attr.ib(type=str)

    #: Navn
    navn  = attr.ib(type=str)

    #: Organisasjonsform
    organisasjonsform = attr.ib(type=Organisasjonsform)

    #: Hjemmeside
    hjemmeside = attr.ib(type=Optional[str])

    #: Registreringsdato i Enhetsregisteret
    registreringsdato_enhetsregisteret = attr.ib(type=Optional[date])

    #: Hvorvidt enheten er registrert i MVA-registeret
    registrert_i_mvaregisteret = attr.ib(type=Optional[bool])

    #: Næringskode 1
    naeringskode1 = attr.ib(type=Optional[Naeringskode])

    #: Antall ansatte
    antall_ansatte = attr.ib(type=Optional[int])

    #: Forretningsadresse
    forretningsadresse = attr.ib(type=Optional[Adresse])

    #: Stiftelsesdato
    stiftelsesdato = attr.ib(type=Optional[date])

    #: Sektorkode
    institusjonell_sektorkode = attr.ib(type=Optional[InstitusjonellSektorkode])

    #: Hvorvidt enheten er registrert i Foretaksregisteret
    registrert_i_foretaksregisteret = attr.ib(type=Optional[bool])

    #: Hvorvidt enheten er registrert i Stiftelsesregisteret
    registrert_i_stiftelsesregisteret = attr.ib(type=Optional[bool])

    #: Hvorvidt enheten er registrert i Frivillighetsregisteret
    registrert_i_frivillighetsregisteret = attr.ib(type=Optional[bool])

    #: År for siste innsendte årsregnskap
    siste_innsendte_aarsregnskap = attr.ib(type=Optional[int])

    #: Hvorvidt enheten er konkurs
    konkurs = attr.ib(type=Optional[bool])

    #: Hvorvidt enheten er under avvikling
    under_avvikling = attr.ib(type=Optional[bool])

    #: Hvorvidt enheten er under tvangsavvikling eller tvangsoppløsning
    under_tvangsavvikling_eller_tvangsopplosning = attr.ib(type=Optional[bool])

    #: Målform
    maalform = attr.ib(type=Optional[str])

    #: Dato enheten ble slettet
    slettedato = attr.ib(type= Optional[date])

    def __str__(self):
        return f'{self.navn} ({self.organisasjonsnummer})'

    @classmethod
    def from_json(cls, json: dict) -> Optional['Enhet']:
        if not json:
            return None

        return cls(
            organisasjonsnummer=json['organisasjonsnummer'],
            navn=json['navn'],
            organisasjonsform=Organisasjonsform.from_json(
                json['organisasjonsform']
            ),
            hjemmeside=json.get('hjemmeside'),
            registreringsdato_enhetsregisteret=parse_date(
                json.get('registreringsdatoEnhetsregisteret')
            ),
            registrert_i_mvaregisteret=json.get('registrertIMvaregisteret'),
            naeringskode1=Naeringskode.from_json(json.get('naeringskode1')),
            antall_ansatte=json.get('antallAnsatte'),
            forretningsadresse=Adresse.from_json(
                json.get('forretningsadresse')
            ),
            stiftelsesdato=parse_date(json.get('stiftelsesdato')),
            institusjonell_sektorkode=InstitusjonellSektorkode.from_json(
                json.get('institusjonellSektorkode')
            ),
            registrert_i_foretaksregisteret=json.get(
                'registrertIForetaksregisteret'
            ),
            registrert_i_stiftelsesregisteret=json.get(
                'registrertIStiftelsesregisteret'
            ),
            registrert_i_frivillighetsregisteret=json.get(
                'registrertIFrivillighetsregisteret'
            ),
            siste_innsendte_aarsregnskap=parse_int(
                json.get('sisteInnsendteAarsregnskap')
            ),
            konkurs=json.get('konkurs'),
            under_avvikling=json.get('underAvvikling'),
            under_tvangsavvikling_eller_tvangsopplosning=json.get(
                'underTvangsavviklingEllerTvangsopplosning'
            ),
            maalform=json.get('maalform'),
            slettedato=parse_date(json.get('slettedato')),
        )


def parse_date(date_string: Optional[str]) -> Optional[date]:
    if date_string is None:
        return None
    return datetime.strptime(date_string, '%Y-%m-%d').date()


def parse_int(int_string: Optional[str]) -> Optional[int]:
    if int_string is None:
        return None
    return int(int_string)