from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import get_user_model

from.models import Posts

class AddPostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['title', 'content']
        labels = {"title": "", "content": ""}
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": _("Заголовок")}),
            "content": forms.Textarea(attrs={
                "class": "add-post-text-input",
                "placeholder": _("Текст..."),
                "rows": "20",
            }),
        }
        error_messages = {
            "title": {
                "unique": "Запись с таким названием уже существует."
            }
        }


# Auth forms

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": _("Имя пользователя")}),
        label='',
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": _("Пароль")}),
        label='',
    )


class UserCreateForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Введите пароль повторно")
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {
            "username": None,
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().filter(email=email).exists():
            return forms.ValidationError('Пользователь с такой почтой уже существует')
        return email


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput)
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="Подтверждение", widget=forms.PasswordInput)


class ProfileSettingsForm(forms.ModelForm):
    email = forms.CharField(disabled=True, label="Почта")

    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
