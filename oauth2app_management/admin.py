from django.contrib import admin

from oauth2app.models import Client, AccessToken

admin.site.register(Client)
admin.site.register(AccessToken)
