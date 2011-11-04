from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import FormMixin, ProcessFormView
from django.forms import Form
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from oauth2app.models import Client, AccessToken, TimestampGenerator

from .forms import ClientForm

class ClientViewMixin(object):
    def get_queryset(self):
        return Client.objects.filter(user=self.request.user)

class ClientCreateView(ClientViewMixin, CreateView):
    template_name = 'oauth2app/client_create.html'
    form_class = ClientForm
    context_object_name = "client_list"
    def get_success_url(self):
        # this could use reverse_lazy in Django 1.4:
        # http://stackoverflow.com/questions/6482573/the-included-urlconf-manager-urls-doesnt-have-any-patterns-in-it
        return reverse('oauth2_client_list')
    def form_valid(self, form):
        client = form.save(commit=False)
        client.user = self.request.user
        client.save()
        self.object = client
        return HttpResponseRedirect(self.get_success_url())

class ClientListView(ClientViewMixin, ListView):
    pass

class ClientUpdateView(ClientViewMixin, UpdateView):
    template_name = 'oauth2app/client_update.html'
    form_class = ClientForm
    slug_field = 'key'
    def get_success_url(self):
        # this could use reverse_lazy in Django 1.4:
        # http://stackoverflow.com/questions/6482573/the-included-urlconf-manager-urls-doesnt-have-any-patterns-in-it
        return reverse('oauth2_client_list')

class AuthorizedClientViewMixin(object):
    slug_field = 'key'
    def get_queryset(self):
        now = TimestampGenerator()()
        return Client.objects.filter(
            accesstoken__user=self.request.user,
            accesstoken__expire__gt=now,
        )

class AuthorizedClientListView(AuthorizedClientViewMixin, ListView):
    template_name = 'oauth2app/authorized_client_list.html'
    pass

class AuthorizedClientRevokeView(AuthorizedClientViewMixin, SingleObjectTemplateResponseMixin, FormMixin, ProcessFormView):
    template_name_suffix = '_revoke'
    form_class = Form
    def get_success_url(self):
        return reverse('oauth2_authorized_client_list')
    def form_valid(self, form):
        # remove the token(s) authorizing this client for this user
        AccessToken.objects.filter(user=self.request.user, client=this.get_object()).delete()
        return super(AuthorizedClientRevokeView, self).form_valid(form)

class AuthorizedClientDetailView(AuthorizedClientViewMixin, DetailView):
    template_name = 'oauth2app/authorized_client_detail.html'
    pass


class TokenListView(ListView):
    def get_queryset(self):
        now = TimestampGenerator()()
        return AccessToken.objects.filter(user=self.request.user, expire__gt=now)

class TokenDetailView(DetailView):
    def get_queryset(self):
        now = TimestampGenerator()()
        return AccessToken.objects.filter(user=self.request.user, expire__gt=now)

class TokenDeleteView(DeleteView):
    def get_queryset(self):
        now = TimestampGenerator()()
        return AccessToken.objects.filter(user=self.request.user, expire__gt=now)

