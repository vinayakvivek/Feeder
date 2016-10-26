from django.db import models
from django.contrib.auth.models import User


# model for instructor
class Instructor(models.Model):
	# storing data of user
	# user.username is just the email address but user.email is left blank
	user = models.OneToOneField(User)
	
	# storing whether special_admin and google or fb signup or normal signup
	special_admin = models.BooleanField(default=False)
	google_fb_login = models.BooleanField(default=False)

	def __str__(self):
		return self.user.username


# model for students
class Student(models.Model):
	name = models.CharField(max_length=100)
	rollno = models.CharField(max_length=15, primary_key=True)

	def __str__(self):
		return self.name


# model for courses
class Course(models.Model):
	name = models.CharField(max_length=100)
	code = models.CharField(max_length=100, primary_key=True)
	students = models.ManyToManyField(Student)

	def __str__(self):
		return self.code
