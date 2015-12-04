from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.conf import settings
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.core.exceptions import ValidationError
from .models import Person, Contact
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, HTML, Div
from crispy_forms.bootstrap import FormActions, PrependedText

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email ID", help_text="Required. 30 characters or fewer.", 
                             widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Please enter a valid email address.'}))

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password2'].label = "Password Confirmation"
        self.helper = FormHelper()
        self.helper.form_class = 'form-signin'
        self.helper.layout = Layout(
            PrependedText('email', '<span class="glyphicon glyphicon-user"></span>'),
            PrependedText('password1', '<span class="glyphicon glyphicon-lock"></span>'),
            PrependedText('password2', '<span class="glyphicon glyphicon-lock"></span>'),
            FormActions(
                Submit('register', 'Sign me up!', css_class='btn-primary btn btn-lg'),
                HTML('<a href={% url "addressdb:home" %} class="btn-primary btn btn-lg">Cancel</a>'),
            )
        )

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.username = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    def clean_email(self):
        username = self.cleaned_data["email"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError(username + ' is already a registered user. Enter another valid email address.')

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = ""
        self.fields['password'].label = ""

        self.helper = FormHelper()
        self.helper.form_class = 'form-signin'
        self.helper.layout = Layout(
            PrependedText('username', '<span class="glyphicon glyphicon-user"></span>'),
            PrependedText('password', '<span class="glyphicon glyphicon-lock"></span>'),
            Div(HTML('<br/>')),
            FormActions(
                Submit('login', 'Login', css_class='btn-lg btn-block'),
            ),
            HTML('<a href={% url "addressdb:signup" %} class="pull-left need-help"><strong>New User?</strong></a>'),
            HTML('<a href={% url "auth_password_reset" %} class="pull-right need-help"><strong>Reset Password?</strong></a>')
        )

    def clean_remember_me(self):
        """clean method for remember_me """
        remember_me = self.cleaned_data.get['remember_me']
        if not remember_me:
            settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = True
        else:
            settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
        return remember_me

class PersonForm(ModelForm): 
    GENDER_CHOICES = (
        ('Sgender', 'Select Gender'),
        ('Male', 'Male'),
        ('Female', 'Female'),
    )  

    GOTHRA_CHOICES = (
        ('Sgothra', 'Select Gothra'),
        ('Agastya','Agastya'),
        ('Alambani','Alambani'),
        ('Angirasa','Angirasa'),
        ('Atreya/Atri','Atreya/Atri'),
        ('Bhardwaj/Bharadvajasa','Bhardwaj/Bharadvajasa'),
        ('Bhargava','Bhargava'),
        ('Charora','Charora'),
        ('Chikitasa','Chikitasa'),
        ('Dalabhya','Dalabhya'),
        ('Darbhas','Darbhas'),
        ('Dhananjaya','Dhananjaya'),
        ('Galvasaya','Galvasaya'),
        ('Garga/Gargheyasa','Garga/Gargheyasa'),
        ('Gaubhilya','Gaubhilya'),
        ('Gautam/Gautamasa','Gautam/Gautamasa'),
        ('Harita/Haritasya','Harita/Haritasya'),
        ('Hukman Bhal','Hukman Bhal'),
        ('Jamadagni','Jamadagni'),
        ('Kalabodhana/Kalaboudha','Kalabodhana/Kalaboudha'),
        ('Kamakayana Vishwamitra','Kamakayana Vishwamitra'),
        ('Kanva','Kanva'),
        ('Kapi/Kapil','Kapi/Kapil'),
        ('Kashyapa','Kashyapa'),
        ('Katyayana','Katyayana'),
        ('Kaundinya','Kaundinya'),
        ('Kaunsh','Kaunsh'),
        ('Kaushika','Kaushika'),
        ('Kutsa/Kutsasa','Kutsa/Kutsasa'),
        ('Lakhi','Lakhi'),
        ('Lohit','Lohit'),
        ('Lomasha','Lomasha'),
        ('Mandavya','Mandavya'),
        ('Matanga','Matanga'),
        ('Mauna Bhargava','Mauna Bhargava'),
        ('Mudgala/Maudgalya/Moudgil/Modgil/Mudgal','Mudgala/Maudgalya/Moudgil/Modgil/Mudgal'),
        ('Nithunthana','Nithunthana'),
        ('Nrisimhadevara','Nrisimhadevara'),
        ('Nydravakashyapa','Nydravakashyapa'),
        ('Parashara','Parashara'),
        ('Parthivasa','Parthivasa'),
        ('Pouragutsya','Pouragutsya'),
        ('Rathitara','Rathitara'),
        ('Roushayadana','Roushayadana'),
        ('Saawarna','Saawarna'),
        ('Saharia Joshi','Saharia Joshi'),
        ('Salankayana','Salankayana'),
        ('Sangar','Sangar'),
        ('Sankrithi','Sankrithi'),
        ('Sankyanasa','Sankyanasa'),
        ('Sathamarshana','Sathamarshana'),
        ('Shandilya','Shandilya'),
        ('Shaunaka','Shaunaka'),
        ('Somnasser','Somnasser'),
        ('Soral','Soral'),
        ('Srivatsa','Srivatsa'),
        ('Sumarkanth','Sumarkanth'),
        ('Suryadhwaja','Suryadhwaja'),
        ('Tugnait','Tugnait'),
        ('Upadhyay','Upadhyay'),
        ('Upamanyu','Upamanyu'),
        ('Vadula','Vadula'),
        ('Valmiki','Valmiki'),
        ('Vashishta','Vashishta'),
        ('Vatsa','Vatsa'),
        ('Veetahavya','Veetahavya'),
        ('Vishnu','Vishnu'),
        ('Viswamitra','Viswamitra'),
        ('Yaska','Yaska'),
        ('NA', 'Not Available'),
    )

    NAKSHATRA_CHOICES = (
        ('Snakshatra', 'Select Nakshatra'),
        ('Aayilyam','Aayilyam'),
        ('Anusham','Anusham'),
        ('Aswini','Aswini'),
        ('Avittam','Avittam'),
        ('Bharani','Bharani'),
        ('Chathayam/Sadayam','Chathayam/Sadayam'),
        ('Chithirai','Chithirai'),
        ('Hastham','Hastham'),
        ('Karthigai','Karthigai'),
        ('Jyeshtha/Kettai','Jyeshtha/Kettai'),
        ('Makam','Makam'),
        ('Moolam','Moolam'),
        ('Mrigasheersham/Makeeryam','Mrigasheersham/Makeeryam'),
        ('Pooraadam','Pooraadam'),
        ('Pooram','Pooram'),
        ('Poorattathi','Poorattathi'),
        ('Poosam/Pooyyam','Poosam/Pooyyam'),
        ('Punarpoosam/Punartham','Punarpoosam/Punartham'),
        ('Revathi','Revathi'),
        ('Rohini','Rohini'),
        ('Swaathi','Swaathi'),
        ('Thiruvaathirai','Thiruvaathirai'),
        ('Thiruvonam','Thiruvonam'),
        ('Uthiraadam','Uthiraadam'),
        ('Uthiram','Uthiram'),
        ('Uthirattathi','Uthirattathi'),
        ('Visaakam','Visaakam'),
        ('NA', 'Not Available'),
    )

    BLOOD_GROUP_CHOICES = (
        ('Sbg', 'Select Blood Group'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('NA', 'Not Available'),
    )

    FAMILY_NAME_CHOICES = (
        ('Sfn', 'Select Family Name'),
        ('Choodamani', 'Choodamani'),
        ('Deekshitar', 'Deekshitar'),
        ('Essuatthan', 'Essuatthan'),
        ('Jadavallabhar', 'Jadavallabhar'),
        ('Kilimangalam', 'Kilimangalam'),
        ('Maanu Pattar', 'Maanu Pattar'),
        ('Neelu Pattar', 'Neelu Pattar'),
        ('Seshan Pattar', 'Seshan Pattar'),
        ('Sivaraman Pattar', 'Sivaraman Pattar'),
        ('Vaadhyaar', 'Vaadhyaar'),
        ('NA', 'Not Available'),
    )

    RELATIONSHIP_CHOICES = (
        ('Srelation', 'Select Relationship'),
        ('Brother', 'Brother'),
        ('Daughter', 'Daughter'),
        ('Father', 'Father'),
        ('Fiancee', 'Fiancee'),
        ('Father-in-Law', 'Father-in-Law'),
        ('GrandFather_Paternal', 'Grand Father (Paternal)'),
        ('GrandMother_Paternal', 'Grand Mother (Paternal)'),
        ('GrandFather_Maternal', 'Grand Father (Maternal)'),
        ('GrandMother_Maternal', 'Grand Mother (Maternal)'),
        ('Mother', 'Mother'),
        ('Mother-in-Law', 'Mother-in-Law'),
        ('Self', 'Self'),
        ('Son', 'Son'),
        ('Sister', 'Sister'),
        ('Spouse', 'Spouse'),
        ('Others', 'Others'),
    )

    first_name = forms.CharField(required=True, label="First Name", widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(required=True, label="Last Name", widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    nick_name = forms.CharField(required=False, label="Nick Name", widget=forms.TextInput(attrs={'placeholder': 'Nick/Pet Name'}))
    #family_name = forms.CharField(required=False, label="Family Name", widget=forms.TextInput(attrs={'placeholder': 'Kilimangalam, Maanu Pattar, Neelu Pattar, Dixithar'}))
    family_name = forms.ChoiceField(choices = FAMILY_NAME_CHOICES, required = True, label = 'Family Name')
    father_name = forms.CharField(required=False, label="Father's Name", widget=forms.TextInput(attrs={'placeholder': 'Name - Nick Name'}))
    mother_name = forms.CharField(required=False, label="Mother's Name", widget=forms.TextInput(attrs={'placeholder': 'Name - Nick Name'}))
    gothram = forms.ChoiceField(choices = GOTHRA_CHOICES, required = True, label = 'Gothra')
    star = forms.ChoiceField(choices = NAKSHATRA_CHOICES, required=True, label="Nakshatra")
    gender = forms.ChoiceField(choices = GENDER_CHOICES, required=True, label="Gender")
    blood_group = forms.ChoiceField(choices = BLOOD_GROUP_CHOICES, required=True, label="Blood Group")
    relation = forms.ChoiceField(choices = RELATIONSHIP_CHOICES, required=True, label="Relationship")
    email = forms.EmailField(required=True, label="Preferred Email", widget=forms.TextInput(attrs={'placeholder': 'Email Address'}))
    alternate_email = forms.EmailField(required=False, label="Alternate Email", widget=forms.TextInput(attrs={'placeholder': 'Alternate Email Address'}))
    #primary_phone = forms.CharField(required=True, label="Preferred Phone", widget=forms.TextInput(attrs={'placeholder': '919856745633 (Mobile#)'}))
    primary_phone = forms.RegexField(label="Preferred Phone", regex=r'^\+?1?\d{9,15}$', error_message = ("Phone number must be entered in the format: '999999999'. Up to 15 digits allowed."), widget=forms.TextInput(attrs={'placeholder': '+919882675673'}))
    #secondary_phone1 = forms.CharField(required=False, label="Alternate Phone", widget=forms.TextInput(attrs={'placeholder': '914912675673 (Home#)'}))
    secondary_phone1 = forms.RegexField(label="Alternate Phone", required=False, regex=r'^\+?1?\d{9,15}$', error_message = ("Phone number must be entered in the format: '999999999'. Up to 15 digits allowed."), widget=forms.TextInput(attrs={'placeholder': '+914912675673'}))
    #secondary_phone2 = forms.CharField(required=False, label="Secondary Phone 2", widget=forms.TextInput(attrs={'placeholder': 'Work#'}))
    extra_info = forms.CharField(required=False, label="Additional Informaton", widget=forms.Textarea(attrs={'placeholder': 'Informaton about your family/any known personalities from your family'})) 

    dob = forms.DateTimeField(
                label="Date & Time of Birth", 
                input_formats=settings.DATETIME_INPUT_FORMATS,
                required=True,
                widget=forms.widgets.DateTimeInput(format="%d-%b-%Y %H:%M"))

    #dob = forms.DateTimeField(
    #            label="Date & Time of Birth",
    #            input_formats=settings.DATETIME_INPUT_FORMATS,
    #            required=True,
    #            widget=DateTimePicker(options={"format": "DD-MMM-YYYY HH:mm",
    #                                   "pickSeconds": False, "pickTime": True, "ignoreReadonly": True}))

    class Meta:         
        model = Person
        fields = ('first_name', 'last_name', 'nick_name', 'family_name', 'father_name', 
                    'mother_name', 'gothram','star', 'gender', 'blood_group', 'dob', 'relation', 
                    'email', 'alternate_email', 'primary_phone', 'secondary_phone1', 'extra_info',)

    def __init__(self, *args, **kwargs):
        initial = kwargs.pop('initial', None)
        if initial is not None:
            self.contact_id = initial.pop('contact_id', None)
            self.user = initial.pop('person', None)
        super(PersonForm, self).__init__(*args, **kwargs)
        self.fields["email"].initial = self.user.username

        self.helper = FormHelper(self)
        self.helper.form_tag = False

    def clean(self):
        form_data = self.cleaned_data
        email = form_data.get('email', '')
        try:
            person = Person.objects.get(email=email)
            if self.contact_id is not None and person.id == int(self.contact_id):
                return form_data
            elif person.user == self.user:
                return form_data
            else:
                raise ValidationError('Primary Email ' + email + ' is already registered by ' + person.user.username + ' for contact: ' + person.first_name + ' ' + person.last_name)
        except Person.DoesNotExist:
            return form_data
        except MultipleObjectsReturned:
            persons = Person.objects.filter(email=email)
            for person in persons:
                if person.user == self.user:
                    continue
                elif self.contact_id is not None and person.id == int(self.contact_id):
                    continue
                else:
                    raise ValidationError('Primary Email ' + email + ' is already registered by ' + person.user.username + ' for contact: ' + person.first_name + ' ' + person.last_name)
            return form_data
                    


class ContactForm(ModelForm):
    COUNTRY_CHOICES = (
        ("Scountry","Select Country"),
        ('AF','Afghanistan'),
        ('AX','Aland Islands'),
        ('AL','Albania'),
        ('DZ','Algeria'),
        ('AS','American Samoa'),
        ('AD','Andorra'),
        ('AO','Angola'),
        ('AI','Anguilla'),
        ('AQ','Antarctica'),
        ('AG','Antigua and Barbuda'),
        ('AR','Argentina'),
        ('AM','Armenia'),
        ('AW','Aruba'),
        ('AU','Australia'),
        ('AT','Austria'),
        ('AZ','Azerbaijan'),
        ('BS','Bahamas'),
        ('BH','Bahrain'),
        ('BD','Bangladesh'),
        ('BB','Barbados'),
        ('BY','Belarus'),
        ('BE','Belgium'),
        ('BZ','Belize'),
        ('BJ','Benin'),
        ('BM','Bermuda'),
        ('BT','Bhutan'),
        ('BO','Bolivia, Plurinational State of'),
        ('BQ','Bonaire, Sint Eustatius and Saba'),
        ('BA','Bosnia and Herzegovina'),
        ('BW','Botswana'),
        ('BV','Bouvet Island'),
        ('BR','Brazil'),
        ('IO','British Indian Ocean Territory'),
        ('BN','Brunei Darussalam'),
        ('BG','Bulgaria'),
        ('BF','Burkina Faso'),
        ('BI','Burundi'),
        ('KH','Cambodia'),
        ('CM','Cameroon'),
        ('CA','Canada'),
        ('CV','Cape Verde'),
        ('KY','Cayman Islands'),
        ('CF','Central African Republic'),
        ('TD','Chad'),
        ('CL','Chile'),
        ('CN','China'),
        ('CX','Christmas Island'),
        ('CC','Cocos (Keeling) Islands'),
        ('CO','Colombia'),
        ('KM','Comoros'),
        ('CG','Congo'),
        ('CD','Congo, the Democratic Republic of the'),
        ('CK','Cook Islands'),
        ('CR','Costa Rica'),
        ('CI','Côte d&apos;Ivoire'),
        ('HR','Croatia'),
        ('CU','Cuba'),
        ('CW','Curaçao'),
        ('CY','Cyprus'),
        ('CZ','Czech Republic'),
        ('DK','Denmark'),
        ('DJ','Djibouti'),
        ('DM','Dominica'),
        ('DO','Dominican Republic'),
        ('EC','Ecuador'),
        ('EG','Egypt'),
        ('SV','El Salvador'),
        ('GQ','Equatorial Guinea'),
        ('ER','Eritrea'),
        ('EE','Estonia'),
        ('ET','Ethiopia'),
        ('FK','Falkland Islands (Malvinas)'),
        ('FO','Faroe Islands'),
        ('FJ','Fiji'),
        ('FI','Finland'),
        ('FR','France'),
        ('GF','French Guiana'),
        ('PF','French Polynesia'),
        ('TF','French Southern Territories'),
        ('GA','Gabon'),
        ('GM','Gambia'),
        ('GE','Georgia'),
        ('DE','Germany'),
        ('GH','Ghana'),
        ('GI','Gibraltar'),
        ('GR','Greece'),
        ('GL','Greenland'),
        ('GD','Grenada'),
        ('GP','Guadeloupe'),
        ('GU','Guam'),
        ('GT','Guatemala'),
        ('GG','Guernsey'),
        ('GN','Guinea'),
        ('GW','Guinea-Bissau'),
        ('GY','Guyana'),
        ('HT','Haiti'),
        ('HM','Heard Island and McDonald Islands'),
        ('VA','Holy See (Vatican City State)'),
        ('HN','Honduras'),
        ('HK','Hong Kong'),
        ('HU','Hungary'),
        ('IS','Iceland'),
        ('IN','India'),
        ('ID','Indonesia'),
        ('IR','Iran, Islamic Republic of'),
        ('IQ','Iraq'),
        ('IE','Ireland'),
        ('IM','Isle of Man'),
        ('IL','Israel'),
        ('IT','Italy'),
        ('JM','Jamaica'),
        ('JP','Japan'),
        ('JE','Jersey'),
        ('JO','Jordan'),
        ('KZ','Kazakhstan'),
        ('KE','Kenya'),
        ('KI','Kiribati'),
        ('KP','Korea, Democratic People&apos;s Republic of'),
        ('KR','Korea, Republic of'),
        ('KW','Kuwait'),
        ('KG','Kyrgyzstan'),
        ('LA','Lao People&apos;s Democratic Republic'),
        ('LV','Latvia'),
        ('LB','Lebanon'),
        ('LS','Lesotho'),
        ('LR','Liberia'),
        ('LY','Libya'),
        ('LI','Liechtenstein'),
        ('LT','Lithuania'),
        ('LU','Luxembourg'),
        ('MO','Macao'),
        ('MK','Macedonia, the former Yugoslav Republic of'),
        ('MG','Madagascar'),
        ('MW','Malawi'),
        ('MY','Malaysia'),
        ('MV','Maldives'),
        ('ML','Mali'),
        ('MT','Malta'),
        ('MH','Marshall Islands'),
        ('MQ','Martinique'),
        ('MR','Mauritania'),
        ('MU','Mauritius'),
        ('YT','Mayotte'),
        ('MX','Mexico'),
        ('FM','Micronesia, Federated States of'),
        ('MD','Moldova, Republic of'),
        ('MC','Monaco'),
        ('MN','Mongolia'),
        ('ME','Montenegro'),
        ('MS','Montserrat'),
        ('MA','Morocco'),
        ('MZ','Mozambique'),
        ('MM','Myanmar'),
        ('NA','Namibia'),
        ('NR','Nauru'),
        ('NP','Nepal'),
        ('NL','Netherlands'),
        ('NC','New Caledonia'),
        ('NZ','New Zealand'),
        ('NI','Nicaragua'),
        ('NE','Niger'),
        ('NG','Nigeria'),
        ('NU','Niue'),
        ('NF','Norfolk Island'),
        ('MP','Northern Mariana Islands'),
        ('NO','Norway'),
        ('OM','Oman'),
        ('PK','Pakistan'),
        ('PW','Palau'),
        ('PS','Palestinian Territory, Occupied'),
        ('PA','Panama'),
        ('PG','Papua New Guinea'),
        ('PY','Paraguay'),
        ('PE','Peru'),
        ('PH','Philippines'),
        ('PN','Pitcairn'),
        ('PL','Poland'),
        ('PT','Portugal'),
        ('PR','Puerto Rico'),
        ('QA','Qatar'),
        ('RE','Réunion'),
        ('RO','Romania'),
        ('RU','Russian Federation'),
        ('RW','Rwanda'),
        ('BL','Saint Barthélemy'),
        ('SH','Saint Helena, Ascension and Tristan da Cunha'),
        ('KN','Saint Kitts and Nevis'),
        ('LC','Saint Lucia'),
        ('MF','Saint Martin (French part)'),
        ('PM','Saint Pierre and Miquelon'),
        ('VC','Saint Vincent and the Grenadines'),
        ('WS','Samoa'),
        ('SM','San Marino'),
        ('ST','Sao Tome and Principe'),
        ('SA','Saudi Arabia'),
        ('SN','Senegal'),
        ('RS','Serbia'),
        ('SC','Seychelles'),
        ('SL','Sierra Leone'),
        ('SG','Singapore'),
        ('SX','Sint Maarten (Dutch part)'),
        ('SK','Slovakia'),
        ('SI','Slovenia'),
        ('SB','Solomon Islands'),
        ('SO','Somalia'),
        ('ZA','South Africa'),
        ('GS','South Georgia and the South Sandwich Islands'),
        ('SS','South Sudan'),
        ('ES','Spain'),
        ('LK','Sri Lanka'),
        ('SD','Sudan'),
        ('SR','Suriname'),
        ('SJ','Svalbard and Jan Mayen'),
        ('SZ','Swaziland'),
        ('SE','Sweden'),
        ('CH','Switzerland'),
        ('SY','Syrian Arab Republic'),
        ('TW','Taiwan, Province of China'),
        ('TJ','Tajikistan'),
        ('TZ','Tanzania, United Republic of'),
        ('TH','Thailand'),
        ('TL','Timor-Leste'),
        ('TG','Togo'),
        ('TK','Tokelau'),
        ('TO','Tonga'),
        ('TT','Trinidad and Tobago'),
        ('TN','Tunisia'),
        ('TR','Turkey'),
        ('TM','Turkmenistan'),
        ('TC','Turks and Caicos Islands'),
        ('TV','Tuvalu'),
        ('UG','Uganda'),
        ('UA','Ukraine'),
        ('AE','United Arab Emirates'),
        ('GB','United Kingdom'),
        ('US','United States'),
        ('UM','United States Minor Outlying Islands'),
        ('UY','Uruguay'),
        ('UZ','Uzbekistan'),
        ('VU','Vanuatu'),
        ('VE','Venezuela, Bolivarian Republic of'),
        ('VN','Viet Nam'),
        ('VG','Virgin Islands, British'),
        ('VI','Virgin Islands, U.S.'),
        ('WF','Wallis and Futuna'),
        ('EH','Western Sahara'),
        ('YE','Yemen'),
        ('ZM','Zambia'),
        ('ZW','Zimbabwe'),
    )

    address = forms.ModelChoiceField(required=False, queryset=Contact.objects.none(), label="Choose a current address", widget=forms.Select(attrs={'onchange':'fill_address_form();'}))
    address1 = forms.CharField(required=True, label="Address Line 1", widget=forms.TextInput(attrs={'placeholder': 'Street address, P.O. box'}))
    address2 = forms.CharField(required=False, label="Address Line 2", widget=forms.TextInput(attrs={'placeholder': 'Flat No/Block No'}))
    address3 = forms.CharField(required=False, label="Address Line 3", widget=forms.TextInput(attrs={'placeholder': 'Building, floor, etc'}))
    address4 = forms.CharField(required=False, label="Address Line 4", widget=forms.TextInput(attrs={'placeholder': 'Landmark'}))
    city = forms.CharField(required=True, label="City/Town", widget=forms.TextInput(attrs={'placeholder': 'City'}))
    state = forms.CharField(required=True, label="State", widget=forms.TextInput(attrs={'placeholder': 'State'}))
    zipcode = forms.CharField(required=True, label="Postal/Zip/Pin Code", widget=forms.TextInput(attrs={'placeholder': 'Postal Code or Zip Code or Pin Code'}))
    country = forms.ChoiceField(choices = COUNTRY_CHOICES, required = True, label = 'Country')

    class Meta:
        model = Contact
        fields = ('address', 'address1', 'address2', 'address3', 'address4', 'city', 'state', 'zipcode', 'country',)

    def __init__(self, *args, **kwargs):
        initial = kwargs.pop('initial', None)
        super(ContactForm, self).__init__(*args, **kwargs)

        if initial is not None:
            person = initial.pop('person', None)
            #print(person)
            self.fields["address"].queryset = Contact.objects.filter(user=person)
        else:
            self.fields["address"].queryset = Contact.objects.all()

        self.helper = FormHelper(self)
        self.helper.form_tag = False

    def clean(self):
        if self.cleaned_data.get('address') and 'country' in self._errors:
            del self._errors['country']
        return self.cleaned_data 

ContactAddressFormSet = inlineformset_factory(Contact, Person,
        extra=0, min_num=1, fields=('first_name', 'last_name', 'nick_name',
        'family_name', 'gothram', 'star', 'gender', 'blood_group', 'dob',
        'email', 'primary_phone', 'secondary_phone1', 'secondary_phone2',
        'extra_info',) )