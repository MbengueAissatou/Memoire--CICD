import pytest
from rsa_app.models import RSAKey

@pytest.mark.unit
def test_rsa_key_creation():
    key = RSAKey(name="Test Key", public_key="pub", private_key="priv")
    assert key.name == "Test Key"
    assert key.public_key == "pub"
    assert key.private_key == "priv"
