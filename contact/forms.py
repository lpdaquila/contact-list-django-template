import re
from typing import Any
from contact.models import Contact
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django import forms

class ContactForm(forms.ModelForm):    
    picture = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'accept': 'image/*',
            }
        )
    )
    
    first_name = forms.CharField(
        min_length=3,
        max_length=80,
    )
    
    class Meta:
        model = Contact
        fields = (
            'first_name', 
            'last_name', 
            'phone', 
            'email', 
            'description', 
            'category',
            'picture'
        )
      
    def clean_first_name(self) -> str | None:
        first_name = self.cleaned_data.get('first_name')
        if first_name == '':
            self.add_error(
                'first_name',
                ValidationError(
                    'First name cannot be empty',
                    code='invalid'
                )
            )
        return first_name
    
    def clean(self) -> dict[str, Any]:
        cleaned_data = self.cleaned_data
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        if first_name == last_name:
            self.add_error(
                'last_name',
                ValidationError(
                    'First name and last name cannot be the same',
                    code='invalid'
                )
            )
        return super().clean()
    
class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        min_length=3
    )
    last_name = forms.CharField(
        required=True,
        min_length=3
    )
    
    email = forms.EmailField(
        required=True,
    )
    
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2',
        )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            self.add_error(
                'email',
                ValidationError(
                    'Email already exists',
                    code='invalid'
                )
            )
        return email
    
class RegisterUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        min_length=3,
        max_length=80,
        required=True,
        help_text='Required'
    )
    
    last_name = forms.CharField(
        min_length=3,
        max_length=80,
        required=True,
        help_text='Required'
    )
    
    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )
    
    password2 = forms.CharField(
        label='Password confirmation',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',}),
        help_text='Enter the same password as before, for verification.',
        required=False,
    )
    
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'username',
        )
        
    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        user = super().save(commit=False)
        
        password = cleaned_data.get('password1')
        if password:
            user.set_password(password)
            
        if commit:
            user.save()
            
        return user
        
    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                self.add_error(
                    'password2',
                    ValidationError(
                        'Passwords do not match',
                        code='invalid'
                    )
                )
            
        return super().clean()
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.email
        if current_email != email:
            if User.objects.filter(email=email).exists():
                self.add_error(
                    'email',
                    ValidationError(
                        'Email already exists',
                        code='invalid'
                    )
                )
        return email
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        
        if password1:
            try:
                password_validation.validate_password(password1)
            except ValidationError as e:
                self.add_error(
                    'password1',
                    ValidationError(
                        e,
                        code='invalid'
                    )
                )
        
        return password1
    