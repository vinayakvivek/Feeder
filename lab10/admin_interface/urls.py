from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^index/', views.index, name='index'),
	url(r'^home/', views.home, name='home'),
	url(r'^login/', views.user_login, name='login'),
	url(r'^googlelogin/', views.google_login, name='googlelogin'),
	url(r'^logout/', views.user_logout, name='logout'),
	url(r'^register/', views.register, name='register'),

	url(r'^student/login/', views.student_login, name='studentlogin'),
	url(r'^student/deadlines/', views.student_deadlines, name='studentdeadlines'),

	url(r'^addcourse/', views.add_course, name='addcourse'),
	url(r'^enroll/$', views.enroll, name='enroll'),
	url(r'^viewcourses/', views.view_courses, name='viewcourses'),
	url(r'^addfeedback/$', views.addfeedback, name='addfeedback'),
	url(r'^viewfeedback/$', views.viewfeedback, name='viewfeedback'),
	url(r'^deadlines/$', views.viewdeadlines, name='viewdeadlines'),
	url(r'^add-deadline/$', views.add_deadline, name='add_deadline'),
	url(r'^(?P<course_code>.+)/newdeadline/$', views.newdeadline, name='newdeadline'),
	url(r'^(?P<feedback_id>[0-9]+)/details/$', views.feedback_details, name='feedbackdetail'),
	url(r'^(?P<rollno>[0-9]+)/(?P<password>.+)/(?P<question_id>[0-9]+)/(?P<answer>[12345]{1})/$', views.mark_answer, name='markanswer'),
	url(r'^(?P<course_code>.+)/feedbacks/$', views.coursefeedbacks, name='feedbacks'),
	url(r'^(?P<course_code>.+)/newfeedback/$', views.newfeedback, name='newfeedback'),
	url(r'^(?P<course_code>.+)/$', views.course_detail, name='course_detail'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
