from django.views.generic import ListView
from django.contrib.auth.models import User

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
