# &#x1F4C7; python-brreg

_API client for Brønnøysundregistrene's open API._

[![Tests](https://img.shields.io/github/actions/workflow/status/crdbrd/python-brreg/tests.yml?branch=main)](https://github.com/crdbrd/python-brreg/actions/workflows/tests.yml)
[![Docs](https://img.shields.io/readthedocs/brreg)](https://brreg.readthedocs.io/en/latest/)
[![Coverage](https://img.shields.io/codecov/c/gh/crdbrd/python-brreg)](https://codecov.io/gh/crdbrd/python-brreg)
[![PyPI](https://img.shields.io/pypi/v/brreg)](https://pypi.org/project/brreg/)

---

`python-brreg`is a Python library for interacting with the open APIs of the
Norwegian Business Registry, [Brønnøysundregistrene](https://www.brreg.no/).

## Installation

The library requires Python 3.8 or newer.

The library can be installed from [PyPI](https://pypi.org/project/brreg/):

```
python3 -m pip install brreg
```

## Project resources

- [Documentation](https://brreg.readthedocs.io/)
- [Source code](https://github.com/crdbrd/python-brreg)
- [Releases](https://github.com/crdbrd/python-brreg/releases)
- [Issue tracker](https://github.com/crdbrd/python-brreg/issues)
- [Contributors](https://github.com/crdbrd/python-brreg/graphs/contributors)

## Features

### Enhetsregistret

The `brreg.enhetsregisteret` part of this library wraps the open
[Enhetsregistret API](https://data.brreg.no/enhetsregisteret/api/docs/index.html).

This is a list of all features this library could implement on top of this API.
However, I will not attempt to make the project cover all parts of
Brønnøysundregisterene's API. I am open to requests, so that time is spent on
the parts of the API that there is an actual demand for.

- Enheter
  - Search - Implemented
  - Get one by organization number - Implemented
  - Get one's roles by organization number - Implemented
  - Get all updates since given time - Request if needed
- Underenheter
  - Search - Implemented
  - Get one by organization number - Implemented
  - Get all updates since given time - Request if needed
- Organisasjonsform
  - Get all - Request if needed
- Rolletype
  - Get all - Request if needed
  - Get one - Request if needed
- Rollegruppetype
  - Get all - Request if needed
  - Get one - Request if needed
- Representant
  - Get all - Request if needed
  - Get one - Request if needed
- Kommuner
  - Get all - Request if needed
- Matrikkelenhet
  - Get one by matrikkelnummer - Request if needed
  - Get one by matrikkelenhet-ID - Request if needed

## License

Copyright
2019 [Otovo ASA](https://www.otovo.com/),
2023 [Cardboard AS](https://cardboard.inc/).

Licensed under the
[Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).
