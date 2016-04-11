from django.views.generic import ListView
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

class UserReportView(ListView):
	template_name = 'addressdb/user/user_report.html'
	model = User

	def get_queryset(self):
		qs = User.objects.all()
		return qs

class IncompleteRegistrationReportView(ListView):
	template_name = 'addressdb/user/incomplete_report.html'


	def get_queryset(self):
		qs = User.objects.raw('select * from auth_user where id not in (select user_id from addressdb_person)')
		return list(qs)

@login_required
def send_email_incomplete_reg(request):
	qs = User.objects.raw('select * from auth_user where id not in (select user_id from addressdb_person)')
	list_users = list(qs)
	if len(list_users) < 1:
		return HttpResponse('No incomplete registration users found. Hence email was not sent.')
	else:
		recipients = list()
		for user in list_users:
			email = user.username
			recipients.insert(0, email)
		print(recipients)
		send_mail('Incomplete Registration - www.nuranians.com', 
			'Hi, You have not completed your registration in nuranians.com. Please login using your email id and password and enter your contact informaton for self and family members',
			'nuranivillage@gmail.com',
			recipients,
			fail_silently=False
			)
		return HttpResponse('Email was sent successfully')

