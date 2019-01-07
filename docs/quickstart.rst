==========
Quickstart
==========

The following examples takes you through typical use cases with the
:mod:`brreg` library.


Organization details by organization number
===========================================

To get details about an organization ("enhet") given its organization number:

>>> from brreg import enhetsregisteret
>>> enhet = enhetsregisteret.get_enhet('915501680')
>>> enhet.organisasjonsnummer
'915501680'
>>> enhet.navn
'OTOVO AS'
>>> enhet.organisasjonsform
Organisasjonsform(kode='AS', beskrivelse='Aksjeselskap')
>>> enhet.forretningsadresse
Adresse(land='Norge', landkode='NO', postnummer='0181', poststed='OSLO', adresse=['Torggata 5'], kommune='OSLO', kommunenummer='0301')
>>>
