from django.db import models
from django.contrib.auth.models import User

class Contact(models.Model):
	address1 = models.CharField(max_length=300)
	address2 = models.CharField(max_length=300, blank=True, null=True)
	address3 = models.CharField(max_length=300, blank=True, null=True)
	address4 = models.CharField(max_length=300, blank=True, null=True)
	city = models.CharField(max_length=100)
	state = models.CharField(max_length=100)
	country = models.CharField(max_length=100, blank=True)
	zipcode = models.CharField(max_length=20)
	user = models.ForeignKey(User)

	def __str__(self): 
		return self.address1 + "," + self.address2 + ',' + self.address3 + ',' + self.address4 + ',' + self.city + ',' + self.state + '-' + self.zipcode + ',' + self.country


class Person(models.Model):
	first_name = models.CharField(max_length=60)
	last_name = models.CharField(max_length=60)
	nick_name = models.CharField(max_length=60, blank=True, null=True)
	family_name = models.CharField(max_length=60, blank=True, null=True)
	father_name = models.CharField(max_length=60, blank=True, null=True)
	mother_name = models.CharField(max_length=60, blank=True, null=True)
	gothram = models.CharField(max_length=60)
	star = models.CharField(max_length=60)
	gender = models.CharField(max_length=10)
	blood_group = models.CharField(max_length=6)
	dob = models.DateTimeField('Date and Time of Birth')
	email = models.EmailField(max_length=50)
	alternate_email = models.EmailField(max_length=50)
	primary_phone = models.CharField(max_length=20)
	secondary_phone1 = models.CharField(max_length=20, blank=True, null=True)
	secondary_phone2 = models.CharField(max_length=20, blank=True, null=True)
	extra_info = models.CharField(max_length=1000, blank=True, null=True)	
	address = models.ForeignKey(Contact)
	user = models.ForeignKey(User)

	def __str__(self):
		return self.first_name + ' ' + self.last_name

