from admin_interface.forms import CourseForm
from admin_interface.forms import DeadlineForm
from admin_interface.forms import FeedbackForm
from admin_interface.forms import QuestionForm
from admin_interface.forms import UserForm
from admin_interface.models import Course
from admin_interface.models import Deadline
from admin_interface.models import Feedback
from admin_interface.models import Instructor
from admin_interface.models import Question
from admin_interface.models import Student
from admin_interface.models import Objectiveanswer

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.forms.formsets import formset_factory
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers


@csrf_exempt
def student_login(request):
	valid = False
	error = ""
	name = ""
	if request.method == 'POST':
		rollno = request.POST['rollno']
		password = request.POST['password']
		if Student.objects.filter(pk=rollno).count() > 0:
			student = Student.objects.get(pk=rollno)
			if student.password == password:
				valid = True
				name = student.name
			else:
				error = "Invalid credentials"
		else:
			error = "Account does not exist"
	else:
		error = "Invalid request"

	return JsonResponse(
		{
			'valid': valid,
			'name': name,
			'error': error,
		})

@csrf_exempt
def student_deadlines(request):
	deadlines = []
	if request.method == 'POST':

		objs = Deadline.objects.all()

		if 'date' in request.POST:
			date = request.POST['date']
			objs = Deadline.objects.filter(submission_date=date)
		
		for obj in objs:
			deadline = {
				'course': obj.course.code,
				'assignment': obj.assignment,
				'is_feedback': obj.is_feedback,
				'submission_date': obj.submission_date,
				'submission_time': obj.submission_time,
				'feedback_id': None,
			}
			if hasattr(obj, 'feedback'):
				deadline['feedback_id'] = obj.feedback.id

			deadlines.append(deadline)

	return JsonResponse({
			'deadlines': deadlines,
		})

@csrf_exempt
def student_courses(request):
	courses = []
	error = ""
	if request.method == 'POST':
		if 'rollno' in request.POST:
			rollno = request.POST['rollno']
			if Student.objects.filter(pk=rollno).count() > 0:
				objs = Student.objects.get(pk=rollno).course_set.all()
				for course in objs:
					courses.append({
							'code': course.code,
							'name': course.name,
						})
			else:
				error = "Student does not exists"
		else:
			error = "Invalid request"

	return JsonResponse({
			'courses': courses,
			'error': error,
		})

@csrf_exempt
def student_feedback(request):
	response = {}
	if request.method == 'POST':
		feedback_id = int(request.POST['id'])
		if Feedback.objects.filter(pk=feedback_id).count() > 0:
			feedback = Feedback.objects.get(pk=feedback_id)
			response['course'] = feedback.course.code
			response['title'] = feedback.title;
			response['description'] = feedback.description
			questions = []
			for q in feedback.questions.all():
				question = {
					'question': q.question,
					'question_id': q.id,
					'a': q.a,
					'b': q.b,
					'c': q.c,
					'd': q.d,
					'e': q.e,
				}
				questions.append(question)
			response['questions'] = questions
	return JsonResponse(response)

@csrf_exempt
def student_feedback_submit(request):
	response = ""
	if request.method == 'POST':
		question_id = int(request.POST['id'])
		answer = int(request.POST['option'])
		if answer != -1:
			if Question.objects.filter(pk=question_id).count() > 0:
				ans = Question.objects.get(pk=question_id).objectiveanswer
				if answer == 1:
					ans.count_a += 1
				elif answer == 2:
					ans.count_b += 1
				elif answer == 3:
					ans.count_c += 1
				elif answer == 4:
					ans.count_d += 1
				elif answer == 5:
					ans.count_e += 1
				ans.save()
				response = "Marked " + str(answer) + " for question " + str(question_id)
			else:
				response = "Question does not exists"
		else:
			response = "Answer not marked for question " + str(question_id)
	return JsonResponse({
			'response': response, 
		})



def index(request):

	authenticated = False

	if request.user.is_authenticated:
		authenticated = True

	context = {
		'authenticated': authenticated,
	}

	return render(request, 'index.html', context)


def google_login(request):

	logged_in = False

	if request.method == 'POST' and 'ID' in request.POST:
		email = request.POST['email']
		name = request.POST['name'].split(' ')[0]
		id = request.POST['ID']

		if Instructor.objects.filter(email=email).count() > 0:
			instructor = Instructor.objects.get(email=email)
			if instructor.google_login == True:
				# google ID is the password for google_login user
				user = authenticate(username=email, password=id)
				if user:
					if user.is_active:
						login(request, user)
						logged_in = True
					else:
						error = "Your account is disabled"
				else:
					error = "Invalid credentials"
		
		else:
			print('new google user')

			user = User()
			user.username = email
			user.email = email
			user.set_password(id)
			user.save()

			new_instructor = Instructor(
				user=user,
				email=email,
				google_login=True)
			new_instructor.save()
			# google ID is the password for google_login user
			user = authenticate(username=email, password=id)
			if user:
				if user.is_active:
					login(request, user)
					logged_in = True
				else:
					error = "Your account is disabled"
			else:
				error = "Invalid credentials"

	print("here " + str(logged_in))
	return render(request, 'google-login.html', {'logged_in': logged_in})

