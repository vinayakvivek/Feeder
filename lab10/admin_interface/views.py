from django.shortcuts import render
from django.contrib.auth.models import User
from admin_interface.models import Instructor
from admin_interface.forms import UserForm


def index(request):
	return render(request, 'index.html', {})

def user_login(request):
	return render(request, 'login.html', {})

def register(request):
	registered = False

	if request.method == 'POST':

		user_form = UserForm(data=request.POST)

		if user_form.is_valid():

			user = user_form.save()

			user.set_password(user.password)
			user.save()

			profile = Instructor()
			profile.user = user
			profile.save()

			registered = True

		else:
			print(user_form.errors)
	
	else:
		user_form = UserForm()

	context = {
		'user_form': user_form,
	}

	return render(request, 'register.html', context)