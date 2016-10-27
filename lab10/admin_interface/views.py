from django.shortcuts import render, redirect, get_object_or_404
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

			print(Student.objects.get(rollno='150050099').course_set.all())

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


# def remove_course(request):

# 	if request.method == 'POST':
# 		course_code = request.POST['course_code']
# 		Course.objects.filter(pk=course_code).delete()

def view_courses(request):

	if request.user.is_authenticated:

		# true when 'remove' button is clicked
		if request.method == 'POST':
			course_code = request.POST['course_code']
			Course.objects.filter(pk=course_code).delete()
		
		courses = Course.objects.all()

		context = {
			'courses': courses,
		}

		return render(request, 'viewcourses.html', context)
				
	else:

		return redirect('login')

def course_detail(request, course_code):

	if request.user.is_authenticated:
		course = get_object_or_404(Course, pk=course_code)

		students = course.students.all()
		course_name = course.name
		# print(students)

		context = {
			'course_name': course_name,
			'students': students,
			'course_code': course_code,
		}

		return render(request, 'course-detail.html', context)

	else:
		return redirect('login')	
	

def enroll(request):

	if request.user.is_authenticated:

		if request.method == 'POST':

			if 'enroll' in request.POST:
				course_code = request.POST['code']
				course = Course.objects.get(pk=course_code)
				for key in request.POST:
					if (request.POST[key] == 'on'):
						print(key)
						student = Student.objects.get(pk=key)
						course.students.add(student)

			else:
				course_code = request.POST['course_code']

				students_list = []

				students = Student.objects.all()
				for student in students:
					if student.course_set.filter(code=course_code).count() == 0:
						students_list.append(student)

				context = {
					'students': students_list,
					'course_code': course_code,
				}

				return render(request, 'enroll.html', context)

		return redirect('viewcourses')

	else :

		return redirect('login')


















