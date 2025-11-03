from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import SignupForm, LoginForm, UserUpdateForm, ProfileUpdateForm 
from django.contrib import messages # Messages framework import karein
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from tests.models import TestResult
from .models import Profile

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            messages.success(request, f'Account created successfully! Welcome to GovernPrep, {user.username}.')
            return redirect('/') 
    else:
        form = SignupForm()
    return render(request, 'users/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('/') 
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('exams:home')
    
@login_required
def dashboard_view(request):
    
    # User ke saare test results fetch karein
    results = TestResult.objects.filter(user=request.user).order_by('-timestamp')
    context = {
        
        'results': results
    }
    return render(request, 'users/dashboard.html', context)    


@login_required
def profile_view(request):
    Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        # p_form = ProfileUpdateForm(request.POST, instance=request.user.profile) # Ise tab use karein jab Profile form mein fields hon

        if u_form.is_valid(): # and p_form.is_valid():
            u_form.save()
            # p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('users:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        # p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        # 'p_form': p_form
    }
    return render(request, 'users/profile.html', context)