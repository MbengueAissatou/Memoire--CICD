import pytest
from django.contrib.auth.models import User
from rsa_app.models import RSAKey

@pytest.mark.integration
@pytest.mark.django_db
def test_rsa_key_save_in_db():
    key = RSAKey.objects.create(name="Integration Key", public_key="pub", private_key="priv")
    retrieved = RSAKey.objects.get(name="Integration Key")
    assert retrieved.public_key == "pub"
    assert retrieved.private_key == "priv"
