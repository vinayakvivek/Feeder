from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from admin_interface.models import Instructor, Course, Student
from admin_interface.forms import UserForm, CourseForm

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse


def index(request):
	return render(request, 'index.html', {})


def user_login(request):

	error = ""

	if request.method == 'POST':

		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)

		# print(username, password)

		if user:

			if user.is_active:

				print(username, password)
				login(request, user)
				return redirect('home')

			else:
				error = "Your account is disabled"

		else:
			error = "Invalid credentials"

	else:
		error = ""

	context = {
		'error_msg': error,
	}

	return render(request, 'login.html', context)


def user_logout(request):
	logout(request)
	return redirect('index')


def register(request):

	if request.user.is_authenticated:
		return redirect('index')

	registered = False
	error = ""

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
			return redirect('login')

		else:
			error = str(user_form.errors)
	
	else:
		user_form = UserForm()

	context = {
		'user_form': user_form,
		'registered': registered,
		'error_msg': error,
	}

	return render(request, 'register.html', context)


def home(request):

	if request.user.is_authenticated:

		if Instructor.objects.filter(user=request.user).count() > 0:
			instrctor = Instructor.objects.get(user=request.user)
			is_special = instrctor.special_admin

			print(Course.objects.get(code='CS207').students.all())

			context = {
				'is_special': is_special,
			}

			return render(request, 'home.html', context)

	return redirect('login')


def add_course(request):

	error = ""

	if request.method == 'POST':

		course_form = CourseForm(data=request.POST)

		if course_form.is_valid():

			course_form.save(commit=False)

			course = Course()
			course.name = course_form.cleaned_data.get('name')
			course.code = course_form.cleaned_data.get('code')
			course.save()

			return redirect('home')

		else:
			error = str(course_form.errors)
			context = {
				'form': course_form,
				'error_msg': error,
			}
			return render(request, 'addcourse.html', context)

	else:

		if request.user.is_authenticated:
			if Instructor.objects.filter(user=request.user).count() > 0:
				
				instrctor = Instructor.objects.get(user=request.user)
				if (instrctor.special_admin):

					form = CourseForm()
					context = {
						'form': form,
					}
					return render(request, 'addcourse.html', context)

		return HttpResponse("You don't have access to this!")

























