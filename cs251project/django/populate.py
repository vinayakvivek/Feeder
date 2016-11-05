import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','Feeder.settings')

import django
django.setup()
from admin_interface.models import Student
from admin_interface.models import Instructor
from django.contrib.auth.models import User

def populate():
	f = open('admin_interface/student_list', 'r')
	for line in f:
		line = line.rstrip('\n').split(',')
		add_student(line[0], line[1], line[2])
		print("- {0} - {1}".format(str(line[0]), str(line[1])))


def add_student(rollno, name, password):
	s = Student.objects.get_or_create(rollno=rollno)[0]
	s.name = name
	s.password = password
	s.save()


print("Populating Student database")
populate()

spl_user = User.objects.get_or_create(username="admin@feeder.com")[0]
spl_user.first_name="admin"; spl_user.last_name="special"; spl_user.email="admin@feeder.com"
spl_user.set_password("admin")
spl_user.save()

if (Instructor.objects.filter(email=spl_user.email).count() == 0):
	spl_admin = Instructor(email=spl_user.email, special_admin=True, user=spl_user)

	spl_admin.save()

non_spl_user = User.objects.get_or_create(username="instructor@feeder.com")[0]
non_spl_user.first_name = "Instructor"
non_spl_user.email="instructor@feeder.com"
non_spl_user.set_password("instructor")
non_spl_user.save()

if (Instructor.objects.filter(email=non_spl_user.email).count() == 0):
	inst = Instructor(email=non_spl_user.email, user=non_spl_user)
	inst.save()









