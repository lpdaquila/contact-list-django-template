from typing import Any
from contact.models import Contact
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class ContactForm(forms.ModelForm):    
    picture = forms.ImageField(
        widget=forms.FileInput(attrs={
            'accept': 'image/*',
            }
        )
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
                    'Error: First name cannot be empty',
                    code='invalid'
                )
            )
            return None
        return first_name
    
    def clean(self) -> dict[str, Any]:
        cleaned_data = self.cleaned_data
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        if first_name == last_name:
            self.add_error(
                'last_name',
                ValidationError(
                    'Error: First name and last name cannot be the same',
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
            raise ValidationError(
                'Error: Email already exists',
                code='invalid'
            )
        return email
    