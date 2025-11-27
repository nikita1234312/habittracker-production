from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SigninForm(forms.Form):
    username = forms.CharField(max_length=32)
    password = forms.CharField(widget=forms.PasswordInput())


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']