def user_login(request):

	error = ""

	if request.method == 'POST':

		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)
		if user:

			if (Instructor.objects.get(email=user.email)).google_login:
				print(Instructor.objects.get(email=user.email).google_login)
				error = "This account already has a social login"
				context = {'error_msg': error,}
				return render(request, 'login.html', context)

			elif user.is_active:

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

	registered = False
	error_passwd = ""
	error_email = ""

	if request.method == 'POST':

		user_form = UserForm(data=request.POST)

		if (not user_form.is_valid()):
			print(user_form.errors)

		if (user_form.is_valid() and user_form.data['password'] == request.POST.get('confirm_password')):

			email = user_form.cleaned_data.get('username') 

			user = user_form.save()
			user.email = email
			user.set_password(user.password)
			user.save()

			profile = Instructor()
			profile.user = user
			profile.email = user.email
			profile.save()

			registered = True

		
		elif (user_form.data['password'] != request.POST.get('confirm_password')):
			error_passwd = "passwords do not match"


	else:
		user_form = UserForm()

	context = {
		'user_form': user_form,
		'registered': registered,
		'error_passwd': error_passwd,
		'error_email': error_email,
	}

	return render(request, 'register.html', context)


def home(request):

	if request.user.is_authenticated:

		if Instructor.objects.filter(user=request.user).count() > 0:
			instrctor = Instructor.objects.get(user=request.user)
			is_special = instrctor.special_admin

			context = {
				'is_special': is_special,
			}

			return render(request, 'home.html', context)

	return render(request, 'permission-denied.html', {})


'''
	view functions for special admin
'''
# creates the default midsem and endsem feedbacks
def createFeedbacks(course_code, midsem_date, midsem_time, endsem_date, endsem_time):
	course = Course.objects.get(pk=course_code)

	# midsem deadline
	midsem_deadline = Deadline(
		course=course,
		assignment='Mid-semester Feedback',
		submission_date=midsem_date,
		submission_time=midsem_time,
		is_feedback=True)
	midsem_deadline.save()

	# midsem deadline
	endsem_deadline = Deadline(
		course=course,
		assignment='End-semester Feedback',
		submission_date=endsem_date,
		submission_time=endsem_time,
		is_feedback=True)
	endsem_deadline.save()

	# Midsem feedback
	question1 = Question(
		question="This course as a whole so far has been",
		a='Poor',
		b='Fair',
		c='Good',
		d='Very Good',
		e='Excellent')
	question1.save()
	answer = Objectiveanswer(question=question1)
	answer.save()

	question2 = Question(
		question="Feedback on course content",
		a='Difficult',
		b='Well-designed',
		c='Poorly graded',
		d='Learning experience',
		e='Just right')
	question2.save()
	answer = Objectiveanswer(question=question2)
	answer.save()

	midsem_feedback = Feedback(
		course=course,
		title="Mid-semester Feedback",
		description="",
		deadline=midsem_deadline)
	midsem_feedback.save()
	midsem_feedback.questions.add(question1)
	midsem_feedback.questions.add(question2)

	# endsem feedback
	question3 = Question(
		question="This course as a whole so far has been",
		a='Poor',
		b='Fair',
		c='Good',
		d='Very Good',
		e='Excellent')
	question3.save()
	answer = Objectiveanswer(question=question3)
	answer.save()

	question4 = Question(
		question="Feedback on course content",
		a='Difficult',
		b='Well-designed',
		c='Poorly graded',
		d='Learning experience',
		e='Just right')
	question4.save()
	answer = Objectiveanswer(question=question4)
	answer.save()

	endsem_feedback = Feedback(
		course=course,
		title="End-semester Feedback",
		description="",
		deadline=endsem_deadline)
	endsem_feedback.save()
	endsem_feedback.questions.add(question1)
	endsem_feedback.questions.add(question2)


def add_course(request):

	# only special admin can access this feature (adding course)
	if request.user.is_authenticated and Instructor.objects.get(user=request.user).special_admin:

		if request.method == 'POST':

			course_form = CourseForm(data=request.POST)

			if course_form.is_valid():

				course_form.save(commit=False)

				course = Course()
				course.name = course_form.cleaned_data.get('name')
				course.code = course_form.cleaned_data.get('code')
				course.save()

				midsem_date = course_form.cleaned_data.get('midsem_date')
				endsem_date = course_form.cleaned_data.get('endsem_date')
				midsem_time = course_form.cleaned_data.get('midsem_time')
				endsem_time = course_form.cleaned_data.get('endsem_time')


				createFeedbacks(course.code, midsem_date, midsem_time, endsem_date, endsem_time)

				return redirect('home')

			else:
				print("invalid")
				context = {
					'form': course_form,
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


def newfeedback(request, course_code):

	if request.user.is_authenticated:

		QFormSet = formset_factory(QuestionForm)
		errors = ""

		if request.method == 'POST':
			
			feedback_form = FeedbackForm(request.POST)
			question_formset = QFormSet(request.POST)

			if feedback_form.is_valid() and question_formset.is_valid():

				course = Course.objects.get(pk=course_code)

				title = feedback_form.cleaned_data.get('title')
				description = feedback_form.cleaned_data.get('description')
				submission_date = feedback_form.cleaned_data.get('submission_date')
				submission_time = feedback_form.cleaned_data.get('submission_time')

				new_deadline = Deadline(
					course=course,
					assignment=title,
					submission_date=submission_date,
					submission_time=submission_time,
					is_feedback=True)
				new_deadline.save()

				new_feedback = Feedback(
							title=title,
							description=description,
							course=course,
							deadline=new_deadline)
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
					answer = Objectiveanswer(question=new_question)
					answer.save()
					new_feedback.questions.add(new_question)

			else:
				print("validation error - feedback form")
				context = {
					'errors': errors,
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

		running_deadlines = []
		past_deadlines = []

		deadlines = Deadline.objects.all().order_by('submission_date', 'submission_time')

		for deadline in deadlines:
			if deadline.is_past_due():
				past_deadlines.append(deadline)
			else:
				running_deadlines.append(deadline)

		context = {
			'deadlines': deadlines,
			'past_deadlines': past_deadlines,
			'running_deadlines': running_deadlines,
		}
		return render(request, 'viewdeadlines.html', context)

	else:
		return redirect('login')
















