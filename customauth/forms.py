from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "autofocus": True,
            "class": "input w-full"
        })
    )

    password = forms.CharField(
        label = 'パスワード',
        widget=forms.PasswordInput(attrs={
            "class": "input w-full"
        })
    )
