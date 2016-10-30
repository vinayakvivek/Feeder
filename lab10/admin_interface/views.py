from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from admin_interface.models import Instructor, Course, Student, Feedback, Question, Deadline
from admin_interface.forms import UserForm, CourseForm, FeedbackForm, QuestionForm, DeadlineForm

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.forms.formsets import formset_factory
from django.conf import settings


def index(request):

	authenticated = False

	if request.user.is_authenticated:
		authenticated = True

	context = {
		'authenticated': authenticated,
	}

	return render(request, 'index.html', context)


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
		
		courses = Course.objects.all()
		context = {
			'courses': courses,
		}
		return render(request, 'addfeedback.html', context)

	else:
		return redirect('login')


# TODO : error checking
def newfeedback(request, course_code):

	if request.user.is_authenticated:

		QFormSet = formset_factory(QuestionForm)

		if request.method == 'POST':
			
			feedback_form = FeedbackForm(request.POST)
			question_formset = QFormSet(request.POST)

			if feedback_form.is_valid() and question_formset.is_valid():

				title = feedback_form.cleaned_data.get('title')
				description = feedback_form.cleaned_data.get('description')
				new_feedback = Feedback(
							title=title,
							description=description,
							course=Course.objects.get(pk=course_code))
				new_feedback.save()

				for qform in question_formset:
					question = qform.cleaned_data.get('question')
					a = qform.cleaned_data.get('a')
					b = qform.cleaned_data.get('b')
					c = qform.cleaned_data.get('c')
					d = qform.cleaned_data.get('d')
					e = qform.cleaned_data.get('e')

					if question:
						new_question = Question(question=question, a=a, b=b, c=c, d=d, e=e)
						new_question.save()
						new_feedback.questions.add(new_question)
					else:
						errors = "Blank question"

			else:
				# TODO
				context = {
					'form': feedback_form,
					'qformset': question_formset,
					'course_code': course_code,
				}
				return render(request, 'feedback-form.html', context)


		else:
			form = FeedbackForm()
			qformset = QFormSet()
			context = {
				'form': form,
				'qformset': qformset,
				'course_code': course_code,
			}
			return render(request, 'feedback-form.html', context)

		return redirect('home')
	else:
		return redirect('login')



def viewfeedback(request):

	if request.user.is_authenticated:

		courses = Course.objects.all()
		context = {
			'courses': courses,
		}
		return render(request, 'viewfeedback.html', context)

	else:
		return redirect('login')


def coursefeedbacks(request, course_code):

	if request.user.is_authenticated:

		feedbacks = Course.objects.get(pk=course_code).feedback_set.all()

		context = {
			'feedbacks': feedbacks,
		}
		return render(request, 'course-feedbacks.html', context)

	else:
		return redirect('login')



def mark_answer(request, rollno, password, question_id, answer):
	print(rollno, password)
	return HttpResponse("You marked " + str(answer) + ", for question " + str(question_id))


def feedback_details(request, feedback_id):

	if request.user.is_authenticated:

		feedback = Feedback.objects.get(pk=feedback_id)
		questions = feedback.questions
		answers = []
		# for q in questions:
		# 	if (hasattr(q, 'objectiveanswer'))

		context = {
			'feedback': feedback,
		}
		return render(request, 'feedback-detail.html', context)

	else:
		return redirect('login')
	

def add_deadline(request):

	if request.user.is_authenticated:

		courses = Course.objects.all()
		context = {
			'courses': courses,
		}
		return render(request, 'add-deadline.html', context)

	return redirect('login')


def newdeadline(request, course_code):

	if request.user.is_authenticated:

		deadline_form = DeadlineForm()

		if request.method == 'POST':

			deadline_form = DeadlineForm(request.POST)

			if deadline_form.is_valid():
				assignment = deadline_form.cleaned_data.get('assignment')
				submission_date = deadline_form.cleaned_data.get('submission_date')
				submission_time = deadline_form.cleaned_data.get('submission_time')
				
				new_deadline = Deadline(
					course=Course.objects.get(pk=course_code),
					assignment=assignment,
					submission_time=submission_time,
					submission_date=submission_date)
				new_deadline.save()

				return redirect('home')
		
		context = {
			'form': deadline_form,
			'course_code': course_code,
		}
		return render(request, 'deadline-form.html', context)

	else:
		return redirect('login')


def viewdeadlines(request):

	if request.user.is_authenticated:

		deadlines = Deadline.objects.all().order_by('submission_date')
		context = {
			'deadlines': deadlines,
		}
		return render(request, 'viewdeadlines.html', context)

	else:
		return redirect('login')
















