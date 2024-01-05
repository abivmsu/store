from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.

def log_in(request):
	if request.method == "POST":
		user_name = request.POST['user_name']
		password = request.POST['password']
		user = authenticate(request, username=user_name, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, ("You Have Been Logged In!"))
			return redirect('index')
		else:
			messages.success(request, ("There was an error, please try again..."))
			return redirect('login')

	else:
		return render(request, 'log_in.html', {})


def log_out(request):
	logout(request)
	messages.success(request, ("You have been logged out"))
	return redirect('log_in')

