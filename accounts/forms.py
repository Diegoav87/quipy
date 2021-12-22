from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update(
            {"class": "form-control", "placeholder": "Email"})
        self.fields['username'].widget.attrs.update(
            {"class": "form-control", "placeholder": "Username"})
        self.fields['password1'].widget.attrs.update(
            {"class": "form-control", "placeholder": "Password"})
        self.fields['password2'].widget.attrs.update(
            {"class": "form-control", "placeholder": "Confirm password"})
