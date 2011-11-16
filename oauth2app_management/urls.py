from django.conf.urls.defaults import patterns, url

from .views import ClientListView, ClientCreateView, ClientUpdateView
from .views import AuthorizedClientListView, AuthorizedClientDetailView, AuthorizedClientRevokeView

urlpatterns = patterns('',
        url(r'^authorized_clients/?$',
            AuthorizedClientListView.as_view(),
            name='oauth2_authorized_client_list',
        ),
        url(r'^authorized_clients/(?P<slug>[\w\-]+)/?$',
            AuthorizedClientDetailView.as_view(),
            name='oauth2_authorized_client_detail',
        ),
        url(r'^authorized_clients/(?P<slug>[\w\-]+)/revoke/?$',
            AuthorizedClientRevokeView.as_view(),
            name='oauth2_authorized_client_revoke',
        ),
        url(r'^clients/?$',
            ClientListView.as_view(),
            name='oauth2_client_list',
        ),
        url(r'^clients/new/?$',
            ClientCreateView.as_view(),
            name='oauth2_client_create',
        ),
        url(r'^clients/(?P<slug>[\w\-]+)/?$',
            ClientUpdateView.as_view(),
            name='oauth2_client_update',
        ),
)
