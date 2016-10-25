from django.shortcuts import render

def index(request):

	# if not request.user.is_authenticated:
	# 	return render(request, 'login.html', {})

	return render(request, 'index.html', {})

def user_login(request):
	return render(request, 'login.html', {})