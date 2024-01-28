=============
API reference
=============

.. module:: brreg

Exceptions
==========

.. autoclass:: BrregError
   :members:
   :undoc-members:


.. autoclass:: BrregRestError
   :members:
   :undoc-members:


Enhetsregisteret
================

.. module:: brreg.enhetsregisteret

Client
------

.. autoclass:: brreg.enhetsregisteret.Client
   :members:

Query objects
-------------

.. autoclass:: brreg.enhetsregisteret.Query
   :members:
   :exclude-members: model_config, model_fields

.. autoclass:: brreg.enhetsregisteret.EnhetQuery
   :members:
   :exclude-members: model_config, model_fields

.. autoclass:: brreg.enhetsregisteret.UnderenhetQuery
   :members:
   :exclude-members: model_config, model_fields

Pagination objects
------------------

.. autoclass:: brreg.enhetsregisteret.Cursor
   :members:
   :exclude-members: model_config, model_fields

.. autoclass:: brreg.enhetsregisteret.Page
   :members:
   :exclude-members: model_config, model_fields

.. autoclass:: brreg.enhetsregisteret.EnhetPage
   :members:
   :exclude-members: model_config, model_fields

.. autoclass:: brreg.enhetsregisteret.UnderenhetPage
   :members:
   :exclude-members: model_config, model_fields

Response objects
----------------

.. autoclass:: brreg.enhetsregisteret.Enhet
   :members:
   :exclude-members: model_config, model_fields

.. autoclass:: brreg.enhetsregisteret.Underenhet
   :members:
   :exclude-members: model_config, model_fields

.. autoclass:: brreg.enhetsregisteret.Adresse
   :members:
   :exclude-members: model_config, model_fields

.. autoclass:: brreg.enhetsregisteret.InstitusjonellSektor
   :members:
   :exclude-members: model_config, model_fields

.. autoclass:: brreg.enhetsregisteret.Naering
   :members:
   :exclude-members: model_config, model_fields

.. autoclass:: brreg.enhetsregisteret.Organisasjonsform
   :members:
   :exclude-members: model_config, model_fields

.. autoclass:: brreg.enhetsregisteret.RollerResponse
   :members:
   :exclude-members: model_config, model_fields

.. autoclass:: brreg.enhetsregisteret.RolleGruppe
   :members:
   :exclude-members: model_config, model_fields

.. autoclass:: brreg.enhetsregisteret.RolleGruppeType
   :members:
   :exclude-members: model_config, model_fields

.. autoclass:: brreg.enhetsregisteret.Rolle
   :members:
   :exclude-members: model_config, model_fields

.. autoclass:: brreg.enhetsregisteret.RolleType
   :members:
   :exclude-members: model_config, model_fields

.. autoclass:: brreg.enhetsregisteret.RollePerson
   :members:
   :exclude-members: model_config, model_fields

.. autoclass:: brreg.enhetsregisteret.RollePersonNavn
   :members:
   :exclude-members: model_config, model_fields

.. autoclass:: brreg.enhetsregisteret.RolleEnhet
   :members:
   :exclude-members: model_config, model_fields

.. autoclass:: brreg.enhetsregisteret.RolleFullmektig
   :members:
   :exclude-members: model_config, model_fields
