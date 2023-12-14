from typing import Optional

import pytest

from brreg.enhetsregisteret import (
    KommunenummerValidator,
    OrganisasjonsnummerValidator,
    SektorkodeValidator,
)


@pytest.mark.parametrize(
    ("value", "expected", "error"),
    [
        ("1234", "1234", None),
        (
            "12345",
            None,
            "String should have at most 4 characters",
        ),
        (
            "123",
            None,
            "String should have at least 4 characters",
        ),
        ("abcd", None, r"String should match pattern '\^\\d\{4\}\$'"),
    ],
)
def test_kommunenummer(
    value: str,
    expected: Optional[str],
    error: Optional[str],
) -> None:
    if expected:
        assert KommunenummerValidator.validate_python(value) == expected

    if error:
        with pytest.raises(ValueError, match=error):
            assert KommunenummerValidator.validate_python(value)


@pytest.mark.parametrize(
    ("value", "expected", "error"),
    [
        ("123456789", "123456789", None),
        ("123 456 789", "123456789", None),
        (
            "1234567890",
            None,
            "Value should have at most 9 items after validation, not 10",
        ),
        (
            "12345678",
            None,
            "Value should have at least 9 items after validation, not 8",
        ),
        ("aaabbbccc", None, r"String should match pattern '\^\\d\{9\}\$'"),
    ],
)
def test_organisasjonsnummer(
    value: str,
    expected: Optional[str],
    error: Optional[str],
) -> None:
    if expected:
        assert OrganisasjonsnummerValidator.validate_python(value) == expected

    if error:
        with pytest.raises(ValueError, match=error):
            assert OrganisasjonsnummerValidator.validate_python(value)


@pytest.mark.parametrize(
    ("value", "expected", "error"),
    [
        ("1234", "1234", None),
        (
            "12345",
            None,
            "String should have at most 4 characters",
        ),
        (
            "123",
            None,
            "String should have at least 4 characters",
        ),
        ("abcd", None, r"String should match pattern '\^\\d\{4\}\$'"),
    ],
)
def test_sektorkode(
    value: str,
    expected: Optional[str],
    error: Optional[str],
) -> None:
    if expected:
        assert SektorkodeValidator.validate_python(value) == expected

    if error:
        with pytest.raises(ValueError, match=error):
            assert SektorkodeValidator.validate_python(value)
