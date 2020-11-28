from django import forms
from app.models import Question


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'}))
    password = forms.CharField(max_length=20,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '******'}))


class AskForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите заголовок'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите текст вопроса'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'})
        }
