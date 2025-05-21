import re
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from contact.forms import RegisterForm, RegisterUpdateForm
from django.contrib.auth.forms import AuthenticationForm

def register(request):
    form = RegisterForm()
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User registered successfully')
            redirect('contact:login')
        
    return render(
        request,
        'contact/register.html',
        {
            'form': form,
            'site_title': 'Register User',
        }
    )
    
def login_view(request):
    form = AuthenticationForm(request)
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            messages.success(request, f'Welcome {user.username}')
            return redirect('contact:index')
    
    return render(
        request,
        'contact/login.html',
        {
            'form': form,
            'site_title': 'Login',
        }
    )
    
@login_required(login_url='contact:login')
def logout_view(request):
    auth.logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('contact:login')

@login_required(login_url='contact:login')
def user_update(request):
    form = RegisterUpdateForm(instance=request.user)
    
    if request.method == 'POST':
        form = RegisterUpdateForm(data=request.POST, instance=request.user)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully')
            return redirect('contact:user_update')
    
    return render(
        request,
        'contact/user_update.html',
        {
            'form': form,
            'site_title': 'Update User',
        }
    )
    