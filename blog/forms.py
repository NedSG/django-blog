from django import forms
from django.utils.translation import gettext_lazy as _

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