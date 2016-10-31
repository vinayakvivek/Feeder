import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','Feeder.settings')

import django
django.setup()
from admin_interface.models import Student

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

if __name__ == '__main__':
	print("Populating Student database")
	populate()









