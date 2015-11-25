from django.conf.urls import url
from .views import HomePageView, SignUpView, LoginView
from .views import LogOutView, contact_new, CreatePersonView, logout_view
from .views import CreateAddressView, EditContactAddressView, ContactAddressWizard, DeleteContactView
from .forms import PersonForm, ContactForm
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url('^$', login_required(HomePageView.as_view()), name='home'),
    url(r'^accounts/register/$', SignUpView.as_view(), name='signup'),
    url(r'^changepassword/$', SignUpView.as_view(), name='changepassword'),
    #url(r'^accounts/login/$', LoginView.as_view(), name='login'),
    #url(r'^accounts/logout/$', LogOutView.as_view(), name='logout'),
    #url(r'^accounts/logout/$', logout_view, name='logout'),
    #url(r'^newcontact/$', CreatePersonView.as_view(), name='new_contact'),
    #url(r'^newaddress/$', CreateAddressView.as_view(), name='new_address'),
    #url(r'^add/$', contact_new, name='new_personcontact'),
    url(r'^add_contact/$', login_required(ContactAddressWizard.as_view([PersonForm, ContactForm])), name='add_contact'),
    url(r'^edit_contact/(?P<contact_id>\d+)/$', login_required(ContactAddressWizard.as_view([PersonForm, ContactForm])), name='edit_contact'),
    url(r'^delete_contact/(?P<pk>\d+)/$', login_required(DeleteContactView.as_view()), name='delete_contact'),
]
