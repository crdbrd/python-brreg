==========
Quickstart
==========

The following examples takes you through typical use cases, showing how to use
the :mod:`brreg` library to query Enhetsregisteret.


Create a client
===============

To query Enhetsregisteret, you need to create a
:class:`brreg.enhetsregisteret.Client` instance:

>>> from brreg.enhetsregisteret import Client
>>> client = Client()
>>>

The client instance will ensure that the HTTP connection is reused across
requests.


Details about a specific organization
=====================================

To get details about an organization ("enhet") given its organization number:

>>> enhet = client.get_enhet('930070556')
>>> enhet.organisasjonsnummer
'930070556'
>>> enhet.navn
'CARDBOARD AS'
>>> enhet.organisasjonsform
Organisasjonsform(kode='AS', beskrivelse='Aksjeselskap', utgaatt=None)
>>> enhet.forretningsadresse
Adresse(adresse=['Grensen 13'], postnummer='0159', poststed='OSLO', kommunenummer='0301', kommune='OSLO', landkode='NO', land='Norge')
>>>

To get details of a suborganization ("underenhet") given its organization number:

>>> underenhet = client.get_underenhet('930090069')
>>> underenhet.organisasjonsnummer
'930090069'
>>> underenhet.antall_ansatte
5
>>> underenhet.beliggenhetsadresse
Adresse(adresse=['Grensen 13'], postnummer='0159', poststed='OSLO', kommunenummer='0301', kommune='OSLO', landkode='NO', land='Norge')
>>>

To get details of roles ("roller") given an organization number:

>>> rollegrupper = client.get_roller('930070556')
>>> [rg.type.beskrivelse for rg in rollegrupper]
['Daglig leder/ adm.direktør', 'Styre', 'Regnskapsfører']
>>> rollegrupper[2].roller[0].enhet
RolleEnhet(organisasjonsnummer='914549140', organisasjonsform=Organisasjonsform(kode='AS', beskrivelse='Aksjeselskap', utgaatt=None), navn=['SYNEGA REGNSKAP AS'], er_slettet=False)
>>>


Searching for organizations
===========================

To search for organizations ("enheter"):

>>> from brreg.enhetsregisteret import EnhetQuery
>>> cursor = client.search_enhet(EnhetQuery(navn='cardboard'))
>>>

The search result is paginated, which you can see by looking at the available page numbers:

>>> list(cursor.page_numbers)
[0]
>>>

The cursor has two iterators, ``cursor.pages`` to iterate over the pages:

>>> page = next(cursor.pages)
>>> page.page_number
0
>>> page.total_items
2
>>> page.total_pages
1
>>> [enhet.navn for enhet in page.items]
['CARDBOARD AS', 'RECYCLING AND TRADING OF SCRAP METAL AND CARDBOARD PAPER V/ABIKAR']
>>>

And ``cursor.items`` to iterate over all items in all pages:

>>> [enhet.navn for enhet in cursor.items]
['CARDBOARD AS', 'RECYCLING AND TRADING OF SCRAP METAL AND CARDBOARD PAPER V/ABIKAR']
>>>

As long as you keep using the same cursor object each page is fetched only once,
no matter how many times you iterate over the pages or items.
