from django.contrib import admin
from admin_interface.models import Instructor, Student, Course

class InstructorAdmin(admin.ModelAdmin):
	list_display = ['user', 'special_admin', 'google_fb_login']

class StudentAdmin(admin.ModelAdmin):
	list_display = ['name', 'rollno'];

class CourseAdmin(admin.ModelAdmin):
	list_display = ['name', 'code']

admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Course, CourseAdmin)

