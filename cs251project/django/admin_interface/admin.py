from django.contrib import admin
from admin_interface.models import Instructor, Student, Course, Feedback, Question, Objectiveanswer, Deadline

class InstructorAdmin(admin.ModelAdmin):
	list_display = ['user', 'special_admin', 'google_login']

class StudentAdmin(admin.ModelAdmin):
	list_display = ['name', 'rollno'];

class CourseAdmin(admin.ModelAdmin):
	list_display = ['name', 'code']

class DeadlineAdmin(admin.ModelAdmin):
	list_display = ['assignment', 'course', 'submission_date', 'submission_time']

admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Feedback)
admin.site.register(Question)
admin.site.register(Objectiveanswer)
admin.site.register(Deadline, DeadlineAdmin)
