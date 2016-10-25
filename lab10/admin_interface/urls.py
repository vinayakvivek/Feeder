from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^index/', views.index, name='index'),
	url(r'^login/', views.user_login, name='login'),
	url(r'^register/', views.register, name='register'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
