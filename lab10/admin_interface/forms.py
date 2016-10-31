from admin_interface.models import Course
from admin_interface.models import Deadline
from admin_interface.models import Feedback
from admin_interface.models import Instructor
from admin_interface.models import Question
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.forms import Textarea
from django.forms.formsets import BaseFormSet
from django.utils import timezone

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password')

class CourseForm(forms.ModelForm):
	midsem_date = forms.DateField(input_formats=['%d %B, %Y'],
									  widget=forms.DateInput(attrs={'class': 'datepicker'}))
	endsem_date = forms.DateField(input_formats=['%d %B, %Y'],
									  widget=forms.DateInput(attrs={'class': 'datepicker'}))
	midsem_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
	endsem_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
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

	def clean_question(self):
		q = self.cleaned_data.get('question')
		if q == "":
			raise forms.ValidationError("Please dont leave any questions blank")

		return q


class DeadlineForm(forms.ModelForm):
	submission_date = forms.DateField(input_formats=['%d %B, %Y'],
									  widget=forms.DateInput(attrs={'class': 'datepicker'}))
	class Meta:
		model = Deadline
		fields = ('assignment', 'submission_date', 'submission_time')
		widgets = {
			'submission_time': forms.TimeInput(format='%H:%M'),
		}













