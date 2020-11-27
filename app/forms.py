from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, label="Введите логин")
    password = forms.CharField(max_length=20, label="Введите пароль")
