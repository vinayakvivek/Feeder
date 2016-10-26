from django import forms
from django.contrib.auth.models import User
from admin_interface.models import Instructor, Course

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password')

class CourseForm(forms.ModelForm):
	class Meta:
		model = Course
		fields = ('name', 'code')