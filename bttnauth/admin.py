from django.contrib import admin

# Register your models here.

from .models import AuthTokens

admin.site.register(AuthTokens)
