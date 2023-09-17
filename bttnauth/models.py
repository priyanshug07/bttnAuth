from django.db import models

# Create your models here.

class AuthTokens(models.Model):
    user_id = models.IntegerField(null=False, blank=False, unique=True, primary_key=True)
    access_token = models.CharField(max_length=200, null=False, blank=False)
    refresh_token = models.CharField(max_length=200, null=False, blank=False)
    auth_expires_at = models.DateTimeField()
    refresh_expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True, blank=False)

    class Meta:
        indexes = [
            models.Index(fields=["access_token"])
        ]