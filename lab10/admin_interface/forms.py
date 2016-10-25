from django import forms
from django.contrib.auth.models import User
from admin_interface.models import Instructor

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password')

