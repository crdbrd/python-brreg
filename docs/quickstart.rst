==========
Quickstart
==========

The following examples takes you through typical use cases with the
:mod:`brreg` library.


Organization details by organization number
===========================================

To get details about an organization ("enhet") given its organization number:

>>> from brreg.enhetsregisteret import Client
>>> client = Client()
>>> enhet = client.get_enhet('915501680')
>>> enhet.organisasjonsnummer
'915501680'
>>> enhet.navn
'OTOVO ASA'
>>> enhet.organisasjonsform
Organisasjonsform(kode='ASA', beskrivelse='Allmennaksjeselskap')
>>> enhet.forretningsadresse
Adresse(land='Norge', landkode='NO', postnummer='0181', poststed='OSLO', adresse=['Torggata 7'], kommune='OSLO', kommunenummer='0301')
>>>
