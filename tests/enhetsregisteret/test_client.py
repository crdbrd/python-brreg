from brreg import enhetsregisteret


def test_manual_open_close() -> None:
    client = enhetsregisteret.Client()
    assert not client._client.is_closed  # noqa: SLF001
    client.close()
    assert client._client.is_closed  # noqa: SLF001


def test_context_manager() -> None:
    with enhetsregisteret.Client() as client:
        assert not client._client.is_closed  # noqa: SLF001
    assert client._client.is_closed  # noqa: SLF001
