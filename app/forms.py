from django import forms
from app.models import Question, Answer


MAX_USERNAME_LENGTH = 50
MAX_PASSWORD_LENGTH = 20


class LoginForm(forms.Form):
    username = forms.CharField(max_length=MAX_USERNAME_LENGTH,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'}),
                               error_messages={'required': 'Введите логин'})

    password = forms.CharField(max_length=MAX_PASSWORD_LENGTH,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '******'}),
                               error_messages={'required': 'Введите пароль'})


class SignupForm(forms.Form):
    username = forms.CharField(max_length=MAX_USERNAME_LENGTH,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'}),
                               error_messages={'required': 'Введите логин'})

    password = forms.CharField(max_length=MAX_PASSWORD_LENGTH,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
                               error_messages={'required': 'Введите пароль'})

    confirm_password = forms.CharField(max_length=MAX_PASSWORD_LENGTH,
                                       widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                         'placeholder': 'Подтвердите пароль'}),
                                       error_messages={'required': 'Введите подтверждение пароля'})

    nickname = forms.CharField(max_length=MAX_USERNAME_LENGTH,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ник на сайте'}),
                               error_messages={'required': 'Введите ник'})

    profile_pic = forms.ImageField(required=False,
                                   widget=forms.FileInput(attrs={'class': 'custom-file-input', 'id': 'user-avatar'}))

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()

        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        if password and confirm_password and password != confirm_password:
            # непустые и не совпадают
            raise forms.ValidationError('Пароли не совпадают')

        return cleaned_data


# TODO: возможно, избавиться от дублирования
class EditForm(forms.Form):
    username = forms.CharField(max_length=MAX_USERNAME_LENGTH,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'}),
                               error_messages={'required': 'Введите логин'})

    nickname = forms.CharField(max_length=MAX_USERNAME_LENGTH,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ник на сайте'}),
                               error_messages={'required': 'Введите ник'})

    profile_pic = forms.ImageField(required=False,
                                   widget=forms.FileInput(attrs={'class': 'custom-file-input', 'id': 'user-avatar'}))


class AskForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите заголовок'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите текст вопроса'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'})
        }
        error_messages = {'title': {'required': 'Введите заголовок'},
                          'content': {'required': 'Введите текст вопроса'},
                          'tags': {'required': 'Введите хотя бы один тег'}}


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        widgets = {'content': forms.Textarea(attrs={'class': 'form-control mb-3',
                                                    'placeholder': 'Введите текст ответа'})}
        error_messages = {'content': {'required': 'Введите текст ответа'}}
