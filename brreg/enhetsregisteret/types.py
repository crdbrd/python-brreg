from datetime import date, datetime
from typing import List, Optional

import attr


__all__ = [
    'Adresse',
    'Enhet',
    'InstitusjonellSektorkode',
    'Naeringskode',
    'Organisasjonsform',
]


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
class Enhet:
    organisasjonsnummer: str
    navn: str
    organisasjonsform: Organisasjonsform
    hjemmeside: Optional[str]
    registreringsdato_enhetsregisteret: Optional[date]
    registrert_i_mvaregisteret: Optional[bool]
    naeringskode1: Optional[Naeringskode]
    antall_ansatte: Optional[int]
    forretningsadresse: Optional[Adresse]
    stiftelsesdato: Optional[date]
    institusjonell_sektorkode: Optional[InstitusjonellSektorkode]
    registrert_i_foretaksregisteret: Optional[bool]
    registrert_i_stiftelsesregisteret: Optional[bool]
    registrert_i_frivillighetsregisteret: Optional[bool]
    siste_innsendte_aarsregnskap: Optional[int]
    konkurs: Optional[bool]
    under_avvikling: Optional[bool]
    under_tvangsavvikling_eller_tvangsopplosning: Optional[bool]
    maalform: Optional[str]
    slettedato: Optional[str]

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
            slettedato=json.get('slettedato'),
        )


def parse_date(date_string: Optional[str]) -> Optional[date]:
    if date_string is None:
        return None
    return datetime.strptime(date_string, '%Y-%m-%d').date()


def parse_int(int_string: Optional[str]) -> Optional[int]:
    if int_string is None:
        return None
    return int(int_string)
