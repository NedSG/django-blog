from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from django.utils import timezone, dateformat
from django.template.defaultfilters import timesince
from datetime import timedelta


class Posts(models.Model):
    title = models.CharField(max_length=200, unique=True)
    content = models.TextField()
#    status = models.CharField(max_length=10, default="draft", help_text="May be either 'draft' or 'published")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(db_index=True, unique=True)
    last_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
#    pub_date = models.DateTimeField(null=True)

    class Meta:
        ordering = ['-date_created']
        indexes = [
            models.Index(fields=['-date_created'], name='IDX_posts_datecreated'),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={'slug': self.slug})

    def timesince(self):
        diff = timezone.now() - self.date_created
        if diff < timedelta(days=365):
            if diff > timedelta(days=7):
                format = 'd M в H:i'
            else:
                return timesince(self.date_created, timezone.now()).split(',')[0] + ' назад'
        else:
            format = 'd E Y'
        return dateformat.format(self.date_created, format)

#    def clean(self):
#        if self.status == 'draft' and self.pub_date is not None:
#            raise ValidationError(
#                {"pub_date": _("Черновики не могут иметь дату публикации")}
#            )
#        if self.status == "published" and self.pub_date is None:
#            self.pub_date = timezone.now()

class Comments(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=900)
    date_created = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE)

    class Meta:
        ordering = ['date_created']
        indexes = [
            models.Index(fields=['date_created'], name='IDX_comments_datecreated'),
        ]

    def __str__(self):
        return f"{self.post}_{self.author}"