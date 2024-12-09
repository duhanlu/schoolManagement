from django import forms
from students.models import Student 
from django.core.exceptions import ValidationError
import datetime

ROLE_CHOICES = [
    ('admin', 'Manager'),
    ('teacher', 'Teacher'),
    ('student', 'Student')
]
class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please phone number'})
    )
    password = forms.CharField(
        max_length = 50,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Please enter phone number'})
    )
    role = forms.ChoiceField(label='Role', choices=ROLE_CHOICES)

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) == 0:
            raise ValidationError('Please enter correct username')
        return username
        
    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) == 0:
            raise ValidationError('password cannot be empty')
        return password
    
