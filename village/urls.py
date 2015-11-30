"""village URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
from addressdb.views import LoginView
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse_lazy

urlpatterns = [
 	url(r'^addressdb/', include('addressdb.urls', namespace="addressdb")),
 	url(r'^$', RedirectView.as_view(url=reverse_lazy('addressdb:home')), name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', LoginView.as_view(), name='login'),
    #url(r'^login/$', 'django.contrib.auth.views.login', {"template_name" : "addressdb/login.html",}, name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/login'}, name='logout'),
    url(r'^passwordreset/$', auth_views.password_reset,
                            {'post_reset_redirect': reverse_lazy('auth_password_reset_done'),
                             'template_name': 'addressdb/registration/password_reset_form.html'
                            },
                            name='auth_password_reset'),
    url(r'^passwordreset/complete/$', auth_views.password_reset_complete,
                           {'template_name': 'addressdb/registration/password_reset_complete.html'},
                           name='auth_password_reset_complete'),
    url(r'^passwordreset/done/$', auth_views.password_reset_done,
                           {'template_name': 'addressdb/registration/password_reset_done.html'},
                           name='auth_password_reset_done'),
    url(r'^passwordreset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm,
                           {'post_reset_redirect': '/passwordreset/complete/',
                            'template_name': 'addressdb/registration/password_reset_confirm.html'
                           }, name='password_reset_confirm'),
    url(r'^contact/', include('contact_form.urls')),
]
