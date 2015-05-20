from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    #password not visible when user types it out
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')
