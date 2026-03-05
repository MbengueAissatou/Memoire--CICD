import pytest

@pytest.mark.integration
@pytest.mark.django_db
def test_rsa_key_save_in_db():
    from rsa_app.models import RSAKey
    RSAKey.objects.create(  
        name="Integration Key",
        public_key="pub",
        private_key="priv"
    )
    assert RSAKey.objects.count() == 1