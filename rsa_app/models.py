from django.db import models


class RSAKey(models.Model):
    name = models.CharField(max_length=255)
    public_key = models.TextField()
    private_key = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


