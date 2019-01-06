from datetime import date, datetime
from typing import List, Optional

import attr


@attr.s(auto_attribs=True)
class InstitusjonellSektorkode:
    kode: str
    beskrivelse: str

    def __str__(self):
        return f'{self.beskrivelse} ({self.kode})'

    @classmethod
    def from_json(
        cls, json: Optional[dict]
    ) -> Optional['InstitusjonellSektorkode']:
        if not json:
            return None

        return cls(kode=json['kode'], beskrivelse=json['beskrivelse'])


@attr.s(auto_attribs=True)
class Adresse:
    land: str
    landkode: str
    postnummer: str
    poststed: str
    adresse: List[str]
    kommune: str
    kommunenummer: str

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


@attr.s(auto_attribs=True)
class Naeringskode:
    kode: str
    beskrivelse: str

    def __str__(self):
        return f'{self.beskrivelse} ({self.kode})'

    @classmethod
    def from_json(cls, json: Optional[dict]) -> Optional['Naeringskode']:
        if not json:
            return None
        return cls(kode=json['kode'], beskrivelse=json['beskrivelse'])


@attr.s(auto_attribs=True)
class Organisasjonsform:
    kode: str
    beskrivelse: str

    def __str__(self):
        return f'{self.beskrivelse} ({self.kode})'

    @classmethod
    def from_json(cls, json: dict) -> 'Organisasjonsform':
        return cls(kode=json['kode'], beskrivelse=json['beskrivelse'])


@attr.s(auto_attribs=True)
class Organisasjon:
    organisasjonsnummer: str
    navn: str
    organisasjonsform: Organisasjonsform
    hjemmeside: Optional[str]
    registreringsdatoEnhetsregisteret: Optional[date]
    registrertIMvaregisteret: Optional[bool]
    naeringskode1: Optional[Naeringskode]
    antallAnsatte: Optional[int]
    forretningsadresse: Optional[Adresse]
    stiftelsesdato: Optional[date]
    institusjonellSektorkode: Optional[InstitusjonellSektorkode]
    registrertIForetaksregisteret: Optional[bool]
    registrertIStiftelsesregisteret: Optional[bool]
    registrertIFrivillighetsregisteret: Optional[bool]
    sisteInnsendteAarsregnskap: Optional[str]
    konkurs: Optional[bool]
    underAvvikling: Optional[bool]
    underTvangsavviklingEllerTvangsopplosning: Optional[bool]
    maalform: Optional[str]
    slettedato: Optional[str]

    def __str__(self):
        return f'{self.navn} ({self.organisasjonsnummer})'

    @classmethod
    def from_json(cls, json: dict) -> Optional['Organisasjon']:
        if not json:
            return None

        return cls(
            organisasjonsnummer=json['organisasjonsnummer'],
            navn=json['navn'],
            organisasjonsform=Organisasjonsform.from_json(
                json['organisasjonsform']
            ),
            hjemmeside=json.get('hjemmeside'),
            registreringsdatoEnhetsregisteret=parse_date(
                json.get('registreringsdatoEnhetsregisteret')
            ),
            registrertIMvaregisteret=json.get('registrertIMvaregisteret'),
            naeringskode1=Naeringskode.from_json(json.get('naeringskode1')),
            antallAnsatte=json.get('antallAnsatte'),
            forretningsadresse=Adresse.from_json(
                json.get('forretningsadresse')
            ),
            stiftelsesdato=parse_date(json.get('stiftelsesdato')),
            institusjonellSektorkode=InstitusjonellSektorkode.from_json(
                json.get('institusjonellSektorkode')
            ),
            registrertIForetaksregisteret=json.get(
                'registrertIForetaksregisteret'
            ),
            registrertIStiftelsesregisteret=json.get(
                'registrertIStiftelsesregisteret'
            ),
            registrertIFrivillighetsregisteret=json.get(
                'registrertIFrivillighetsregisteret'
            ),
            sisteInnsendteAarsregnskap=json.get('sisteInnsendteAarsregnskap'),
            konkurs=json.get('konkurs'),
            underAvvikling=json.get('underAvvikling'),
            underTvangsavviklingEllerTvangsopplosning=json.get(
                'underTvangsavviklingEllerTvangsopplosning'
            ),
            maalform=json.get('maalform'),
            slettedato=json.get('slettedato'),
        )


def parse_date(date_string: Optional[str]) -> Optional[date]:
    if not date_string:
        return None
    return datetime.strptime(date_string, '%Y-%m-%d').date()
