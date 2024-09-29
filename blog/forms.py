from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import get_user_model

from.models import Post, Comment

class AddPostForm(forms.ModelForm):
    """
    Форма для создания поста.

    Model:
        - `Post`.

    Using in:
        - Views: `AddPostView`, `UpdatePostView`.
        - Templates: `blog/add_post.html`, `blog/update_post.html`.

    Fields:
        - title (str): Заголовок поста.
        - content (str): Текст поста.
    """
    class Meta:
        model = Post
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

class AddCommentForm(forms.ModelForm):
    """
    Форма для создания комментария.

    Model:
        - `Comment`.

    Using in:
        - Views: `PostDetailView`.
        - Templates: `blog/post_detail.html`.

    Fields:
        - text (str): Текст комментария.
        - parent_comment (Comment): Родительский комментарий. Значением может быть NULL.
    """
    text = forms.CharField(label='', widget=forms.TextInput(attrs={"placeholder": "Введите текст"}))
    parent_comment = forms.ModelChoiceField(queryset=Comment.objects.all(), widget=forms.HiddenInput, required=False)
    class Meta:
        model = Comment
        fields = ['text', 'parent_comment']


# Auth forms

class CustomAuthenticationForm(AuthenticationForm):
    """
    Форма для аутентификации пользователя.

    Наследуется от AuthenticationForm, но убираются встроенные подписи и добавляется атрибут 'placeholder'.

    Using in:
        - Views: `LoginView` (используется напрямую в URLconf)
        - Templates: `registration/login.html`.

    Fields:
        - username (str): Имя пользователя.
        - password (str): Пароль
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": _("Имя пользователя")}),
        label='',
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": _("Пароль")}),
        label='',
    )


class UserCreateForm(UserCreationForm):
    """
    Форма для регистрации пользователя.

    Наследуется от UserCreationForm. Переопределяет поля паролей со своими подписями (атрибут label),
    удаляет help_text определяемый по умолчанию. Так же добавляет валидацию поля 'email' проверяя
    почту на уникальность.

    Using in:
        - Views: `registration_view`.
        - Templates: `registration\reg_page.html`.

    Fields:
        - username (str): Имя пользователя.
        - email (str): Электронная почта.
        - password1 (str): Пароль.
        - password2 (str): Подтверждение пароля.
    """
    password1 = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Введите пароль повторно")
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {
            "username": None,
        }

    def clean_email(self):
        """Проверяет нет ли пользователя с таким же email."""
        email = self.cleaned_data['email']
        if get_user_model().filter(email=email).exists():
            return forms.ValidationError('Пользователь с такой почтой уже существует')
        return email


class CustomPasswordChangeForm(PasswordChangeForm):
    """
    Форма для смены пароля.

    Наследуется от PasswordChangeForm и переопределяет все поля с новыми подписями (label).

    Using in:
        - Views: `CustomPasswordChangeView`.
        - Templates: `registration/password_change.html`.

    Fields:
        - old_password (str): Старый пароль.
        - new_password1 (str): Новый пароль.
        - new_password2 (str): Подтверждение нового пароля.
    """
    old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput)
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="Подтверждение", widget=forms.PasswordInput)


class ProfileSettingsForm(forms.ModelForm):
    """
    Форма для изменения данных пользователя.

    Model:
        - `User`

    Using in:
        - Views: `ProfileSettingsView`.
        - Templates: `blog/profile_settings.html`

    Fields:
        - email (str): Электронная почта. Поле закрыто для модификации(disabled=True).
        - first_name (str): Имя пользователя.
        - last_name (str): Фамилия пользователя.
    """
    email = forms.CharField(disabled=True, label="Почта")

    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
