from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    # add email to send email (UserCreationForm has three fields: username, password1, password2)
    email = forms.EmailField(max_length=200, help_text='Required')
    firstname = forms.CharField(max_length=64, help_text='Required')
    lastname = forms.CharField(max_length=64, help_text='Required')
    class Meta:
        model = User
        fields = ('firstname', 'lastname', 'username', 'email', 'password1', 'password2')
