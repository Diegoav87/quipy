from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm

from .models import CustomUser


class CustomUserForm(UserCreationForm):
    username = forms.CharField(
        label='Username', min_length=4, max_length=50, help_text='Required')
    email = forms.EmailField(max_length=100, help_text='Required', error_messages={
        'required': 'Sorry, you will need an email'})

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update(
            {"placeholder": "Email"})
        self.fields['username'].widget.attrs.update(
            {"placeholder": "Username"})
        self.fields['password1'].widget.attrs.update(
            {"placeholder": "Password"})
        self.fields['password2'].widget.attrs.update(
            {"placeholder": "Confirm password"})

    def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "User with this username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'User with this email already exists')
        return email


class UserEditForm(forms.ModelForm):
    username = forms.CharField(
        label='Username', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'form-firstname'}))

    class Meta:
        model = CustomUser
        fields = ('username',)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['username'].required = True

    def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.exclude(pk=self.request.user.pk).filter(username=username).exists():
            raise forms.ValidationError(
                "User with this username already exists")
        return username


class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        user = CustomUser.objects.filter(email=email)
        if not user:
            raise forms.ValidationError(
                'We could not find your account')
        return email


class PasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Confirm password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Confirm Password', 'id': 'form-new-pass2'}))
