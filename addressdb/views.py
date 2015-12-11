from __future__ import absolute_import
from django.views import generic
from .forms import RegistrationForm, LoginForm, PersonForm, ContactForm, ContactAddressFormSet
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy
from .models import Person, Contact
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView
from django.views.generic.edit import FormMixin, ProcessFormView
from django.shortcuts import render, redirect, get_object_or_404
from formtools.wizard.views import SessionWizardView
from django.forms.models import model_to_dict
from django.http import HttpResponseForbidden, Http404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from datetime import datetime
import qsstats

class SignUpView(generic.CreateView):
    form_class = RegistrationForm
    model = User
    success_url = reverse_lazy('addressdb:add_contact')
    template_name = 'addressdb/signup.html'

    def form_valid(self, form):
        valid = super(SignUpView, self).form_valid(form)
        username, password = form.cleaned_data.get('email'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid 


class HomePageView(ListView):
    template_name = 'addressdb/home.html'
    model = Person

    def get_queryset(self):
        return Person.objects.filter(user=self.request.user)

class ContactReportView(ListView):
    template_name = 'addressdb/user/contact_report.html'

    def get_queryset(self):
        qs = Person.objects.all()
        return qs 


class LoginView(generic.FormView):
    form_class = LoginForm
    success_url = reverse_lazy('addressdb:home')
    template_name = 'addressdb/login.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(self.request, user)
            return super(LoginView, self).form_valid(form)
        else:
            return self.form_invalid(form)

class LogOutView(generic.RedirectView):
    url = reverse_lazy('addressdb:logout')

    def get(self, request, *args, **kwargs):
        logout(request)
        print("Log out invoked")
        return super(LogOutView, self).get(request, *args, **kwargs)

    def get_redirect_url(self):
        logout(self.request)
        return reverse('addressdb:home')

def logout_view(request):
    print("Log out invoked")
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/addressdb/accounts/login")

def contact_new(request):
    contact_form = ContactForm()
    person_form = PersonForm()
    return render(request,'addressdb/add.html', {'contact_form':contact_form, 'person_form':person_form, })

class CreatePersonView(CreateView):
    form_class = PersonForm
    success_url = reverse_lazy('addressdb:home')
    template_name = 'addressdb/new_contact.html'

    def form_valid(self, form):
        print(self.request)
        form.instance.user = self.request.user
        return super(CreatePersonView, self).form_valid(form)

    #def get_success_url(self):
        # redirect to the Contact view.
    #    return self.get_object().get_absolute_url()

class CreateAddressView(CreateView):
    form_class = ContactForm
    success_url = reverse_lazy('addressdb:home')
    template_name = 'addressdb/new_address.html'

    def form_valid(self, form):
        print(self.request)
        form.instance.user = self.request.user
        return super(CreateAddressView, self).form_valid(form)    

class EditContactAddressView(UpdateView):
    model = Person
    template_name = 'edit_addresses.html'
    form_class = ContactAddressFormSet

    def get_success_url(self):

        # redirect to the Contact view.
        return self.get_object().get_absolute_url()

class ContactAddressWizard(SessionWizardView):
    template_name = "addressdb/contact_address_form.html"
    def done(self, form_list, form_dict, **kwargs):
        user = self.request.user
        if 'contact_id' in self.kwargs:
            contact_id = self.kwargs['contact_id']
            person = get_object_or_404(Person, pk=contact_id)
            address = person.address

            if person.user != user:
                raise HttpResponseForbidden()
            else:
                for form in form_list:
                    print(form.cleaned_data)
                    if isinstance(form, ContactForm):
                        address_from_select = form.cleaned_data.get('address')
                        print(address_from_select)
                        if address_from_select is None:
                            if address_from_select is None:
                                address.address1 = form.cleaned_data.get('address1')
                                address.address2 = form.cleaned_data.get('address2')
                                address.address3 = form.cleaned_data.get('address3')
                                address.address4 = form.cleaned_data.get('address4')
                                address.city = form.cleaned_data.get('city')
                                address.state = form.cleaned_data.get('state')
                                address.zipcode = form.cleaned_data.get('zipcode')
                                address.country = form.cleaned_data.get('country')
                                address.user = user
                                address = address.save()
                        else:
                            address = Contact.objects.get(pk=address_from_select.id)
                    elif isinstance(form, PersonForm):
                        person.first_name = form.cleaned_data.get('first_name')
                        person.last_name = form.cleaned_data.get('last_name')
                        person.nick_name = form.cleaned_data.get('nick_name')
                        person.family_name = form.cleaned_data.get('family_name')
                        person.father_name = form.cleaned_data.get('father_name')
                        person.mother_name = form.cleaned_data.get('mother_name')
                        person.gothram = form.cleaned_data.get('gothram')
                        person.star = form.cleaned_data.get('star')
                        person.gender = form.cleaned_data.get('gender')
                        person.blood_group = form.cleaned_data.get('blood_group')
                        person.dob = form.cleaned_data.get('dob')
                        person.relation = form.cleaned_data.get('relation')
                        person.email = form.cleaned_data.get('email')
                        person.primary_phone = form.cleaned_data.get('primary_phone')
                        person.secondary_phone1 = form.cleaned_data.get('secondary_phone1')
                        person.secondary_phone2 = form.cleaned_data.get('secondary_phone2')
                        person.extra_info = form.cleaned_data.get('extra_info')
                        person.user = user
                        person.address = address
                        person.save()
        else:
            person_data = {}
            for form in form_list:
                if isinstance(form, ContactForm):
                    if form.cleaned_data.get('address') is None:
                            contact_instance= Contact.objects.get_or_create(address1=form.cleaned_data.get('address1'), 
                                                                         address2=form.cleaned_data.get('address2'),
                                                                         address3=form.cleaned_data.get('address3'),
                                                                         address4=form.cleaned_data.get('address4'),
                                                                         city=form.cleaned_data.get('city'),
                                                                         state=form.cleaned_data.get('state'),
                                                                         zipcode=form.cleaned_data.get('zipcode'),
                                                                         country=form.cleaned_data.get('country'),
                                                                         user=user)[0]
                    else:
                        address = self.get_cleaned_data_for_step('1')['address']
                        contact_instance = Contact.objects.get(pk=address.id)
                elif isinstance(form, PersonForm):
                    print(form.cleaned_data)
                    person_data = form.cleaned_data
                else:
                    form.save()
            person_data.update({'address':contact_instance, 'user':user})
            Person.objects.create(**person_data)
        return redirect('addressdb:home')

    def get_form_initial(self, step):
        #print("In ContactAddressWizard View: " + self.request.user.username)
        initial = self.initial_dict.get(step, {})
        if 'contact_id' in self.kwargs:
            initial.update({'person': self.request.user, 'contact_id': self.kwargs['contact_id']})
        else:
            initial.update({'person': self.request.user})
        return initial

    def get_form_instance(self, step):
        if 'contact_id' in self.kwargs:
            contact_id = self.kwargs['contact_id']
            person = Person.objects.get(id=contact_id, user=self.request.user)
            if step == '0':
                return person
            else:
                return person.address
        else:
            return self.instance_dict.get(step, None)

class ListContactView(ListView):
    model = Person

class DeleteContactView(DeleteView):
    model = Person
    template_name = 'addressdb/delete_contact.html'

    def get_success_url(self):
        return reverse_lazy('addressdb:home')
