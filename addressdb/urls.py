from django.conf.urls import url
from .views import HomePageView, SignUpView, LoginView
from .views import LogOutView, contact_new, CreatePersonView, logout_view
from .views import CreateAddressView, EditContactAddressView, ContactAddressWizard, DeleteContactView, ContactReportView
from .forms import PersonForm, ContactForm
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url('^$', login_required(HomePageView.as_view()), name='home'),
    url(r'^accounts/register/$', SignUpView.as_view(), name='signup'),
    url(r'^add_contact/$', login_required(ContactAddressWizard.as_view([PersonForm, ContactForm])), name='add_contact'),
    url(r'^edit_contact/(?P<contact_id>\d+)/$', login_required(ContactAddressWizard.as_view([PersonForm, ContactForm])), name='edit_contact'),
    url(r'^delete_contact/(?P<pk>\d+)/$', login_required(DeleteContactView.as_view()), name='delete_contact'),
    url(r'^contact_report/$', login_required(ContactReportView.as_view()), name='contact_report'),
]
