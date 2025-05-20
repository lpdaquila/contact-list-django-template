from django.shortcuts import redirect, render
from django.contrib import messages
from contact.forms import RegisterForm


def register(request):
    form = RegisterForm()
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User registered successfully')
            redirect('contact:index')
        
    return render(
        request,
        'contact/register.html',
        {
            'form': form
        }
    )