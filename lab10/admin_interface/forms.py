from django import forms
from django.forms import Textarea
from django.forms.formsets import BaseFormSet
from django.contrib.auth.models import User
from admin_interface.models import Instructor, Course, Question, Feedback

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password')

class CourseForm(forms.ModelForm):
	class Meta:
		model = Course
		fields = ('name', 'code')


class FeedbackForm(forms.ModelForm):
	class Meta:
		model = Feedback
		fields = ('title', 'description')

class QuestionForm(forms.ModelForm):
	class Meta:
		model = Question
		fields = ('question', 'a', 'b', 'c', 'd', 'e')
		widgets = {
			'question': Textarea(attrs={
									'placeholder': "Question",
									'class': 'materialize-textarea'}),

			'a': forms.TextInput(attrs={'placeholder': 'Option 1'}),
			'b': forms.TextInput(attrs={'placeholder': 'Option 2'}),
			'c': forms.TextInput(attrs={'placeholder': 'Option 3'}),
			'd': forms.TextInput(attrs={'placeholder': 'Option 4'}),
			'e': forms.TextInput(attrs={'placeholder': 'Option 5'}),
		}

