from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin, ProcessFormView
from django.forms import Form
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from oauth2app.models import Client, AccessToken, TimestampGenerator

from .forms import ClientForm

class ClientViewMixin(object):
    def get_queryset(self):
        return Client.objects.filter(user=self.request.user)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ClientViewMixin, self).dispatch(*args, **kwargs)

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
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AuthorizedClientViewMixin, self).dispatch(*args, **kwargs)

class AuthorizedClientListView(AuthorizedClientViewMixin, ListView):
    template_name = 'oauth2app/authorized_client_list.html'
    pass

class AuthorizedClientRevokeView(AuthorizedClientViewMixin, DetailView, FormMixin, ProcessFormView):
    template_name = 'oauth2app/authorized_client_revoke.html'
    form_class = Form
    def get_success_url(self):
        return reverse('oauth2_authorized_client_list')
    def form_valid(self, form):
        # remove the token(s) authorizing this client for this user
        client = self.get_object()
        AccessToken.objects.filter(user=self.request.user, client=client).delete()
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

