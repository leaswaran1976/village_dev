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

def bulk_upload(request):
    template_name = 'addressdb/user/bulk_upload.html'
    storage = messages.get_messages(request)
    storage.used = True
    if "GET" == request.method:
        return render(request, template_name, {})
    try:
        csv_file = request.FILES["csv_file"]
        print(csv_file)
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File is not CSV type')
            return HttpResponseRedirect(reverse_lazy("addressdb:bulk_upload"))
        # if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request, "Uploaded file is too big (%.2f MB)." % (
                csv_file.size / (1000 * 1000),))
            return HttpResponseRedirect(reverse_lazy("addressdb:bulk_upload"))
        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\r")
        # loop over the lines and save them in db. If error , store as string and then display
        loadError = ""
        lineCount = 1
        for line in lines:
            print(line)
            fields = line.split("|")
            print(fields)
            data_dict = {}
            lineError = False

            fieldValue = fields[0]
            if fieldValue and len(fieldValue) > 3:
                data_dict["firstname"] = fieldValue
            else:
                loadError += 'First Name was empty in line# {} or length of first name was less than 4\n'.format(lineCount)
                lineError = True

            fieldValue = fields[1]
            if fieldValue:
                data_dict["lastname"] = fieldValue
            else:
                loadError += 'Last Name was empty in line#' + \
                    lineCount + '\n'
                lineError = True

            fieldValue = fields[2]
            try:
                validate_email(fieldValue)
                data_dict["email"] = fieldValue
            except ValidationError:
                loadError += 'Email is not valid in line# {}\n'.format(lineCount)
                lineError = True

            fieldValue = fields[3]
            if(fieldValue and re.match(r'^\+?1?\d{9,15}$', fieldValue) != None):
                data_dict["phone"] = fieldValue
            else:
                loadError += 'Phone is not valid in line# {}. Phone number must be entered in the format: 999999999\n'.format(lineCount)
                lineError = True

            fieldValue = fields[4]
            if fieldValue:
                data_dict["address"] = fieldValue
            else:
                loadError += 'Address was empty in line# {}\n'.format(lineCount)
                lineError = True

            fieldValue = fields[5]
            if fieldValue:
                data_dict["city"] = fieldValue
            else:
                loadError += 'City was empty in line# {}\n'.format(lineCount)
                lineError = True

            fieldValue = fields[6]
            if fieldValue:
                data_dict["state"] = fieldValue
            else:
                loadError += 'State was empty in line# {}\n'.format(lineCount)
                lineError = True

            fieldValue = fields[7]
            if fieldValue:
                data_dict["country"] = fieldValue
            else:
                loadError += 'Country was empty in line#{}\n'.format(lineCount)
                lineError = True

            fieldValue = fields[8]
            if fieldValue and fieldValue.isdigit():
                data_dict["zipcode"] = fieldValue
            else:
                loadError += 'Zip Code was empty or incorrect in line# {}. Zip Code can contain only numbers\n'.format(lineCount)
                lineError = True

            if not lineError:
                user = None
                address = None
                person = None
                try:
                    user = User._default_manager.get(username=data_dict["email"])
                except User.DoesNotExist:
                    user = User.objects.create_user(
                        username=data_dict["email"], email=None, password='changeme')
                    user.save()
                    print('User after creation: ' + str(user) )

                try:
                    address = Contact.objects.get(
                        address1=data_dict["address"], city=data_dict["city"], state=data_dict["state"], country=data_dict["country"], zipcode=data_dict["zipcode"], user=user)
                except Contact.DoesNotExist:
                    address = Contact.objects.create(user=user)
                    address.address1 = data_dict["address"]
                    address.city = data_dict["city"]
                    address.state = data_dict["state"]
                    address.country = data_dict["country"]
                    address.zipcode = data_dict["zipcode"]
                    address.save()
                #print(address)

                try:
                    person = Person.objects.get(first_name=data_dict["firstname"], last_name=data_dict["lastname"], email=data_dict["email"])
                except Person.DoesNotExist:
                    person = Person.objects.create(user=user, address=address)
                    person.first_name = data_dict["firstname"]
                    person.last_name = data_dict["lastname"]
                    person.email = data_dict["email"]
                    person.primary_phone = data_dict["phone"]
                    person.save()
                #print(person)
            else:
                messages.error(request, loadError)
            lineCount = lineCount + 1
        messages.success(request, 'Bulk Upload Completed Successfully')
    except Exception as e:
        print("Exception in user code:")
        print('-'*60)
        traceback.print_exc(file=sys.stdout)
        print('-'*60)
        messages.error(request, "Unable to upload file. " + repr(e))
    return HttpResponseRedirect(reverse_lazy("addressdb:bulk_upload"))