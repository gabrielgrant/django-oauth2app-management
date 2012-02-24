django-oauth2app-management: a management interface for oauth2app


django-oauth2app-management provides views for users to create and manage their OAuth2
clients, see which clients they have authorized to access their account, and to revoke
those authorizations.

For an example of the views provided, see the equivalent pages on github:

- Create/manage your applications: https://github.com/account/applications/
- View/revoke third-party apps' access to your account:
  https://github.com/account/connections


Installation
------------

1. Install [oauth2app](https://github.com/hiidef/oauth2app)
2. `pip install django-oauth2app-management`
3. Add `oauth2app_management` to your list of installed applications in `settings.py`
4. Create the necessary templates (see below)
5. include `oauth2app_management.urls` in your urlconf (something like 
   `(r'^oauth2/management/', include('oauth2app_management.urls')),`)


django-oauth2app-management does not include templates out of the box, because
they should be created to match the feel of the rest of your site.


Templates
---------

oauth2app/authorized_client_detail.html
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Users view details of a client which has access to their account

Context:

``client`` - The authorized Client object

oauth2app/authorized_client_list.html
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Users view a list of clients which are authorized to access their account

Context:

``client_list`` - The list of authorized Client objects

oauth2app/authorized_client_revoke.html
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The template should allow Users to confirm that they wish to
revoke a client's access to their account. POSTing to this
URL to revoke the given client's access.

Context:

``client`` - The Client object
``form`` - An empty form.


oauth2app/client_create.html
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Users fill out a form to create a new OAuth2 client application

Context:

``form`` - an instance of ``oauth2app_management.forms.ClientForm``

oauth2app/client_update.html
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Users fill out a form to update an existing OAuth2 client application

Context:

``form`` - an instance of ``oauth2app_management.forms.ClientForm``

``client`` - the client being updated


oauth2app/client_list.html
^^^^^^^^^^^^^^^^^^^^^^^^^^

Users view a list of their registered OAuth2 Clients. This page
should link to the individual Client Update pages (using
``{% url 'oauth2_client_update' slug=client.key %}``), and to (likely)
to the Client creation view (with ``{% url 'oauth2_client_create' %}``)

Context:

``client_list`` - a list of the User's client objects
