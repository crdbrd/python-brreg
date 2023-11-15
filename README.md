# &#x1F4C7; python-brreg

_API client for Brønnøysundregistrene's open API._

[![Tests](https://img.shields.io/github/actions/workflow/status/jodal/python-brreg/tests.yml?branch=main)](https://github.com/jodal/python-brreg/actions/workflows/tests.yml)
[![Docs](https://img.shields.io/readthedocs/brreg)](https://brreg.readthedocs.io/en/latest/)
[![Coverage](https://img.shields.io/codecov/c/gh/jodal/python-brreg)](https://codecov.io/gh/jodal/python-brreg)
[![PyPI](https://img.shields.io/pypi/v/brreg)](https://pypi.org/project/brreg/)

---

`python-brreg`is a Python library for interacting with the open APIs of the
Norwegian Business Registry, [Brønnøysundregistrene](https://www.brreg.no/).

## Installation

The library requires Python 3.8 or newer.

The package is available from [PyPI](https://pypi.org/project/brreg/):

```
python3 -m pip install brreg
```

## Project resources

- [Documentation](https://brreg.readthedocs.io/)
- [Source code](https://github.com/jodal/python-brreg)
- [Releases](https://github.com/jodal/python-brreg/releases)
- [Issue tracker](https://github.com/jodal/python-brreg/issues)
- [Contributors](https://github.com/jodal/python-brreg/graphs/contributors)

## Development status

This project was originally developed in 2019 while I worked at Otovo.
Eventually, it was never used there, and at the end of 2023, I got the project
back under my control.

I intend to brush the project up with modern project tooling and typing hints,
making it a good foundation to build upon, and will release a 1.0 release as
soon as that is done.

However, I will not attempt to make the project cover all parts of
Brønnøysundregisterene's API. I am open to requests, so that time is spent
on the parts of the API that there is an actual demand for.

## License

`python-brreg` is copyright
2019 [Otovo ASA](https://www.otovo.com/),
2023 Stein Magnus Jodal and contributors.

`python-brreg` is licensed under the
[Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).
