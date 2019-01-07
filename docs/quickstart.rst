==========
Quickstart
==========

The following examples takes you through typical use cases with the
:mod:`brreg` library.


Organization details by organization number
===========================================

To get details about an organization given its organization number:

>>> from brreg import enhetsregisteret
>>> org = enhetsregisteret.get_organization_by_number('915501680')
>>> org.organisasjonsnummer
'915501680'
>>> org.navn
'OTOVO AS'
>>> org.organisasjonsform
Organisasjonsform(kode='AS', beskrivelse='Aksjeselskap')
>>> org.forretningsadresse
Adresse(land='Norge', landkode='NO', postnummer='0181', poststed='OSLO', adresse=['Torggata 5'], kommune='OSLO', kommunenummer='0301')
>>>
