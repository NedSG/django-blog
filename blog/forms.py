from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

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
    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None