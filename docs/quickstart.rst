==========
Quickstart
==========

The following examples takes you through typical use cases with the
:mod:`brreg` library.


Querying Enhetsregisteret
=========================

To query Enhetsregisteret, you need to create a :class:`brreg.enhetsregisteret.Client` instance:

>>> from brreg.enhetsregisteret import Client
>>> client = Client()
>>>

The client instance will ensure that the HTTP connection is reused across requests.

To get details about an organization ("enhet") given its organization number:

>>> enhet = client.get_enhet('915501680')
>>> enhet.organisasjonsnummer
'915501680'
>>> enhet.navn
'OTOVO ASA'
>>> enhet.organisasjonsform
Organisasjonsform(kode='ASA', beskrivelse='Allmennaksjeselskap')
>>> enhet.forretningsadresse
Adresse(adresse=['Torggata 7'], postnummer='0181', poststed='OSLO', kommunenummer='0301', kommune='OSLO', landkode='NO', land='Norge')
>>>

To get details of a suborganization ("underenhet") given its organization number:

>>> underenhet = client.get_underenhet('915659683')
>>> underenhet.organisasjonsnummer
'915659683'
>>> underenhet.antall_ansatte
91
>>> underenhet.beliggenhetsadresse
Adresse(adresse=['Torggata 7'], postnummer='0181', poststed='OSLO', kommunenummer='0301', kommune='OSLO', landkode='NO', land='Norge')
>>>
