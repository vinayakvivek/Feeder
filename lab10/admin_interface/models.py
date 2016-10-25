from django.db import models
from django.contrib.auth.models import User

# model for instructor
class Instructor(models.Model):
	# storing data of user
	# user.username is just the email address but user.email is left blank
	user = models.OneToOneField(User)
	
	# storing whether special_admin and gmail or fb signup or normal signup
	special_admin = models.BooleanField()
	gmail_fb_login = models.BooleanField()

	def __str__(self):
		return self.user.username

