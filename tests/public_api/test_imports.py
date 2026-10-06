"""Public API smoke tests."""


def test_package_imports():
    import nxopenkit
    assert nxopenkit is not None
