from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm , UserForm	, GroupForm
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from django.views.decorators.http import require_POST
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
			return redirect('/')

	else:
		return render(request, 'log_in.html', {})


@login_required(login_url='log_in')
def editProfile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            login(request, User.objects.get(id=request.user.id) )
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')  # Redirect to the user's profile page
        else:
            messages.error(request, 'Error updating your profile. Please correct the errors below.')
    else: 
        form = ProfileForm(instance=request.user)

    return render(request, 'edit_profile.html', {'form': form})

def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group, created = Group.objects.get_or_create(name=form.cleaned_data['name'])
            # return redirect('create_user', group_id=group.id)
            return redirect('create_user')
    else:
        form = GroupForm()

    return render(request, 'create_user.html', {'form': form})


# def create_user(request, group_id):
    #group = Group.objects.get(pk=group_id)
def create_user(request):

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            userr = form.save(commit=False)
            userr.set_password('1234')
            userr.save()
            userr.groups.set(form.cleaned_data['groups'])
            return redirect('user_list')  # Redirect to a success page

#dont forget else:
    else:
        user_form = UserForm()
        group_form = GroupForm()

    return render(request, 'create_user.html', {'user_form': user_form, 'group_form': group_form})


def user_list(request):
	users = User.objects.all()
	context = {'users': users}
	return render(request, 'user_list.html', context )

@require_POST
def remove_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        userr = get_object_or_404(User, id=user_id)
        userr.delete()
        # Return a JSON response to the AJAX request
        return JsonResponse({'message': 'User removed successfully'})

    # Handle cases where the request method is not POST
    return JsonResponse({'error': 'Invalid request method'})

@require_POST
def activate_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        userr = get_object_or_404(User, id=user_id)
        userr.is_active= True
        userr.save()
        # Return a JSON response to the AJAX request
        return JsonResponse({'message': 'User Activated successfully'})

    # Handle cases where the request method is not POST
    return JsonResponse({'error': 'Invalid request method'})
	
def deactivate_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        userr = get_object_or_404(User, id=user_id)
        userr.is_active= False
        userr.save()
        # Return a JSON response to the AJAX request
        return JsonResponse({'message': 'User Deactivated successfully'})

    # Handle cases where the request method is not POST
    return JsonResponse({'error': 'Invalid request method'})


def log_out(request):
	logout(request)
	messages.success(request, ("You have been logged out"))
	return redirect('log_in')

