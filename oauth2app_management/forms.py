from django.forms import ModelForm

from oauth2app.models import Client

class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'description', 'redirect_uri']
