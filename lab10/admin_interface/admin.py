from django.contrib import admin
from admin_interface.models import Instructor

class InstructorAdmin(admin.ModelAdmin):
	list_display = ['user', 'special_admin', 'gmail_fb_login']

admin.site.register(Instructor, InstructorAdmin)
