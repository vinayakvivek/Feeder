from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from admin_interface.models import Instructor, Course, Student, Feedback, Question
from admin_interface.forms import UserForm, CourseForm, FeedbackForm, QuestionForm

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.forms.formsets import formset_factory


def index(request):
	return render(request, 'index.html', {})


def user_login(request):

	error = ""

	if request.method == 'POST':

		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)

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

	else:

		return render(request, 'permission-denied.html', {})


'''
	view functions for special admin
'''
def add_course(request):

	error = ""

	if request.user.is_authenticated and Instructor.objects.get(user=request.user).special_admin:

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

			if Instructor.objects.filter(user=request.user).count() > 0:
				
				instrctor = Instructor.objects.get(user=request.user)
				if (instrctor.special_admin):

					form = CourseForm()
					context = {
						'form': form,
					}
					return render(request, 'addcourse.html', context)

	else:
		
		return render(request, 'permission-denied.html', {})


def view_courses(request):

	if request.user.is_authenticated and Instructor.objects.get(user=request.user).special_admin:

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

		return render(request, 'permission-denied.html', {})


def course_detail(request, course_code):

	if request.user.is_authenticated and Instructor.objects.get(user=request.user).special_admin:
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
		return render(request, 'permission-denied.html', {})	
	

def enroll(request):

	if request.user.is_authenticated and Instructor.objects.get(user=request.user).special_admin:

		if request.method == 'POST':

			if 'enroll' in request.POST:
				course_code = request.POST['code']
				course = Course.objects.get(pk=course_code)
				# key == rollno
				for key in request.POST:
					if (request.POST[key] == 'on'):
						print(key)
						student = Student.objects.get(pk=key)
						course.students.add(student)

			elif 'dismiss' in request.POST:
				course_code = request.POST['course_code']
				student = request.POST['student']
				# return HttpResponse(str(Student.objects.get(pk=student)))
				Student.objects.get(pk=student).course_set.remove(course_code)
				return redirect('viewcourses')

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
		return render(request, 'permission-denied.html', {})


'''
	view functions for any instructor
'''
def addfeedback(request):

	if request.user.is_authenticated:
		
		if request.method == 'POST' and 'course_code' in request.POST:

			course_code = request.POST['course_code']

		else:
			courses = Course.objects.all()
			context = {
				'courses': courses,
			}
			return render(request, 'addfeedback.html', context)

	else:
		return redirect('login')


def feedback(request, course_code):

	if request.user.is_authenticated:

		QFormSet = formset_factory(QuestionForm)

		if request.method == 'POST':
			
			feedback_form = FeedbackForm(request.POST)
			question_formset = QFormSet(request.POST)

			if feedback_form.is_valid() and question_formset.is_valid():

				title = feedback_form.cleaned_data.get('title')
				description = feedback_form.cleaned_data.get('description')
				new_feedback = Feedback(title=title, description=description)
				new_feedback.save()

				for qform in question_formset:
					question = qform.cleaned_data.get('question')
					a = qform.cleaned_data.get('a')
					b = qform.cleaned_data.get('b')
					c = qform.cleaned_data.get('c')
					d = qform.cleaned_data.get('d')
					e = qform.cleaned_data.get('e')

					new_question = Question(question=question, a=a, b=b, c=c, d=d, e=e)
					new_question.save()

					new_feedback.questions.add(new_question)

			else:
				# TODO
				return HttpResponse("errors in form")


		else:
			form = FeedbackForm()
			# qform = QuestionForm()
			qformset = QFormSet()
			context = {
				'form': form,
				'qformset': qformset,
				'course_code': course_code,
			}
			return render(request, 'feedback-form.html', context)

		return HttpResponse("New feedback in " + str(course_code))
	else:
		return redirect('login')















