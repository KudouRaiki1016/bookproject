from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Class

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username',)

# class AddClassMembersForm(forms.ModelForm):
#     class Meta:
#         model = Class
#         fields = ('', 'user_name')