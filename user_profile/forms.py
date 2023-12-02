from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'email']
        widget = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': "введите ваш никнейм"})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': "введите пароль"})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': "введите пароль ещё раз"})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': "введите ваш адрес эл. почты"})


class UserLoginForm(AuthenticationForm):
    password1 = forms.TextInput,
    password2 = forms.TextInput,

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'введите ваш никнейм'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': "введите пароль"})
