from django.db import models

class RSAKey(models.Model):
    # your fields here
    public_key = models.TextField()
    private_key = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)