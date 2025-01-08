from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from django.contrib.auth.models import User
from . import models

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password',)

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'password1', 'password2',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ('recall', 'text',)